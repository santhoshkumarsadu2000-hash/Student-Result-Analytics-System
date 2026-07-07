import pymysql

def get_connection():
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="Santhosh@1982",
        database="student_result_db"
    )
    return connection