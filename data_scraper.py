import praw


# PERSONAL USE SCRIPT TOKEN
# 2AWi3DM-2NNfX0Gk5MJNEw

# SECRET TOKEN
# UU5MJTYvBbytbsaCNZRrnxOLb771cg

r = praw.Reddit(client_id='2AWi3DM-2NNfX0Gk5MJNEw',
                client_secret='UU5MJTYvBbytbsaCNZRrnxOLb771cg',
                user_agent='python:tone.evan.toppostscompiler:v0.1'
                           '(by /u/suff_r)')


def get_submissions(subreddit_name: str, time_period: str, num_posts: int, num_comments: int) -> dict:
    print("Fetching Reddit data...")
    for count, submission in enumerate(r.subreddit(subreddit_name).top(time_period, limit=num_posts)):
        # print(f"count: {count}, num_posts: {num_posts}")
        if count == num_posts - 1:
            print("Submission fetched.")
            sub = {
                "subreddit": submission.subreddit.display_name,
                "title": submission.title,
                "author": submission.author.name,
                "score": submission.score,
                "comments": []
            }
            submission.comment_sort = "top"
            submission.comment_limit = num_comments
            submission.comments.replace_more(limit=0)
            for comment in submission.comments:
                comment_dict = {
                    'body': comment.body,
                    'author': comment.author.name,
                    'score': comment.score
                }
                sub['comments'].append(comment_dict)
            return sub
