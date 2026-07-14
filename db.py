import os
import pymysql

def get_connection():
    connection = pymysql.connect(
        host=os.environ.get("DB_HOST"),
        port=int(os.environ.get("DB_PORT", 3306)),
        user=os.environ.get("root"),
        password=os.environ.get("Santhosh@1982"),
        database=os.environ.get("student_result_db"),
    )
    return connection