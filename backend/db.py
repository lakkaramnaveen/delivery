from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session
from config import Config


# --------------------------------------------------------
# SQLAlchemy engine with SQLite-specific setting
# check_same_thread=False allows usage across threads
# --------------------------------------------------------
engine = create_engine(
    Config.SQLALCHEMY_DATABASE_URI,
    future=True,
    echo=Config.SQLALCHEMY_ECHO,
    pool_pre_ping=True,         # avoid stale connections
    pool_recycle=1800,
)

# --------------------------------------------------------
# Factory to create new database sessions
# Use: session = SessionLocal()
# --------------------------------------------------------
SessionLocal = scoped_session(sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True))

# --------------------------------------------------------
# Base class for declarative models
# All model classes should inherit from this
# --------------------------------------------------------
Base = declarative_base()
