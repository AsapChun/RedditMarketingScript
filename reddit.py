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

list_of_subreddits = set(['test', 'budgeting'])
user_subreddit_dic = {}

#Grab and send messages to 25 of the hottest posts and subsequent comments in searched subreddit
for subreddit in list_of_subreddits:
  unique_user_set = set([])
  for submission in reddit.subreddit(subreddit).hot(limit=25):
      # print(submission.author.name)
      unique_user_set.add(submission.author.name)
      for comment in submission.comments:
        try:
          unique_user_set.add(comment.author.name)
        except:
          print("handling comment object exception")
  user_subreddit_dic.update({subreddit: unique_user_set})

# print(user_subreddit_dic)

#Send message to all users
for subreddit in list_of_subreddits:
  user_list = user_subreddit_dic[subreddit]
  print(user_list)
  for user in user_list:
    try: 
      reddit.redditor(submission.author.name).message(subject= '<ENTER_A_TITLE>', message= '<ENTER_MESSAGE>')
    except: 
      print("handling comment object exception")