import psycopg2
import sys

try:
    conn = psycopg2.connect('postgresql://postgres:postgres123@localhost:5432/edumate')
    cur = conn.cursor()
    cur.execute('SELECT 1 as test')
    result = cur.fetchone()
    print(f"Database connection successful: {result}")
    conn.close()
    sys.exit(0)
except Exception as e:
    print(f"Database connection failed: {e}")
    sys.exit(1)