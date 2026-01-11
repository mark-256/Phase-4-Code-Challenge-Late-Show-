from app import db
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

class Episode(db.Model):
    __tablename__ = 'episodes'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    number = db.Column(db.Integer, nullable=False)
    
    # Relationships
    appearances = db.relationship('Appearance', back_populates='episode', 
                                  cascade='all, delete-orphan')
    
    # Association proxy to get guests through appearances
    guests = association_proxy('appearances', 'guest',
                               creator=lambda guest: Appearance(guest=guest))
    
    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date,
            'number': self.number
        }

class Guest(db.Model):
    __tablename__ = 'guests'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    occupation = db.Column(db.String, nullable=False)
    
    # Relationships
    appearances = db.relationship('Appearance', back_populates='guest', 
                                  cascade='all, delete-orphan')
    
    # Association proxy to get episodes through appearances
    episodes = association_proxy('appearances', 'episode',
                                 creator=lambda episode: Appearance(episode=episode))
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'occupation': self.occupation
        }

class Appearance(db.Model):
    __tablename__ = 'appearances'
    
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id', ondelete='CASCADE'), nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id', ondelete='CASCADE'), nullable=False)
    
    # Relationships
    episode = db.relationship('Episode', back_populates='appearances')
    guest = db.relationship('Guest', back_populates='appearances')
    
    # Validation
    @validates('rating')
    def validate_rating(self, key, rating):
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            raise ValueError("Rating must be an integer between 1 and 5")
        return rating
    
    def to_dict(self):
        return {
            'id': self.id,
            'rating': self.rating,
            'episode_id': self.episode_id,
            'guest_id': self.guest_id
        }