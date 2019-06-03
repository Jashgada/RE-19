import apiOperations
import DatabaseOperations
import urllib.request
import json
import datetime



class comment_info_extract:
    def __init__(self):
        print("This was a construct")

    # Input: Api statement after GET part
    # Returned: A dictionary, as returned by the api
    def extractIssueApi(self, statement):
        url = "https://api.github.com/repos/" + statement
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())
        return data

    def convertToDatetime(self, str):
        time = datetime.datetime.strptime(str[:-1], '%Y-%m-%dT%H:%M:%S')
        return time

    def searchByKey(self,key , val):
        query = "SELECT * FROM new_git_comments WHERE "+ str(key) + "='" + str(val) + "'"
        commentInfo = DatabaseOperations.query_data_dict(query)
        if len(commentInfo) == 0:
            return None
        else:
            return commentInfo[0]

    def searchCommentById(self, idNum):
        query = "SELECT * FROM new_git_comments WHERE comment_id='" + str(idNum) + "'"
        commentInfo = DatabaseOperations.query_data_dict(query)
        if len(commentInfo) == 0:
            return None
        else:
            return commentInfo[0]

    def insertValue(self, comment, issueId):
        comment['body'] = str.encode(comment['body'], 'ascii', 'ignore')
        if (comment['created_at'] is None) == False:
            comment['created_at'] = self.convertToDatetime(comment['created_at'])
        if (comment['updated_at'] is None) == False:
            comment['updated_at'] = self.convertToDatetime(comment['updated_at'])
        insert_val = (issueId, comment['id'], comment['node_id'], comment['url'], comment['user']['id'],
                      comment['user']['login'],
                      comment['created_at'], comment['updated_at'], comment['body'])
        return insert_val

    def updateAllKeys(self, comment, issueId):
        insert_stmt = ("UPDATE network_t.new_git_comments " 
                       "SET issue_number = %s, comment_id = %s, node_id = %s, url = %s, user_id = %s, "
                       "username = %s, created_at = %s, updated_at = %s, body = %s "
                       "WHERE comment_id = " + str(comment['id']))
        insert_val = self.insertValue(comment, issueId)

        try:
            DatabaseOperations.insert_data(insert_stmt, insert_val)
        except Exception as e:
            print(comment['id'])
            print(e)

    def insertComment(self, apiDict, issueNumber):
        # listOfCols = ["id", "number", "node_id", "url", "state", "assignee", "comments",
        #               "created_at", "updated_at", "closed_at", "html_url"]
        insert_stmt = ("INSERT INTO network_t.new_git_comments " +
                       "(issue_number, comment_id, node_id, url, user_id, username, created_at, updated_at,body) "
                       "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")

        insert_val = self.insertValue(apiDict, issueNumber)
        try:
            DatabaseOperations.insert_data(insert_stmt, insert_val)
        except Exception as e:
            print(insert_val[0])
            print(e)

    def insertToDatabase(self, comment, issueNumber):
        if self.searchCommentById(comment['id']) is None:
            try:
                self.insertComment(comment, issueNumber)
            except Exception as e:
                print(comment['id'])
                print(e)
        else:
            self.updateAllKeys(comment, issueNumber)


    def commentExtraction(self):
        query_stmt = "SELECT (issue_number) FROM network_t.new_git_issues"
        issueList = DatabaseOperations.query_data(query_stmt)
        i = 0
        for issue in issueList:
            if i >10:
                break
            issueNumber = issue[0]
            i=i+1
            # NOTE: YOU WILL HAVE TO ADD THE ACCESS TOKEN IN THE NEXT LINE
            apiCall = "atom" + "/" + "atom" + "/issues/"+ str(issueNumber)+ "/comments?access_token= git_access_token"
            commentsList = apiOperations.extractApis(apiCall)
            for comment in commentsList:
                try:
                    self.insertToDatabase(comment, issueNumber)
                except Exception as e:
                    print(issueNumber)
                    print(comment["id"])
                    print(e)


x = comment_info_extract()
x.commentExtraction()
# x = "SELECT (issue_id) FROM network_t.new_git_issues"
# y = DatabaseOperations.query_data(x)
# print(y)
# print(type(y[0][0]))
