# processor.py

import socket
import random
import string
from getmac import get_mac_address as gma
from pymongo import MongoClient
from colorama import Fore
from datetime import datetime, date
# Database credentials and defined
cluster = "mongodb+srv://xavierlol:01632987@cluster0.usjq3sl.mongodb.net/LOGINDATA?retryWrites=true&w=majority"
client = MongoClient(cluster)
db = client['Licenseverification']
license_collection = db['License']
connection_true=Fore.YELLOW+" CONNECTION TO DATABASE SUCCESSFUL "
connection_try=Fore.YELLOW+" CONNECTING TO DATABASE  "
connection_false=Fore.YELLOW+" CONNECTION TO DATABASE UNSUCCESSFUL "
exit=Fore.RED+"press enter to exit "
# Global variables
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
huid = gma()

def check_db():
    print(connection_try)
    start_time = datetime.now()
    try:
        client.server_info()  # This will throw an exception if connection fails
        print(connection_true)
        end_time = datetime.now()
        connection_time = (end_time - start_time).total_seconds() * 1000  # Calculate connection time in milliseconds
        print(f"Time taken to establish connection: {connection_time:.2f} milliseconds")
        # Additional security checks
        print(f"Hostname: {hostname}")
        print(f"IP Address: {ip_address}")
        return True
    except Exception as e:
        print(f"{connection_false} {str(e)}")
        return False


def generate_password_string(length=10):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))




def license_verification():
    try:
        for x in license_collection.find({"huid": huid, "ip": ip_address}, {'_id': 0}):
            a = "NONE"
            b = "NONE"
            c = "NONE"
            for key, value in x.items():
                if 'huid' in key:
                    a = value
                elif 'ip' in key:
                    b = value
                elif 'password' in key:
                    c = value
           
            return a, b, c
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None, None



def license_create(licensename):
    # Find the document with the highest ID
   highest_id_doc = license_collection.find_one({}, sort=[("_id", -1)])
   auto_password_generated = generate_password_string()
# Check if a document with the highest ID exists
   if highest_id_doc:
       
    #CREATING LICENSE WITH ID >=1
    highest_id = highest_id_doc["_id"]
    highest_id=int(highest_id) + 1
    license_information = {
        '_id': highest_id,
        "authorized":"Human",
        "username":"NONE",
        "email_address": "NONE",
        "license": licensename,
        "password": auto_password_generated,
        "ip": "NONE",
        "huid": "NONE",
        "validity": "True",
        "power" : "user",
        "isbanned":"False",
        "Creation_Time": datetime.now()
    }
    create = license_collection.insert_one(license_information)
    print('License created')
    
   #CREATING LICENSE WITH ID 0 
   else:
    highest_id = 0
    print("Creating new license...")
    license_information = {
        '_id': highest_id,
        "authorized":"Human",
        "username":"NONE",
        "email_address": "NONE",
        "license": licensename,
        "password": auto_password_generated,
        "ip": "NONE",
        "huid": "NONE",
        "validity": "True",
        "power" : "user",
        "isbanned":"False",
        "Creation_Time": datetime.now()
    }
    create = license_collection.insert_one(license_information)
    print('License created')
def otp_verification(system_generated,user_entered):
    if system_generated==user_entered:
        return True
    else:
        print(f'Invalid otp!')
        return False