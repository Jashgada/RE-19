import json #Just used to pretty print
import  DatabaseOperations
# from nltk.tag.stanford import StanfordPOSTagger
# from nltk.tag import StanfordNERTagger
from nltk.parse.stanford import StanfordParser
# from nltk.parse.stanford import StanfordDependencyParser
from nltk import tree
from nltk import sent_tokenize
import nltk
import string
import nltk
from nltk import word_tokenize
import re
import os
os.environ["CLASSPATH"] = 'D:\\A College\\Semester III\\Python Programming 93A\\Final Project\\stanford-parser-full-2018-10-17'
java_path = "C:\\Program Files\\Java\\jdk-13.0.1\\bin\\java.exe"
os.environ['JAVAHOME'] = java_path


def questionIdentification(parsedString):
    if bool(re.search(r'\bSQ\b|\b\SBARQ\b',parsedString)) == True:
        return '1'
    return '0'

def parseComment(comment):
    parser = StanfordParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
    sentenceList = sent_tokenize(comment['body'])
    try:
        parsedList = list(parser.raw_parse_sents(sentenceList))
    except:
        print("Could not parse comment", end=' ')
        print(comment['comment_id'])
    else:
        parsedstring = ''.join([' '.join([str(c) for c in lst]) for lst in parsedList])
        isQuest = questionIdentification(parsedstring)
        return isQuest

def insertToTable(comment, isQuestion):
    insertStmt = ("UPDATE new_git_comments SET is_question = %s WHERE comment_id = %s")
    insertVal = (isQuestion, comment['comment_id'])
    try:
        DatabaseOperations.insert_data(insertStmt, insertVal)
    except Exception as e:
        print(comment['comment_id`'])
        print(e)


def queryComments():
    commentsList = DatabaseOperations.query_data_dict("Select * FROM new_git_comments where id>=209976")
    for comment in commentsList:
        isQuestion = parseComment(comment)
        insertToTable(comment, isQuestion)

queryComments()
