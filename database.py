from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



try:
    SQLALCHEMY_DATABASE_URL = "mssql+pyodbc://localhost\\SQLEXPRESS/CarDB?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        echo=True,
        pool_pre_ping=True,
        pool_recycle=300
    )
    # Test connection
    with engine.connect() as conn:
        from sqlalchemy import text
        conn.execute(text("SELECT 1"))
    print("Connected to MSSQL Server successfully!")
except Exception as e:
    print(f"MSSQL connection failed: {e}")
    print("Falling back to SQLite...")
    SQLALCHEMY_DATABASE_URL = "sqlite:///./cars.db"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        echo=True,
        connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    try:
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully!")
    except Exception as e:
        print(f"Error creating tables: {e}")
        raise
