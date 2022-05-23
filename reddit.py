import requests
import praw
import os
from dotenv import load_dotenv

load_dotenv()

REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_SECRET_ID = os.getenv('REDDIT_SECRET_ID')
REDDIT_USERNAME = os.getenv('REDDIT_USERNAME')
REDDIT_PASSWORD = os.getenv('REDDIT_PASSWORD')

reddit = praw.Reddit(client_id =REDDIT_CLIENT_ID,
                     client_secret =REDDIT_SECRET_ID,
                     user_agent ='my user agent',
                     username =REDDIT_USERNAME,
                     password =REDDIT_PASSWORD)

#enter subreddits we want to message to
list_of_subreddits = set(['test', 'budgeting'])
user_subreddit_dic = {}

#Grab and send messages to post author and subsequent comments in searched subreddits
for subreddit in list_of_subreddits:
  unique_user_set = set([])
  # Different search filters available 
  # for submission in reddit.subreddit(subreddit).controversial(time_filter="month"):
  # for submission in reddit.subreddit(subreddit).top(time_filter="all", limit=25):
  for submission in reddit.subreddit(subreddit).hot(limit=25):
      try:
        unique_user_set.add(submission.author.name)
        for comment in submission.comments:
          try:
            unique_user_set.add(comment.author.name)
          except:
            print("handling comment object exception")
      except:
        print("handling submission object exception")      
  user_subreddit_dic.update({subreddit: unique_user_set})

# print(user_subreddit_dic)

# Send message to all users
for subreddit in list_of_subreddits:
  user_list = user_subreddit_dic[subreddit]
  for user in user_list:
    try: 
      reddit.redditor(user).message(subject= '<ENTER_A_TITLE>', message= '<ENTER_MESSAGE>')
      print("message successfully sent to " + user)
    except: 
      print("handling user object exception")