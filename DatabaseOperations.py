import mysql.connector
from mysql.connector import errorcode

#change config information before you use it

config = {
  'user': 'root',
  'password': '',
  'host': 'localhost',
  'database': 'network_t',
  'raise_on_warnings': True
}

TABLES = {}

#creating table
def create_tables(TABLES):
  #connect to database
  cnx = mysql.connector.connect(**config)
  cursor = cnx.cursor()
  #create tables
  for name, ddl in TABLES.iteritems():
    try:
      print ("Creating table {}: ".format(name))
      cursor.execute(ddl)
    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
        print("already exists.")
      else:
        print(err.msg)
    else:
      print("OK")
  #close connection
  cursor.close()
  cnx.close()

#inserting data
def insert_data(insert_format, insert_data):
  #connect to database
  cnx = mysql.connector.connect(**config)
  cursor = cnx.cursor()
  #insert data
  cursor.execute(insert_format, insert_data)
  cnx.commit()
  #close connection
  cursor.close()
  cnx.close()

#querying data
def query_data(query):
  #connect to database
  cnx = mysql.connector.connect(**config)
  cursor = cnx.cursor()
  #excute query
  cursor.execute(query)
  results = cursor.fetchall()
  #close connection
  cursor.close()
  cnx.close()
  return results

#querying data dictionary
def query_data_dict(query):
  #connect to database
  cnx = mysql.connector.connect(**config)
  cursor = cnx.cursor(dictionary=True)
  #excute query
  cursor.execute(query)
  results = cursor.fetchall()
  #close connection
  cursor.close()
  cnx.close()
  return results