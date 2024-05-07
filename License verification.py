# main.py
import sys
import socket
from datetime import datetime
from colorama import Fore, init
import processor
import os
import random
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
        license_key_exist = processor.license_collection.count_documents({"license": license_key})
        result = license_key_exist if license_key_exist!=0 else processor.exit()
        dealer_2fa = input(f'enter dealer generated password: ')
        password_2fa = input(f'enter a password for 2fa: ')
        username_user_entered=input(f'enter username to link: ')
        email_address = input("enter your email address: ")
       
        #VERIFICATION OF EMAIL ADDRESS
        os.system('cls')
        email_verification_otp = random.randint(1000,9999)
        subject = f'Email Verification'
        exiting_message = f'Otp sent!'
        message = f"Your email verification code is {email_verification_otp} . Do not share!"
        if processor.send_email(email_address,subject,message,exiting_message ) ==True:

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
               print(" FAILED TO UPDATE DATA (Invalid license key!) ")
    else:
          print(f'PREVIOUS LOGIN DETECTED! ')
          uniqueid, ip, password_license = processor.license_verification()
   
          Password_verification = input(f'please enter your password linked with your license : ')
          if uniqueid == processor.huid and ip == processor.ip_address and password_license == Password_verification:
              os.system('cls')
              print(f'credentials verified \n')
              
              
              # Inputs for license creation
              licensename = input("Please enter your license key to create: ")
              email_address=input("enter users email / NONE ")
              subject=f"License details"
              message = f"""your license details are - 
              license key - {licensename}
              dealer-generated password - """
              exiting_message = "Details sent!"
              processor.license_create(licensename,email_address,subject,message,exiting_message)
          else:
              print("unable to verify credentials")
        
else:
    print("Connection to database unsuccessful.")

# Press enter to exit
input(Fore.RED + "Press enter to exit")
