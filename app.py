from flask import Flask, render_template, request, redirect, url_for 
from db import get_connection

app = Flask(__name__)


@app.route("/")
def home():
    connection = get_connection()
    cursor = connection.cursor()

    # Total Students
    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    # Total Subjects
    cursor.execute("SELECT COUNT(*) FROM subjects")
    total_subjects = cursor.fetchone()[0]

    # Average Marks
    cursor.execute("SELECT AVG(marks) FROM marks")
    average_marks = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return render_template(
        "home.html",
        total_students=total_students,
        total_subjects=total_subjects,
        average_marks=round(average_marks, 2)
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

    students = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("students.html", students=students)


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

        values = (
            roll_number,
            name,
            gender,
            department,
            year,
            email,
            phone
        )

        print(values)

        cursor.execute(query, values)
        connection.commit()

        print("Inserted Successfully")

        cursor.close()
        connection.close()

        return redirect("/students")

    except Exception as e:
        print(e)
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

    values = (
        roll_number,
        name,
        gender,
        department,
        year,
        email,
        phone,
        student_id
    )

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
    app.run(debug=True)