import apiOperations
import DatabaseOperations
import urllib.request
import json
import datetime
import time
import urllib.error
from issue_info_extractor import issue_info_extract
import random


class comment_info_extract:
    def __init__(self):
        print("This was a construct")

    # Input: Api statement after GET part
    # Returned: A dictionary, as returned by the api
    def extractIssueApi(self, statement):
        url = "https://api.github.com/repos/" + statement
        try:
            response = urllib.request.urlopen(url)
        except urllib.error.HTTPError as e:
            print(e)
            if e.code == 403:
                time.sleep(3600)
                self.extractIssueApi(statement)
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

    def insertValue(self, comment, issueNum, issueId):
        comment['body'] = str.encode(comment['body'], 'ascii', 'ignore')
        if (comment['created_at'] is None) == False:
            comment['created_at'] = self.convertToDatetime(comment['created_at'])
        if (comment['updated_at'] is None) == False:
            comment['updated_at'] = self.convertToDatetime(comment['updated_at'])
        insert_val = (issueNum, comment['id'], comment['node_id'], comment['url'], comment['user']['id'],
                      comment['user']['login'],
                      comment['created_at'], comment['updated_at'], comment['body'], issueId)
        return insert_val

    def updateAllKeys(self, comment, issueNum, issueId):
        insert_stmt = ("UPDATE network_t.new_git_comments " 
                       "SET issue_number = %s, comment_id = %s, node_id = %s, url = %s, user_id = %s, "
                       "username = %s, created_at = %s, updated_at = %s, body = %s, issue_id = %s "
                       "WHERE comment_id = " + str(comment['id']))
        insert_val = self.insertValue(comment, issueNum, issueId)

        try:
            DatabaseOperations.insert_data(insert_stmt, insert_val)
            print("Successfully updated")
        except Exception as e:
            print(comment['id'])
            print(e)

    def insertComment(self, apiDict, issueNumber, issueId):
        # listOfCols = ["id", "number", "node_id", "url", "state", "assignee", "comments",
        #               "created_at", "updated_at", "closed_at", "html_url"]
        insert_stmt = ("INSERT INTO network_t.new_git_comments " +
                       "(issue_number, comment_id, node_id, url, user_id, username, created_at, updated_at,body, issue_id) "
                       "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

        insert_val = self.insertValue(apiDict, issueNumber, issueId)
        try:
            DatabaseOperations.insert_data(insert_stmt, insert_val)
            print("Successfully inserted")
        except Exception as e:
            print(insert_val[0])
            print(e)

    def insertToDatabase(self, comment, issueNumber, issueId):
        if self.searchCommentById(comment['id']) is None:
            try:
                self.insertComment(comment, issueNumber, issueId)
            except Exception as e:
                print(comment['id'])
                print(e)
        else:
            self.updateAllKeys(comment, issueNumber, issueId)


    def commentExtraction(self):
        query_stmt = "SELECT issue_number, issue_id FROM network_t.new_git_issues where project_id = 3228505"
        issueList = DatabaseOperations.query_data(query_stmt)
        i = 0
        for issue in issueList:
            issueNumber = issue[0]
            issueId = issue[1]
            i=i+1
            obj = issue_info_extract()
            fullName = obj.searchFullnameById(issueId)
            apiCall = fullName + "/issues/" + str(issueNumber) + "/comments?access_token=5fdf01ce251225484af8a2a5f604d34d1fa41509"
            commentsList = apiOperations.extractApis(apiCall)
            if commentsList is None:
                print(issueId)
            else:
                for comment in commentsList:
                    try:
                        self.insertToDatabase(comment, issueNumber, issueId)
                    except Exception as e:
                        print(issueNumber)
                        print(comment["id"])
                        print(e)

def getlist():
    query_stmt = "SELECT id FROM network_t.new_git_comments where issue_id in (Select issue_id from network_t.new_git_issues  where project_id=3228505) and is_question=1"
    lst = DatabaseOperations.query_data(query_stmt)
    rand_lst = random.sample(lst, 100)
    print(rand_lst)
    return 0
x = comment_info_extract()
x.commentExtraction()
