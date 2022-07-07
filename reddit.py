import requests
import praw
import os
from dotenv import load_dotenv
import time
from praw.models import Message


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
list_of_subreddits = set(['whatcarshouldIbuy'])
user_subreddit_dic = {}

# Gather list of users already messaged
users_messaged = []
for Message in reddit.inbox.sent(limit=10000):
  users_messaged.append(Message.dest)

# Grab and send messages to post author and subsequent comments in searched subreddits
# Do not send message to any users already messaged
for subreddit in list_of_subreddits:
  unique_user_set = set([])
  # Different search filters available 
  for submission in reddit.subreddit(subreddit).new(limit=100):
  # for submission in reddit.subreddit(subreddit).controversial(time_filter="week"):
  # for submission in reddit.subreddit(subreddit).top(time_filter="all", limit=25):
  # for submission in reddit.subreddit(subreddit).hot(limit=25):
    try:
      if submission.author.name not in users_messaged:
          try:
            unique_user_set.add(submission.author.name)
            for comment in submission.comments:
              try:
                unique_user_set.add(comment.author.name)
              except Exception as e:
                print("handling comment object exception")
                print(e)
          except Exception as e:
            print("handling submission object exception")      
            print(e)
      user_subreddit_dic.update({subreddit: unique_user_set})
    except Exception as e:  
      print("name error")    
print(user_subreddit_dic)

# TODO: Rate limit handling--> add timer to pause sending messages
def rateLimitHandling():
  # print("Pausing for 5 mins")
  # time.sleep(60)
  print("Pausing for 4 mins")
  time.sleep(60)
  print("Pausing for 3 mins")
  time.sleep(60)
  print("Pausing for 2 mins")
  time.sleep(60)
  print("Pausing for 1 mins")
  time.sleep(60)
  print("Done")

# Send message to all users
for subreddit in list_of_subreddits:
  numOfMessages = 0
  user_list = user_subreddit_dic[subreddit]
  for user in user_list:
    try:
      if (numOfMessages == 75) :
        break
      print(numOfMessages)
      message= (f"Hey {user} hope you are well! I'm a recent college grad / aspiring entrepreneur,"
      f" it's great to meet you! I saw you were in r/{subreddit} so i figured i would reach out!"
      "My savings goals are being impacted by inflation and current budgeting solutions are not meeting my needs. " 
      "I feel with your participation, we can build a new budgeting solution together. "
      "Im building a subreddit dedicated to creating a new budgeting product to help us meet our savings goals. "
      "Feel free to share what your struggling with or any potential ideas you may have to offer! "
      "r/OkaneApp here is the sub")

      # message= (f"Hey, {user} hope you are well! I’m a recent college grad / aspiring entrepreneur on r/{subreddit}." 
      # " I'm building a budgeting chrome extension (similar to honey, except we show you your personal finances instead"  
      # " of coupons, so you can make informed shopping decisions). I made it because I have a ton of anxiety buying stuff lmao," 
      # " I’m still not used to having a salary compared to being broke in college. "  
      # " We have a user testing experiment out right now; do you mind checking it out and lmk what you think of our idea?" 
      # f" We are actively building it rn and would love feedback. You can find it here: https://t.maze.co/92145647?reddituser={user}&subreddit={subreddit} "
      # " I also recognize that I could seem scammy sending you a link; Maze is a trusted industry survey tool used by huge companies like Uber."
      # " Our survey is vetted and hosted entirely by them, you can see their website here: https://maze.co/ " 
      # " Thanks again!")
      title = "Building a community to create a new budgeting solution!"
      reddit.redditor(user).message(subject= title, message= message)
      rateLimitHandling()
      print("message successfully sent to " + user)
      numOfMessages += 1
    except Exception as e:
      print("handling user object exception: ")
      print(e)