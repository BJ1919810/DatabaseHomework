import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=8888,
    database="finance",
    user="dbuser",
    password="Test@123"
)

cur = conn.cursor()
cur.execute("""
    CREATE TABLE client(
    c_id INT PRIMARY KEY,
    c_name VARCHAR(100) NOT NULL,
    c_mail CHAR(30) UNIQUE,
    c_id_card CHAR(20) UNIQUE NOT NULL,
    c_phone CHAR(20) UNIQUE NOT NULL,
    c_password CHAR(20) NOT NULL
);
""")
conn.commit()

cur.close()
conn.close()
