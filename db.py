import os
import pymysql

def get_connection():
    """
    Establishes a secure SSL connection to the Aiven MySQL Database.
    """
    # Dynamically find the absolute path to 'ca.pem' so it works on Linux/Render
    current_dir = os.path.dirname(os.path.abspath(__file__))
    cert_path = os.path.join(current_dir, "ca.pem")
    
    connection = pymysql.connect(
        host=os.environ.get("DB_HOST", "mysql-3573fd4b-santhoshkumarsadu2000-e072.a.aivencloud.com"),
        port=int(os.environ.get("DB_PORT", 12864)),
        user=os.environ.get("DB_USER", "avnadmin"),
        password=os.environ.get("DB_PASSWORD", "AVNS_1h9ZJi7XgqcijG_64Qu"),
        database=os.environ.get("DB_NAME", "defaultdb"),
        ssl={'ca': cert_path},
        cursorclass=pymysql.cursors.DictCursor
    )
    
    return connection
