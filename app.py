from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData
import os

# Configure naming convention for foreign keys
convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": 'uq_%(table_name)s_%(column_0_name)s',
    "ck": 'ck_%(table_name)s_%(constraint_name)s',
    "fk": 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    "pk": 'pk_%(table_name)s'
}

metadata = MetaData(naming_convention=convention)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return '<h1>The Late Show API</h1>'

# Import models after db is initialized
from models import Episode, Guest, Appearance

# GET /episodes
@app.route('/episodes', methods=['GET'])
def get_episodes():
    episodes = Episode.query.all()
    return jsonify([episode.to_dict() for episode in episodes])

# GET /episodes/<int:id>
@app.route('/episodes/<int:id>', methods=['GET'])
def get_episode(id):
    episode = Episode.query.get(id)
    if not episode:
        return jsonify({'error': 'Episode not found'}), 404
    
    # Build response with appearances and guest info
    episode_dict = episode.to_dict()
    episode_dict['appearances'] = []
    
    for appearance in episode.appearances:
        appearance_dict = appearance.to_dict()
        # Get guest info without recursion
        guest_dict = {
            'id': appearance.guest.id,
            'name': appearance.guest.name,
            'occupation': appearance.guest.occupation
        }
        appearance_dict['guest'] = guest_dict
        episode_dict['appearances'].append(appearance_dict)
    
    return jsonify(episode_dict)

# DELETE /episodes/<int:id>
@app.route('/episodes/<int:id>', methods=['DELETE'])
def delete_episode(id):
    episode = Episode.query.get(id)
    if not episode:
        return jsonify({'error': 'Episode not found'}), 404
    
    try:
        db.session.delete(episode)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# GET /guests
@app.route('/guests', methods=['GET'])
def get_guests():
    guests = Guest.query.all()
    guests_list = []
    for guest in guests:
        guests_list.append({
            'id': guest.id,
            'name': guest.name,
            'occupation': guest.occupation
        })
    return jsonify(guests_list)

# POST /appearances
@app.route('/appearances', methods=['POST'])
def create_appearance():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['rating', 'episode_id', 'guest_id']
        if not data or not all(field in data for field in required_fields):
            return jsonify({'errors': ['Missing required fields']}), 422
        
        # Check if episode and guest exist
        episode = Episode.query.get(data['episode_id'])
        guest = Guest.query.get(data['guest_id'])
        
        if not episode:
            return jsonify({'errors': ['Episode not found']}), 422
        if not guest:
            return jsonify({'errors': ['Guest not found']}), 422
        
        # Validate rating
        rating = data['rating']
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            return jsonify({'errors': ['Rating must be an integer between 1 and 5']}), 422
        
        # Create appearance
        appearance = Appearance(
            rating=rating,
            episode_id=data['episode_id'],
            guest_id=data['guest_id']
        )
        
        db.session.add(appearance)
        db.session.commit()
        
        # Prepare response
        response = {
            'id': appearance.id,
            'rating': appearance.rating,
            'guest_id': appearance.guest_id,
            'episode_id': appearance.episode_id,
            'episode': {
                'id': episode.id,
                'date': episode.date,
                'number': episode.number
            },
            'guest': {
                'id': guest.id,
                'name': guest.name,
                'occupation': guest.occupation
            }
        }
        
        return jsonify(response), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'errors': [str(e)]}), 422

if __name__ == '__main__':
    app.run(port=5555, debug=True)