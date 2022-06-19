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
# This script will count the number of messages in our inbox we have received from the user, to determine which stage they are in
# This automatically generates the marketing data table we were manually maintaining
# TODO: Afterwards, it will flag the messages that need us to respond as 'unread', so that we can find / send easily

def add_message_count(message_body, input_dict, input_index):
    # First message
    position_subreddit = message_body.find("r/")
    if position_subreddit > -1:
        position_subreddit += 2
        subreddit_string = user_messaged_body[position_subreddit:len(user_messaged_body)]
        end_of_subreddit_index = re.search(r'\W+', subreddit_string).start()
        subreddit_string = subreddit_string[0 : end_of_subreddit_index]
        input_dict["Subreddit"][input_index] = subreddit_string
        input_dict["Number of Messages"][input_index] = max(input_dict["Number of Messages"][input_index], 1)
    # Second message
    position_subreddit = message_body.find("https://www.youtube.com/watch?v=Pz75Qp2s0LQ")
    if position_subreddit > -1:
        input_dict["Number of Messages"][input_index] = max(input_dict["Number of Messages"][input_index], 2)
    # Third message
    position_subreddit = message_body.find("t.maze.co")
    if position_subreddit > -1:
        input_dict["Number of Messages"][input_index] = max(input_dict["Number of Messages"][input_index], 3)


# Gather list of users already messaged, ignore messages sent before we aligned on short intro blurb
users_messaged_dict = {"Name":[],"Subreddit":[],"Number of Messages":[]}
for Message in reddit.inbox.sent(limit=None):
    user_messaged_name = Message.dest
    user_messaged_body = Message.body
    if Message.created_utc < 1655070865:
        continue
    users_messaged_dict["Name"].append(user_messaged_name)
    user_index = users_messaged_dict["Name"].index(user_messaged_name)
    users_messaged_dict["Subreddit"].append("")
    users_messaged_dict["Number of Messages"].append(0)
    add_message_count(user_messaged_body, users_messaged_dict, user_index)


marketing_data = pd.DataFrame.from_dict(users_messaged_dict)
marketing_data = pd.pivot_table(marketing_data, values='Number of Messages', index=['Subreddit'],
                    columns=['Number of Messages'], aggfunc='count').fillna(0)
del marketing_data[0]
marketing_data = marketing_data.drop('')
marketing_data['% of 1'] = marketing_data[1].astype(float)
marketing_data['% of 2'] = marketing_data[2].astype(float)
marketing_data['% of 3'] = marketing_data[3].astype(float)
marketing_data['% of 1'] = ((marketing_data[1] / marketing_data[1]) * 100).astype(int)
marketing_data['% of 2'] = ((marketing_data[2] / marketing_data[1]) * 100).astype(int)
marketing_data['% of 3'] = ((marketing_data[3] / marketing_data[1]) * 100).astype(int)
print(marketing_data)