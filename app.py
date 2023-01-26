'''
Created on

Course work:

@author: TactBOT 2.0 Team

Source:

'''

# Import necessary modules

import os
from typing import final
from dotenv import load_dotenv
from slack_sdk import WebClient
from flask import *
from slackeventsapi import SlackEventAdapter
from datetime import datetime
from pymongo import MongoClient
import pymongo
import pymongo.errors as pymon_err
from datetime import date
from datetime import timedelta
import requests
import pytz
import comedy as cmd
from pprint import pprint

load_dotenv()

mongo_uri = os.environ['MONGO_URI']

PORT = 9000

SLACK_APP_TOKEN = os.environ['SLACK_APP_TOKEN']

DB_NAME = 'time-bot'

COLLECTION_NAME = 'time-bot-data'

client = MongoClient(mongo_uri)

database = client[DB_NAME]

t12_van = database[COLLECTION_NAME]

SLACK_TOKEN = os.environ["SLACK_BOT_TOKEN"]

SIGNING_SECRET = os.environ["SIGNING_SECRET"]

app = Flask(__name__)

slack_events_adapter = SlackEventAdapter(SIGNING_SECRET, "/slack/events", app)

client = WebClient(token=SLACK_TOKEN)

BOT_ID = client.api_call("auth.test")['user_id']

@app.route("/")
def hello():

    return "Hello there! "

@slack_events_adapter.on('message')
def message(payload):

    pprint(payload)

    event = payload.get('event', {})

    channel_id = event.get('channel')

    user_id = event.get('user')

    text = event.get('text')

    if text == 'timings' or text == 'Timings':

        send(channel_id)

        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

    result = client.users_info(
        user=user_id
    )

    user_name = result['user']['real_name']

    if user_id != BOT_ID:

        try:

            is_comedy = cmd.check_if_comedy(text)

            if is_comedy:

                punchline = cmd.execute_comedy(text)

                client.chat_postMessage(channel = channel_id, text = punchline)

            else:
                
                did_update = process_and_update(text, user_name)

                if did_update:

                    client.chat_postMessage(channel = channel_id, text = f"Rejoin Info for {user_name} Noted")

        except:

            client.chat_postMessage(channel = 'test-channel', text = f"Datetime : {datetime.now()} some error : {payload} ")

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

def check_if_rejoin(text):

    if 'rejoin' in text:

        return 1

    return 0

def get_current_indian_date():

    india = pytz.timezone('asia/kolkata')
    today = datetime.now(tz=india).replace(microsecond=0, second=0, minute=0, hour=0)

    return today

def process_and_update(text, user_name):

    text = str(text).lower()

    is_rejoin = check_if_rejoin(text)

    if not is_rejoin:

        return 0

    text = text.replace('\n',' ')

    text_list = text.split('rejoin')

    required_data = text_list[-1]

    required_data = required_data.replace("```"," ")

    required_data = required_data.replace(":"," ")

    current_date = get_current_indian_date()

    data = {
        "updated_at"    : current_date,
        "rejoin_time"   : required_data,
        "user_name"     : user_name
    }

    t12_van.insert_one(data)

    return 1

@app.route("/send-data")
def send(channel_id = "test-channel"):

    current_date = get_current_indian_date()

    yesterday_date = current_date - timedelta(days = 1)

    required_data = list(t12_van.find({"updated_at" : {"$in" : [yesterday_date,current_date]}},{"rejoin_time" : 1 , "user_name" : 1 , "_id" : 0}))

    final_text = " "

    for user in required_data:

        final_text += f"{user['user_name']}:{user['rejoin_time']} \n"

    if final_text == " ":

        client.chat_postMessage(channel = channel_id, text = "No Data Available")

        return "No Data"

    final_text_list = final_text.split('\n')

    result = []

    [result.append(x) for x in final_text_list if x not in result]

    final_text = " "

    for res in result:

        final_text += f"{res} \n"

    client.chat_postMessage(channel = channel_id, text = final_text)

    return jsonify(final_text)

if __name__ == '__main__':

    app.run(debug = True, host = "0.0.0.0", port = PORT)

