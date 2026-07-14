import os
import pymysql

def get_connection():
    """
    Establishes a secure SSL connection to the Aiven MySQL Database.
    Reads sensitive database credentials from system environment variables.
    """
    
    # 1. Dynamically locate the path to the 'ca.pem' certificate
    current_dir = os.path.dirname(os.path.abspath(__file__))
    cert_path = os.path.join(current_dir, "ca.pem")
    
    # 2. Establish connection using environment variables (fallback to hardcoded values for local testing)
    connection = pymysql.connect(
        host=os.environ.get("DB_HOST", "://aivencloud.com"),
        port=int(os.environ.get("DB_PORT", 12864)),
        user=os.environ.get("DB_USER", "avnadmin"),
        password=os.environ.get("DB_PASSWORD", "AVNS_1h9ZJi7XgqcijG_64Qu"),
        database=os.environ.get("DB_NAME", "defaultdb"),
        ssl={'ca': cert_path},
        cursorclass=pymysql.cursors.DictCursor  # Returns query results as clean Python dictionaries
    )
    
    return connection
