import re
import requests
import praw
import os
from dotenv import load_dotenv
import time
from praw.models import Message
import pandas as pd
import re


load_dotenv()

REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_SECRET_ID = os.getenv('REDDIT_SECRET_ID')
REDDIT_USERNAME = os.getenv('REDDIT_USERNAME')
REDDIT_PASSWORD = os.getenv('REDDIT_PASSWORD')

REDDIT_CLIENT_ID = '###'
REDDIT_SECRET_ID = '###'
REDDIT_USERNAME = '###'
REDDIT_PASSWORD = '###'

reddit = praw.Reddit(client_id =REDDIT_CLIENT_ID,
                     client_secret =REDDIT_SECRET_ID,
                     user_agent ='my user agent',
                     username =REDDIT_USERNAME,
                     password =REDDIT_PASSWORD)

# There are 4 stages a user can be in the 'message flow': 
# 1. Initial outreach
# 2. Share idea
# 3. Share survey / offer
# 4. Thank them for taking survey
# This script will count the number of messages in our inbox we have received from the user, to determine which stage they are in
# This automatically generates the marketing data table we were manually maintaining
# TODO: Afterwards, it will flag the messages that need us to respond as 'unread', so that we can find / send easily

# Gather list of users already messaged
users_messaged_dict = {"Name":[],"Subreddit":[],"Number of Messages":[]}
for Message in reddit.inbox.sent(limit=10000):
    user_messaged_name = Message.dest
    user_messaged_body = Message.body
    # User's name has not been found yet, add new entry
    if user_messaged_name not in users_messaged_dict["Name"]:
        users_messaged_dict["Name"].append(user_messaged_name)
        user_index = users_messaged_dict["Name"].index(user_messaged_name)
        users_messaged_dict["Subreddit"].append("")
        position_subreddit = user_messaged_body.find("r/")
        if position_subreddit > -1:
            position_subreddit += 2
            subreddit_string = user_messaged_body[position_subreddit:len(user_messaged_body)]
            end_of_subreddit_index = re.search(r'\W+', subreddit_string).start()
            subreddit_string = subreddit_string[0 : end_of_subreddit_index]
            users_messaged_dict["Subreddit"][user_index] = subreddit_string
        users_messaged_dict["Number of Messages"].append(1)
    # User's name has been found, update entry
    else:
        user_index = users_messaged_dict["Name"].index(user_messaged_name)
        users_messaged_dict["Number of Messages"][user_index] += 1
        position_subreddit = user_messaged_body.find("r/")
        if position_subreddit > -1:
            position_subreddit += 2
            subreddit_string = user_messaged_body[position_subreddit:len(user_messaged_body)]
            end_of_subreddit_index = re.search(r'\W+', subreddit_string).start()
            subreddit_string = subreddit_string[0 : end_of_subreddit_index]
            users_messaged_dict["Subreddit"][user_index] = subreddit_string


marketing_data = pd.DataFrame.from_dict(users_messaged_dict)
marketing_data = pd.pivot_table(marketing_data, values='Number of Messages', index=['Subreddit'],
                    columns=['Number of Messages'], aggfunc='count')
# Ignore the subreddit row that is 'blank', this is likely from messages we sent prior to our standardized format
print(marketing_data)
