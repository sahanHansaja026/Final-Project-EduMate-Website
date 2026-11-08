import os
import psycopg2

# Set the database URL explicitly
os.environ['DATABASE_URL'] = 'postgresql://postgres:postgres123@localhost:5432/edumate?sslmode=disable'

# Test connection directly
try:
    conn = psycopg2.connect('postgresql://postgres:postgres123@localhost:5432/edumate')
    cur = conn.cursor()
    cur.execute('SELECT 1 as test')
    print("Direct connection successful:", cur.fetchone())
    conn.close()
except Exception as e:
    print("Direct connection failed:", e)

# Now test SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(os.environ['DATABASE_URL'])
print("SQLAlchemy engine created successfully")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Try to create all tables (this was failing before)
try:
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully")
except Exception as e:
    print("Table creation info:", str(e)[:200])