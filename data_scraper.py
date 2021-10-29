import praw


# PERSONAL USE SCRIPT TOKEN
# 2AWi3DM-2NNfX0Gk5MJNEw

# SECRET TOKEN
# UU5MJTYvBbytbsaCNZRrnxOLb771cg

r = praw.Reddit(client_id='2AWi3DM-2NNfX0Gk5MJNEw',
                client_secret='UU5MJTYvBbytbsaCNZRrnxOLb771cg',
                user_agent='python:tone.evan.toppostscompiler:v0.1'
                '(by /u/suff_r)')


def get_submission():
    print("QUESTION")
    for submission in r.subreddit("askreddit").top("week", limit=1):
        print("||||||||||||||||||||||||")
        print(submission.title)
        sub = {
            "title": submission.title,
            "comments": []
        }
        print("===================")
        submission.comment_sort = "top"
        submission.comment_limit = 5
        submission.comments.replace_more(limit=0)
        for comment in submission.comments:
            print(comment.body)
            print("----------")
            sub['comments'].append(comment.body)
        return sub

