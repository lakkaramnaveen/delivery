from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# --------------------------------------------------------
# SQLite database connection string
# For production, you may switch to PostgreSQL/MySQL
# --------------------------------------------------------
DATABASE_URL = "sqlite:///deliveries.db"

# --------------------------------------------------------
# SQLAlchemy engine with SQLite-specific setting
# check_same_thread=False allows usage across threads
# --------------------------------------------------------
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # SQLite-specific
    echo=False  # Set to True only for debugging SQL queries
)

# --------------------------------------------------------
# Factory to create new database sessions
# Use: session = SessionLocal()
# --------------------------------------------------------
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --------------------------------------------------------
# Base class for declarative models
# All model classes should inherit from this
# --------------------------------------------------------
Base = declarative_base()
