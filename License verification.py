# main.py

import sys
import socket
from datetime import datetime
from colorama import Fore, init
import processor
import smtplib
import os
import ssl
import random
from email.message import EmailMessage
# Add SSL (layer of security)
import ssl
context = ssl.create_default_context()

# CODE FOR SENDING OTP
email_sender = 'shourya.development.studio@gmail.com'
email_password = "geayouagpimwcbvp"
em = EmailMessage()
em['From'] = email_sender
"""  subject = 'Transaction Update!'
                          em['Subject'] = subject
                          em['To'] = sender_email
                          message=f"Your otp for amount {amount_to_receive} is {otp} \nRequested by {bank_name}"
                          message=str(message)
                          em.set_content(message)
                         # Log in and send the email
                          with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                           smtp.login(email_sender, email_password)
                           smtp.sendmail(email_sender, sender_email, em.as_string())"""
# Initialize colorama
init(autoreset=True)

# Call the function to check the database connection
if processor.check_db():
    # Define the key-value pair to search for
    key = "huid"
    value = processor.huid

    # Count occurrences of the key-value pair in the collection
    count = processor.license_collection.count_documents({key: value})

    # Store the count in a variable
    occurrences = count

    # FIRST LOGIN OCCURENCE SYSTEM
    if occurrences == 0:
        os.system('cls')
        print(f'FIRST TIME LOGIN DETECTED! \n ')
        license_key = input(f'enter your license: ')
        dealer_2fa = input(f'enter dealer generated password: ')
        password_2fa = input(f'enter a password for 2fa: ')
        username_user_entered=input(f'enter username to link: ')
        email_address = input("enter your email address: ")
       
        #VERIFICATION OF EMAIL ADDRESS
        os.system('cls')
        print(f'verifying with the server! ')
        email_verification_otp = random.randint(1000,9999)
        subject = 'Email Verifiation'
        em['Subject'] = subject
        em['To'] = email_address
        message=f"Your email verification code is {email_verification_otp} . Do not share!"
        email_verification_otp=str(email_verification_otp)
        message=str(message)
        em.set_content(message)
        
       # Log in and send the email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
         smtp.login(email_sender, email_password)
         smtp.sendmail(email_sender, email_address, em.as_string())
         print(f"OTP has been sent! ")
         user_entered_otp = input(f'please enter your otp: ')
         correct_otp =  processor.otp_verification(email_verification_otp,user_entered_otp)
         if correct_otp:
           old_data = {"license": license_key, "huid": "NONE" , "password":dealer_2fa}
       
           # Define the new values to set
           new_data = {
               "$set": {
                   "email_address" : email_address,
                   "username":username_user_entered,
                   "huid": processor.huid,
                   "password": password_2fa,
                   "ip": processor.ip_address
               }
           }
           # Update the document in the collection
           result = processor.license_collection.update_one(old_data, new_data)
    
           # Check if the update was successful
           if result.modified_count > 0:
               print("Data updated! Re-login.")
           else:
               print("Invalid license key!")
    else:
        print(f'PREVIOUS LOGIN DETECTED! ')
        uniqueid, ip, password_license = processor.license_verification(processor.huid, processor.ip_address)

        Password_verification = input(f'please enter your password linked with your license : ')
        if uniqueid == processor.huid and ip == processor.ip_address and password_license == Password_verification:
            print(f'credentials verified \n')
            os.system('cls')
            
            # Inputs for license creation
            licensename = input("Please enter your license key to create: ")
            processor.license_create(licensename)
        else:
            print("unable to verify credentials")
else:
    print("Connection to database unsuccessful.")

# Press enter to exit
input(Fore.RED + "Press enter to exit")
