# Late Show Application

A Flask application for managing late show data with SQLAlchemy ORM and Alembic migrations.

## Features

- Flask web framework
- SQLAlchemy ORM for database management
- Alembic for database migrations
- PostgreSQL database support
- Environment variable configuration

## Installation
# Initialize migrations
flask db init

# Create initial migration
flask db migrate -m "Initial tables"

# Apply migration
flask db upgrade

# Seed the database
python seed.py

## Project Structure

```
lateshow/
├── app.py           # Main Flask application
├── models.py        # Database models
├── seed.py          # Database seeding script
├── migrations/      # Alembic migrations
│   ├── versions/    # Migration version files
│   ├── alembic.ini  # Alembic configuration
│   └── env.py       # Migration environment
├── Pipfile          # Python dependencies
├── .env             # Environment variables
└── .gitignore       # Git ignore rules
```

## API Endpoints

(Add your API endpoints here)

## License

MIT
