import psycopg2

try:
    cnx = psycopg2.connect(user="team5hack", password="IneedApa$$word", host="team5-postgres-db.postgres.database.azure.com", port=5432, database="postgres")
    print("Connection successful.")
except Exception as e:
    print(f"Connection failed: {e}")
    exit(1)

cursor = cnx.cursor()

dummydata = '_dummydata' # '_dummydata' or ''

cursor.execute(f"CREATE SCHEMA IF NOT EXISTS team5_schema{dummydata};")
cursor.execute(f"SET search_path TO team5_schema{dummydata};")
    


# Create table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS vendors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS criteria_categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS criteria (
    id SERIAL PRIMARY KEY,
    criteria_categories_id INT REFERENCES criteria_categories(id),
    name VARCHAR(100),
    goal VARCHAR(100),
    weight INT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS responses (
    id SERIAL PRIMARY KEY,
    criteria_id INT REFERENCES criteria(id),
    vendors_id INT REFERENCES vendors(id),
    response_text TEXT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS costs (
    id SERIAL PRIMARY KEY,
    criteria_categories_id INT REFERENCES criteria_categories(id),
    vendors_id INT REFERENCES vendors(id),
    cost DECIMAL(10, 2)
);
""")


cursor.execute(f"SELECT COUNT(*) FROM criteria_categories;")
row_count = cursor.fetchone()[0]

if row_count <= 0:
    data = [("schedule",), ("expertise",), ("risk",), ("solution",), ("training",), ("support",), ("quality assurance",), ("rights",)]
    cursor.executemany(
        "INSERT INTO criteria_categories (name) VALUES (%s);",
        data
    )



cnx.commit()


cursor.execute("SELECT * FROM criteria_categories;")
rows = cursor.fetchall()
for row in rows:
    print(row)

