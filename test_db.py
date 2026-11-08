import psycopg2

conn = psycopg2.connect('postgresql://postgres:postgres123@localhost:5432/edumate')
cur = conn.cursor()
cur.execute('SELECT 1 as test')
print(cur.fetchone())
conn.close()
print("Database connection successful!")