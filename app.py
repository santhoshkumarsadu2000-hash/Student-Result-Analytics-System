import os
from flask import Flask, render_template, request, redirect, url_for 
from db import get_connection

app = Flask(__name__)

def init_db():
    """Automatically builds missing tables before the application starts up."""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # 1. Create students table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    student_id INT AUTO_INCREMENT PRIMARY KEY,
                    roll_number VARCHAR(50) NOT NULL UNIQUE,
                    full_name VARCHAR(150) NOT NULL,
                    gender VARCHAR(20),
                    department VARCHAR(100),
                    year_of_study INT,
                    email VARCHAR(150),
                    phone VARCHAR(20)
                )
            """)
            # 2. Create subjects table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS subjects (
                    subject_id INT AUTO_INCREMENT PRIMARY KEY,
                    subject_name VARCHAR(100) NOT NULL UNIQUE
                )
            """)
            # 3. Create marks table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS marks (
                    mark_id INT AUTO_INCREMENT PRIMARY KEY,
                    student_id INT,
                    subject_id INT,
                    marks INT,
                    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
                )
            """)
            connection.commit()
            print("Database tables initialized successfully.")
    except Exception as e:
        print(f"Database initialization error: {e}")
    finally:
        connection.close()

# Trigger table check/creation
init_db()

@app.route("/")
def home():
    connection = get_connection()
    cursor = connection.cursor()

    # Total Students
    cursor.execute("SELECT COUNT(*) as total FROM students")
    total_students = cursor.fetchone()['total']

    # Total Subjects
    cursor.execute("SELECT COUNT(*) as total FROM subjects")
    total_subjects = cursor.fetchone()['total']

    # Average Marks
    cursor.execute("SELECT AVG(marks) as avg_marks FROM marks")
    avg_res = cursor.fetchone()['avg_marks']
    average_marks = round(float(avg_res), 2) if avg_res is not None else 0.0

    cursor.close()
    connection.close()

    return render_template(
        "home.html",
        total_students=total_students,
        total_subjects=total_subjects,
        average_marks=average_marks
    )

@app.route("/students")
def students():
    connection = get_connection()
    cursor = connection.cursor()

    search = request.args.get("search", "")

    if search:
        query = """
        SELECT * FROM students
        WHERE roll_number LIKE %s
        OR full_name LIKE %s
        """
        value = ("%" + search + "%", "%" + search + "%")
        cursor.execute(query, value)
    else:
        cursor.execute("SELECT * FROM students")

    students_list = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("students.html", students=students_list)

@app.route("/add")
def add_student():
    return render_template("add_student.html")

@app.route("/edit/<int:student_id>")
def edit_student(student_id):
    connection = get_connection()
    cursor = connection.cursor()

    query = "SELECT * FROM students WHERE student_id = %s"
    cursor.execute(query, (student_id,))

    student = cursor.fetchone()

    cursor.close()
    connection.close()

    return render_template("edit_student.html", student=student)

@app.route("/add", methods=["POST"])
def save_student():
    try:
        roll_number = request.form["roll_number"]
        name = request.form["name"]
        gender = request.form["gender"]
        department = request.form["department"]
        year = request.form["year"]
        email = request.form["email"]
        phone = request.form["phone"]

        connection = get_connection()
        cursor = connection.cursor()

        query = """
        INSERT INTO students
        (roll_number, full_name, gender, department, year_of_study, email, phone)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        values = (roll_number, name, gender, department, year, email, phone)
        cursor.execute(query, values)
        connection.commit()

        cursor.close()
        connection.close()

        return redirect("/students")
    except Exception as e:
        return str(e)

@app.route("/update", methods=["POST"])
def update_student():
    student_id = request.form["student_id"]
    roll_number = request.form["roll_number"]
    name = request.form["name"]
    gender = request.form["gender"]
    department = request.form["department"]
    year = request.form["year"]
    email = request.form["email"]
    phone = request.form["phone"]

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    UPDATE students
    SET
        roll_number = %s,
        full_name = %s,
        gender = %s,
        department = %s,
        year_of_study = %s,
        email = %s,
        phone = %s
    WHERE student_id = %s
    """

    values = (roll_number, name, gender, department, year, email, phone, student_id)

    cursor.execute(query, values)
    connection.commit()
    cursor.close()
    connection.close()
    return redirect("/students") 

@app.route("/delete/<int:student_id>")
def delete_student(student_id):
    connection = get_connection()
    cursor = connection.cursor()
    query = "DELETE FROM students WHERE student_id = %s"
    cursor.execute(query, (student_id,))
    connection.commit()

    cursor.close()
    connection.close()

    return redirect("/students")

if __name__ == "__main__":
    # Uses port environment variable assigned by Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
