import urllib.request
import json
import DatabaseOperations
import mysql.connector
# change config information before you use it

config = {
  'user': 'root',
  'password': '',
  'host': 'localhost',
  'database': 'network_t',
  'raise_on_warnings': True
}
def fn(owner,repo):
    get = "https://api.github.com/"
    url = get + "repos/" + owner + "/" + repo
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    database = json.dumps(data)
    print(database)
    table = {}
    table["id"] = data["id"]
    print(data["id"])
    return data

def trialDatabase():
        #name = name.replace("'", "''")
        query = "SELECT * FROM jira_user"
        user = DatabaseOperations.query_data_dict(query)
        # return the first search result
        if (len(user) == 0):
            return None
        return user

# Input Parameters: Name of the table (str), a List of Columns
# Return: No returned value
# Note: This function creates rows in SQL, and hence shall be only used once for each Table
def addColumnsToTable(table,column):
    stmt = "Alter table {} add column {} varchar(255)"
    stmt = stmt.format(table, column)
    # connect to database
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    # insert data
    cursor.execute(stmt)
    cnx.commit()
    # close connection
    cursor.close()
    cnx.close()
def fillColumns():
    col = ["id", "name", "fullname", "owner", "url", "created", "updated", "description", "size", "language", "default_branch",
           "clone_url", "issue_event_url", "branches_url", "small_url"]
    for columns in col:
        addColumnsToTable("new_git_project_info", columns)
def fillColsWithValue():
    col = ["id", "name", "fullname", "owner", "url", "created", "updated", "description", "size", "language",
           "default_branch", "clone_url", "issue_event_url", "branches_url", "small_url"]

def ignoreUnicode(unicodeString):
    # Replaces unicode characters with ?
    if unicodeString is None:
        return ''
    if isinstance(unicodeString, int):
        return unicodeString
    return unicodeString.encode('ascii', 'replace')
def extractApis(statement):
    url = "https://api.github.com/repos/" + statement
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    return data