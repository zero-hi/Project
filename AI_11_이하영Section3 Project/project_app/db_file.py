import psycopg2

conn = psycopg2.connect(
    host="arjuna.db.elephantsql.com",
    database="dmaytoab",
    user="dmaytoab",
    password="TcT8CabQtMBOEyHoo1me5nfChDF0vdtR")

cur = conn.cursor()




