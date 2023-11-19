import os
import psycopg2

conn = psycopg2.connect(
        host="localhost",
        database="university_db",
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'])


# Open a cursor to perform database operations
cur = conn.cursor()

# Open a cursor to perform database operations
cur.execute('DROP TABLE IF EXISTS Student;')
cur = conn.cursor()
cur.execute('''
    CREATE TABLE Student(
        password VARCHAR(256) NOT NULL,
        Name VARCHAR(30) NOT NULL,
        Email VARCHAR(60) NOT NULL,
        StudentId VARCHAR(10) NOT NULL,
        PRIMARY KEY (password)
    )
''')
cur.execute('DROP TABLE IF EXISTS Attendance;')
cur.execute('''CREATE TABLE Attendance(StudentId VARCHAR(10) NOT NULL, Date DATE, AttendStatus VARCHAR(30))''')

conn.commit()
cur.close()
conn.close()