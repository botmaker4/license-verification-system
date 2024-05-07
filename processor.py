# processor.py
import sys
import socket
import json
import random
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


em = EmailMessage()
em['From'] = email_sender
client = MongoClient(mongo_cluster)
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
            d = "NONE"
            for key, value in x.items():
                if 'huid' in key:
                    a = value
                elif 'ip' in key:
                    b = value
                elif 'password' in key:
                    c = value
                elif 'power' in key:
                    d = value
           
            return a, b, c , d
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None, None



def license_create(licensename,email_address,subject,message,exiting_message):
    # Find the document with the highest ID
   highest_id_doc = license_collection.find_one({}, sort=[("_id", -1)])
   auto_password_generated = generate_password_string()
   message = message + auto_password_generated
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
    if email_address!="NONE":
     send_email(email_address,subject,message,exiting_message)
    
    
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
    
def exit():
    print("Exiting..")
    sys.exit(1)
    
def send_email(email_address,subject,message,exiting_message):
    print(f'verifying with the server! ')
    subject = subject
    em['Subject'] =str(subject)
    em['To'] = email_address
    message=str(message)
    message=str(message)
    em.set_content(message)
    # Log in and send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
     smtp.login(email_sender, email_password)
     smtp.sendmail(email_sender, email_address, em.as_string())
     print(exiting_message)
     return True
 
 # Function to get public IP address
def get_public_ip():
    try:
        # Using a public API to fetch public IP address
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            public_ip = s.getsockname()[0]
        return public_ip
    except Exception as e:
        print("Failed to get public IP address:", e)
        return None


#OPTIONS SELECTION - USER

def show_menu():
    print("Select an option:")
    print("1. view license details")
    print("2. change username")
    print("3. change password")
    print("4. request custom license")
    print("5. change email")
    
def get_choice():
    while True:
        choice = input("Enter the number of your choice: ")
        if choice.isdigit() and int(choice) in [1, 2, 3,4,5]:
            return int(choice)
        else:
            print("Invalid input. Please enter a number between 1 and 5.")

def main():
    show_menu()
    choice = get_choice()

    if choice == 1:
        print("You selected Option 1.")
    elif choice == 2:
        print("You selected Option 2.")
    elif choice == 3:
        print("You selected Option 3.")
    elif choice == 4:
        print("You selected Option 4.")
    elif choice == 5:
        print("You selected Option 5.")
    return choice


