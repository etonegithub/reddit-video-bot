import praw
from pymongo import MongoClient

client = MongoClient("mongodb+srv://admin:<password>@reddit-video-data.qaodr.mongodb.net/"
                     "myFirstDatabase?retryWrites=true&w=majority")


# PERSONAL USE SCRIPT TOKEN
# 2AWi3DM-2NNfX0Gk5MJNEw

# SECRET TOKEN
# UU5MJTYvBbytbsaCNZRrnxOLb771cg

r = praw.Reddit(client_id='2AWi3DM-2NNfX0Gk5MJNEw',
                client_secret='UU5MJTYvBbytbsaCNZRrnxOLb771cg',
                user_agent='python:tone.evan.toppostscompiler:v0.1'
                '(by /u/suff_r)')

print("QUESTION")
for submission in r.subreddit("askreddit").top("week", limit=2):
    print("||||||||||||||||||||||||")
    print(submission.title)
    print("===================")
    submission.comment_sort = "top"
    submission.comments.replace_more(limit=0)
    for comment in submission.comments:
        print(comment.body)
        print("----------")

