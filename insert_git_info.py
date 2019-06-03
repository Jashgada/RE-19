import apiOperations
import mysql.connector
import DatabaseOperations
from mysql.connector import errorcode
import urllib.request
import json

#change config information before you use it

config = {
  'user': 'root',
  'password': '',
  'host': 'localhost',
  'database': 'network_t',
  'raise_on_warnings': True
}


class git_info_extraction:
    def __init__(self):
        print("This is a constructor")

    # Input Paramters: A dictionary, a list
    # Returned Value: A dictionary with only the values needed to store to database
    def refineApiData(self, apiDict, tableCols):
      fin_dict = {}
      if type(apiDict) is dict:
        for key,val in apiDict.items():
            if type(val) is dict:
                fin_dict.update(self.refineApiData(val, tableCols))
            else:
                if key in tableCols:
                    fin_dict[key] = val
                    tableCols.remove(key)
        print("Hopefully Successful")

      return fin_dict

    # Input parameters: Project Owner, Repository name
    # Returned: Dictionary with all data in api
    def extractRepoInfo(self, owner, repo):
        url = "https://api.github.com/repos/" + owner + "/" + repo
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())
        return data

    def insertToDatabse(self, owner, repo):
        data = self.extractRepoInfo(owner, repo)
        col = ["id", "name","login", "full_name", "url", "created_at", "updated_at", "description", "size", "language",
               "default_branch", "clone_url", "issue_events_url", "branches_url", "small_url"]
        info = self.refineApiData(data, col)
        insert_stmt = ("INSERT INTO network_t.new_git_project_info "
                       "(ProjectId, name, login, full_name, url, created, updated, description, size, language, "
                       "default_branch, clone_url, issue_events_url, branches_url)"
                       "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        insert_val = (info['id'], info['name'], info['login'], info['full_name'], info['url'], info['created_at'],
                      info['updated_at'], info['description'], info['size'], info['language'], info['default_branch'],
                      info['clone_url'], info['issue_events_url'], info['branches_url'])
        DatabaseOperations.insert_data(insert_stmt, insert_val)

    # input parameter: name of the repository
    # Returned: the project Id
    def getProjectId(self, repo_name):
        query = "SELECT * FROM new_git_project_info WHERE name='"+repo_name+"'"
        projectInfo = DatabaseOperations.query_data(query)
        if len(projectInfo) == 0:
            return None
        else:
            return projectInfo[0][1]

    # Input Parameters: repository name
    # Returned: Project Information
    def searchByName(self, repo_name):
        query = "SELECT * FROM new_git_project_info WHERE name='" + repo_name + "'"
        projectInfo = DatabaseOperations.query_data_dict(query)
        if len(projectInfo) == 0:
            return None
        else:
            return projectInfo[0]

    # Input Parameters: Id of the Project
    # Returned: Project Information
    def searchById(self, idNum):
        query = "SELECT * FROM new_git_project_info WHERE project_id='" + str(idNum) + "'"
        projectInfo = DatabaseOperations.query_data_dict(query)
        if len(projectInfo) == 0:
            return None
        else:
            return projectInfo[0]

x = git_info_extraction()
# print(x.getProjectId("ato"))
print(x.searchById(322850))






# INSERT INTO SQL FUNCTION
                # print("Key iterating")
                # print(key)
                # print("  ")
                # print(val)
                # print('\n')
                # try:
                # #connect to database
                #     cnx = mysql.connector.connect(**config)
                #     conn = cnx.cursor()
                #     x = str(key)
                #     y = str(val)
                #     # insert data
                #     sql = f"""INSERT INTO network_t.new_git_project_info ({x}) VALUES ('"{y}"')"""
                #     print(sql)
                #     conn.execute(sql)
                #     cnx.commit()
                #     # close connection
                #     conn.close()
                #     cnx.close()
                # except Exception as e:
                #     print(e)
                # # DELETE FROM LIST
                # tableCols.remove(key)