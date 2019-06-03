import apiOperations
import DatabaseOperations
import urllib.request
import json
import datetime



class issue_info_extract:
    def __init__(self):
        print("This was a construct")

    # Input: Api statement after GET part
    # Returned: A dictionary, as returned by the api
    def extractIssueApis(self, statement):
        url = "https://api.github.com/repos/" + statement
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())
        return data

    def convertToDatetime(self, str):
        time = datetime.datetime.strptime(str[:-1], '%Y-%m-%dT%H:%M:%S')
        return time

    def searchIssueById(self, idNum):
        query = "SELECT * FROM new_git_issues WHERE issue_id='" + str(idNum) + "'"
        projectInfo = DatabaseOperations.query_data_dict(query)
        if len(projectInfo) == 0:
            return None
        else:
            return projectInfo[0]


    def searchByKey(self,key,val):
        query = "SELECT * FROM new_git_issues WHERE "+ str(key) + "='" + str(val) + "'"
        projectInfo = DatabaseOperations.query_data_dict(query)
        if len(projectInfo) == 0:
            return None
        else:
            return projectInfo[0]



    def updateIssueByKey(self, issue_id, key, value):
        update_issue = ("UPDATE new_git_issues SET " + key + "= %s WHERE issue_id=%s")
        data_issue = (value, issue_id)
        try:
            DatabaseOperations.insert_data(update_issue, data_issue)
        except Exception as e:
            print(issue_id)
            print(e)
        return

    # Input Paramters: A dictionary, a list
    # Returned Value: A dictionary with only the values needed to store to database as per the input list
    # def refineApiData(self, apiDict, tableCols):
    #     fin_dict = {}
    #     if type(apiDict) is dict:
    #         for key,val in apiDict.items():
    #             if type(val) is dict:
    #                 if key == "user":
    #                     fin_dict["user_id"] = val["id"]
    #                     fin_dict["username"] = val["login"]
    #                 elif key == "assignee" and ((val is None) == False):
    #                     fin_dict["assignee"] = val["login"]
    #                     fin_dict.update(self.refineApiData(val, tableCols))
    #             else:
    #                 if key == 'body':
    #                     fin_dict['body'] = str.encode(val, 'ascii', 'ignore')
    #                     tableCols.remove(key)
    #                     # print(type(fin_dict['body']))
    #                 elif key == 'title':
    #                     fin_dict['title'] = str.encode(val, 'ascii', 'ignore')
    #                     tableCols.remove(key)
    #                 elif key in tableCols:
    #                     fin_dict[key] = val
    #                     tableCols.remove(key)
    #     return fin_dict

    def insertValue(self, issue, projectId):
        issue['body'] = str.encode(issue['body'], 'ascii', 'ignore')
        issue['title'] = str.encode(issue['title'], 'ascii', 'ignore')
        if (issue['created_at'] is None) == False:
            issue['created_at'] = self.convertToDatetime(issue['created_at'])
        if (issue['updated_at'] is None) == False:
            issue['updated_at'] = self.convertToDatetime(issue['updated_at'])
        if (issue['closed_at'] is None) == False:
            issue['closed_at'] = self.convertToDatetime(issue['closed_at'])
        try:
            insert_val = (projectId, issue['id'], issue['number'], issue['node_id'], issue['url'], issue['user']['id'],
                          issue['user']['login'], issue["title"], issue['state'], issue['assignee']['login'],
                          issue['comments'],
                          issue['created_at'], issue['updated_at'], issue['closed_at'], issue['body'],
                          issue['html_url'])
        except:
            insert_val = (projectId, issue['id'], issue['number'], issue['node_id'], issue['url'], issue['user']['id'],
                          issue['user']['login'], issue["title"], issue['state'], issue['assignee'],
                          issue['comments'],
                          issue['created_at'], issue['updated_at'], issue['closed_at'], issue['body'],
                          issue['html_url'])
        return insert_val


    def updateAllKeys(self, issue, projectId):
        insert_stmt = ("UPDATE network_t.new_git_issues " 
                       "SET project_id = %s, issue_id = %s, issue_number = %s, node_id = %s, url = %s, user_id = %s, "
                       "username = %s," 
                       "title = %s, state = %s, assignee = %s, comments = %s, created_at = %s, updated_at = %s, "
                       "closed_at = %s, body = %s, website = %s "
                       "WHERE issue_id = " + str(issue['id']))
        insert_val = self.insertValue(issue, projectId)

        try:
            DatabaseOperations.insert_data(insert_stmt, insert_val)
        except Exception as e:
            print(issue['id'])
            print(e)


    def insertIssue(self, apiDict, projectId):
        # listOfCols = ["id", "number", "node_id", "url", "state", "assignee", "comments",
        #               "created_at", "updated_at", "closed_at", "html_url"]
        insert_stmt = ("INSERT INTO network_t.new_git_issues " +
                       "(project_id, issue_id, issue_number, node_id, url, user_id, username," +
                       "title, state, assignee, comments, created_at, updated_at, closed_at," +
                       "body, website) "
                       "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

        insert_val = self.insertValue(apiDict, projectId)
        try:
            DatabaseOperations.insert_data(insert_stmt, insert_val)
        except Exception as e:
            print(insert_val[0])
            print(e)

    def insertToDatabase(self, issue, project_id):
        if self.searchIssueById(issue['id']) is None:
            try:
                self.insertIssue(issue, project_id)
            except Exception as e:
                print(issue['id'])
                print(e)
        else:
            self.updateAllKeys(issue, project_id)


    def IssueExtraction(self, owner, repo):
         i = 0
         while i<10:
             apiCall = owner + "/" + repo + "/issues?" + "page=" + str(i) + "&state=all"
             projectApi = owner + "/" + repo
             projectDict = self.extractIssueApis(projectApi)
             projectId = projectDict["id"]
             issueList = self.extractIssueApis(apiCall)
             if len(issueList) != 0:
                 for issue in issueList:
                     if ("pull_request" in issue) == False:
                        self.insertToDatabase(issue, projectId)
             else:
                 print("Reached the end of the issues")
                 break
             i = i + 1


x = issue_info_extract()
x.IssueExtraction("atom","atom")
# x.IssueExtraction("atom","atom")
# abcd = x.extractIssueApi("atom/atom/issues/19366")
# a = abcd['body']
# print(a)
# print(type(a))
# b = apiOperations.ignoreUnicode(a)
# print(type(b))
# print(b)
# c = b.encode('utf-8')
# print(type(c))
# print(c)
# dt = abcd['created_at']
# time = datetime.datetime.strptime(dt[:-1], '%Y-%m-%dT%H:%M:%S')
