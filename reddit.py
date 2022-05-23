import praw

reddit = praw.Reddit(client_id ='<ENTER_CLIENT_ID>',
                     client_secret ='<ENTER_CLIENT_SECRET',
                     user_agent ='my user agent',
                     username ='<ENTER_USERNAME>',
                     password ='<ENTER_PASSWORD')

unique_user_set = set([])

#Grab and send message to 25 of the hottest posts and subsequent comments in searched subreddit
for submission in reddit.subreddit("<ENTER_SUBREDDIT>").hot(limit=25):
    # print(submission.author.name)
    unique_user_set.add(submission.author.name)
    for comment in submission.comments:
      try:
        print(comment.author.name)
        unique_user_set.add(comment.author.name)
      except:
        print("comment error")

#Send message to all users
for user in unique_user_set:
  try: 
    reddit.redditor(submission.author.name).message(subject= '<ENTER_A_TITLE>', message= '<ENTER_MESSAGE>')
  except: 
    print("error with user")