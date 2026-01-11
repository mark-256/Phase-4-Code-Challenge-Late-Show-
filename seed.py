import csv
import os
from app import app, db
from models import Episode, Guest, Appearance

def clear_data():
    """Clear existing data from tables"""
    db.drop_all()
    db.create_all()
    print("✓ Database tables created")

def seed_episodes():
    """Seed episodes from CSV or default data"""
    episodes = []
    
    # Try to load from CSV if exists
    csv_file = 'episodes.csv'
    if os.path.exists(csv_file):
        try:
            with open(csv_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    episodes.append(Episode(
                        date=row['date'],
                        number=int(row['number'])
                    ))
            print(f"✓ Loaded episodes from {csv_file}")
        except Exception as e:
            print(f"⚠ Error loading CSV: {e}")
            # Fall back to default data
            episodes = [
                Episode(date='1/11/99', number=1),
                Episode(date='1/12/99', number=2),
                Episode(date='1/13/99', number=3),
                Episode(date='1/14/99', number=4),
                Episode(date='1/15/99', number=5),
            ]
    else:
        # Default data
        episodes = [
            Episode(date='1/11/99', number=1),
            Episode(date='1/12/99', number=2),
            Episode(date='1/13/99', number=3),
            Episode(date='1/14/99', number=4),
            Episode(date='1/15/99', number=5),
        ]
        print("✓ Using default episode data")
    
    db.session.add_all(episodes)
    db.session.commit()
    print(f"✓ Seeded {len(episodes)} episodes")
    return episodes

def seed_guests():
    """Seed guests from CSV or default data"""
    guests = []
    
    # Try to load from CSV if exists
    csv_file = 'guests.csv'
    if os.path.exists(csv_file):
        try:
            with open(csv_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    guests.append(Guest(
                        name=row['name'],
                        occupation=row['occupation']
                    ))
            print(f"✓ Loaded guests from {csv_file}")
        except Exception as e:
            print(f"⚠ Error loading CSV: {e}")
            # Fall back to default data
            guests = [
                Guest(name='Michael J. Fox', occupation='actor'),
                Guest(name='Sandra Bernhard', occupation='Comedian'),
                Guest(name='Tracey Ullman', occupation='television actress'),
                Guest(name='Kevin Bacon', occupation='actor'),
                Guest(name='David Bowie', occupation='musician'),
                Guest(name='Madonna', occupation='singer'),
                Guest(name='Robin Williams', occupation='actor/comedian'),
                Guest(name='Julia Roberts', occupation='actress'),
                Guest(name='Tom Hanks', occupation='actor'),
                Guest(name='Beyoncé', occupation='singer'),
            ]
    else:
        # Default data
        guests = [
            Guest(name='Michael J. Fox', occupation='actor'),
            Guest(name='Sandra Bernhard', occupation='Comedian'),
            Guest(name='Tracey Ullman', occupation='television actress'),
            Guest(name='Kevin Bacon', occupation='actor'),
            Guest(name='David Bowie', occupation='musician'),
            Guest(name='Madonna', occupation='singer'),
            Guest(name='Robin Williams', occupation='actor/comedian'),
            Guest(name='Julia Roberts', occupation='actress'),
            Guest(name='Tom Hanks', occupation='actor'),
            Guest(name='Beyoncé', occupation='singer'),
        ]
        print("✓ Using default guest data")
    
    db.session.add_all(guests)
    db.session.commit()
    print(f"✓ Seeded {len(guests)} guests")
    return guests

def seed_appearances(episodes, guests):
    """Seed appearances with random ratings"""
    import random
    
    appearances = []
    
    # Create some appearances
    appearance_data = [
        (1, 1, 4),  # episode 1, guest 1, rating 4
        (1, 2, 5),  # episode 1, guest 2, rating 5
        (2, 3, 3),  # episode 2, guest 3, rating 3
        (2, 4, 4),  # episode 2, guest 4, rating 4
        (3, 5, 5),  # episode 3, guest 5, rating 5
        (3, 6, 4),  # episode 3, guest 6, rating 4
        (4, 7, 5),  # episode 4, guest 7, rating 5
        (4, 8, 3),  # episode 4, guest 8, rating 3
        (5, 9, 5),  # episode 5, guest 9, rating 5
        (5, 10, 4), # episode 5, guest 10, rating 4
    ]
    
    for ep_idx, guest_idx, rating in appearance_data:
        # Make sure indices are within range
        if ep_idx <= len(episodes) and guest_idx <= len(guests):
            appearances.append(Appearance(
                rating=rating,
                episode_id=ep_idx,
                guest_id=guest_idx
            ))
    
    # Add some random appearances
    for _ in range(10):
        ep = random.choice(episodes)
        guest = random.choice(guests)
        rating = random.randint(1, 5)
        
        # Check if this appearance already exists
        existing = Appearance.query.filter_by(
            episode_id=ep.id,
            guest_id=guest.id
        ).first()
        
        if not existing:
            appearances.append(Appearance(
                rating=rating,
                episode_id=ep.id,
                guest_id=guest.id
            ))
    
    db.session.add_all(appearances)
    db.session.commit()
    print(f"✓ Seeded {len(appearances)} appearances")

def main():
    """Main seeding function"""
    print("Starting database seeding...")
    
    with app.app_context():
        # Clear and create tables
        clear_data()
        
        # Seed data
        episodes = seed_episodes()
        guests = seed_guests()
        seed_appearances(episodes, guests)
        
        print("\n✅ Database seeding completed successfully!")
        print(f"   Total Episodes: {len(episodes)}")
        print(f"   Total Guests: {len(guests)}")
        print(f"   Total Appearances: {Appearance.query.count()}")

if __name__ == '__main__':
    main()