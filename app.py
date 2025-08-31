import os
from passlib.hash import sha256_crypt
import psycopg2
from flask import *
app = Flask(__name__)
app.secret_key="loginform"
def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='university_db',
                            user=os.environ['DB_USERNAME'],
                            password=os.environ['DB_PASSWORD'])
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('select * from student')

    student_data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html')

@app.route('/signup/', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        name = request.form['nm']
        email = request.form['em']
        password = request.form['pwd']
        studentId = request.form['id']

        # Hash password before storing it
        encpassword = sha256_crypt.encrypt(password)
        
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute('INSERT INTO student (password, name, email, StudentId) VALUES (%s, %s, %s, %s)',
                    (encpassword, name, email, studentId))

            conn.commit()
            cur.close()
            conn.close()
            
            return redirect(url_for('index'))
        except:
            return redirect(url_for('signup'))

        
    return render_template('signup.html')

@app.route('/attendancesfill', methods=['POST'])
def attendance():
    if request.method == 'POST':
        studentId = request.form['studentId']
        date = request.form['date']
        status = request.form['status']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO Attendance(StudentId, Date, AttendStatus) VALUES(%s, %s, %s)', (studentId, date, status))
        conn.commit()
        cur.close()
        conn.close()
        return render_template('Attendance_submission.html')


@app.route('/attendence/')
def attendence():
    return redirect(url_for('SignIn'))

@app.route('/announcement/', methods=['POST', 'GET'])
def announcement():
    if request.method == "POST":
        title = request.form['announcement_title']
        content = request.form["announcement_content"]

        return render_template('Announcements.html', title = title, content=content)
    else:
        return render_template('Announcements.html')


@app.route("/SignIn/", methods=['POST', 'GET'])
def SignIn():
    if request.method == 'POST':
        studentId = request.form['id']
        password = request.form['pwd']
        conn = get_db_connection()
        cur = conn.cursor()

        # Fetch data from the student table
        cur.execute('SELECT * FROM student WHERE StudentId = %s', (studentId,))
        student_data = cur.fetchone()

        # Fetch data from the attendance table
        cur.execute('SELECT * FROM attendance WHERE StudentId = %s', (studentId,))
        attendance_data = cur.fetchall()

        try:
            if student_data and sha256_crypt.verify(password, student_data[0]):
                name = student_data[1]
                return render_template('Attendance.html', name=name, attendance_data=attendance_data, studentId=studentId)
            else:
                error = "Student ID or password may be incorrect."
                return render_template('SignIn.html', error=error)
        finally:
            conn.commit()
            cur.close()
            conn.close()

    else:
        return render_template('SignIn.html')

@app.route('/LeaveRequest/', methods=['POST', 'GET'])
def LeaveRequest():
    if request.method == 'POST':
        StudentId = request.form['student_id']
        reason = request.form['reason']
        conn = get_db_connection()
        cur = conn.cursor()

        # Fetch data from the student table
        cur.execute('SELECT * FROM student WHERE studentId = %s', (StudentId,))
        student_data = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        return render_template('LR_Submission.html', name=student_data[1])

    else:
        return render_template("LeaveRequest.html")
