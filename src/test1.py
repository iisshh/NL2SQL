#Connecting to the database
from langchain_community.utilities import SQLDatabase
import os
from sqlalchemy import create_engine



# password = os.getenv('MYSQL_PASSWORD')
user = "root"
password = "admin1234"
host = "localhost"
port ="3306"
database = "classicmodels"

print(f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}")

db_uri = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"

db=SQLDatabase.from_uri(db_uri)

# try:
#     engine = create_engine(db_uri)
#     connection = engine.connect()
#     print("Connection successful")
#     connection.close()
# except Exception as e:
#     print(f"Connection failed: {e}")

print(db.dialect) # get the dialect
print(db.get_usable_table_names())  # get all table names
print(db.table_info) # get all table info