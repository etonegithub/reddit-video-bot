import requests

# PERSONAL USE SCRIPT TOKEN
# 2AWi3DM-2NNfX0Gk5MJNEw

# SECRET TOKEN
# UU5MJTYvBbytbsaCNZRrnxOLb771cg

##########################################

# Token is valid for 2 hours
# Last Token: 10/15 11:20am

TOKEN = "769069790649-CFEsBSzWX_Bifkdf40lwk34AS31YRw"
headers = {'User-Agent': 'TopPostsCompiler/0.0.1'}
headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}


##########################################

# auth = requests.auth.HTTPBasicAuth('2AWi3DM-2NNfX0Gk5MJNEw', 'UU5MJTYvBbytbsaCNZRrnxOLb771cg')
# data = {'grant_type': 'password',
#         'username': 'suff_r',
#         'password': '1849gold'}
# headers = {'User-Agent': 'TopPostsCompiler/0.0.1'}
# res = requests.post('https://www.reddit.com/api/v1/access_token',
#                     auth=auth, data=data, headers=headers)
# print(res.json())
# TOKEN = res.json()['access_token']
# headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

###############################################

resp = requests.get("https://oauth.reddit.com/r/AskReddit/top/?t=month",
                    headers=headers)

for post in resp.json()['data']['children']:
    print(post['data']['title'])


