import pymysql

def get_connection():
    connection = pymysql.connect(
        host="mysql-3573fd4b-santhoshkumarsadu2000-e072.a.aivencloud.com",
        user="avnadmin",
        password="AVNS_1h9ZJi7XgqcijG_64Qu",
        database="defaultdb"
    )
    return connection
