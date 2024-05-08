import sys      
import socket
import json
import random
import processor
import dataupdate
import string
from getmac import get_mac_address as gma
from pymongo import MongoClient
from colorama import Fore
from datetime import datetime, date
import smtplib
import os
import ssl
from email.message import EmailMessage
# Add SSL

import ssl
context = ssl.create_default_context()

#LOADING CREDENTIALS
with open('config.json', 'r') as f:
    config = json.load(f)

email_sender = config['email_sender']
email_password = config['email_password']
mongo_cluster = config['mongo_cluster']
huid_config = config['huid_config']


em = EmailMessage()
em['From'] = email_sender
client = MongoClient(mongo_cluster)
db = client['Licenseverification']
license_collection = db['License']
log_collection = db['logs']

#LOGS CREATE -

# Function to log user action
def log_action(action):
    huid_public,ip_public,license_key,power,username=processor.license_details()
    log_entry = {
        "username": username,
        "license_key": license_key,
        "action": action,
        "power": power,
        "huid": huid_public,
        "ip-public" : ip_public,
        "timestamp": datetime.now()
    }
    log_collection.insert_one(log_entry)

# Main code
def log_update(action, power):
    log_action(action)
    
    folder_path = "./user_logs/"

    if huid_config == gma():
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        file_path = os.path.join(folder_path, "user_logs.log")

        with open(file_path, "w") as f:
            for log_entry in log_collection.find():
                log_str = f"""At - {log_entry['timestamp']}
                username - {log_entry['username']} 
                license - ({log_entry['license_key']})
                action - {log_entry['action']}
                power - {power} \n"""
                f.write(log_str)
    else:
        pass
