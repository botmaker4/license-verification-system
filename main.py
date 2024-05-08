# main.py
import os
import random
import sys
from colorama import Fore, init
import logscontroller
import processor
import dataupdate

# Initialize colorama
init(autoreset=True)


def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


# Call the function to check the database connection
processor.loading_animation()
sys.stdout.write('\r' + ' ' * 50 + '\r')
if processor.check_db():
    

    # Define the key-value pair to search for
    key = "huid"
    value = processor.huid

    # Count occurrences of the key-value pair in the collection
    occurrences = processor.license_collection.count_documents({key: value})

    # FIRST LOGIN OCCURRENCE SYSTEM
    if occurrences == 0:
        print('FIRST TIME LOGIN DETECTED!\n')
        license_key = input('Enter your license key: ')
        license_exists = processor.license_collection.count_documents({"license": license_key})

        if not license_exists:
            sys.exit("Invalid license key. Exiting...")

        dealer_generated_password = input('Enter dealer-generated password: ')
        if not processor.verify_dealer_password(license_key, dealer_generated_password):
            sys.exit("Invalid dealer-generated password. Exiting...")

        password_2fa = input('Enter a password for 2FA: ')
        username_user_entered = input('Enter username to link: ')
        
        # Check if username already exists in a license
        key = "username"
        value = username_user_entered
        occurrences = processor.license_collection.count_documents({key: value})
        if occurrences>0:
            sys.exit("Username already exists in another license. Exiting...")
            
        email_address = input("Enter your email address: ")
        
        key = "email_address"
        value = email_address
        occurrences = processor.license_collection.count_documents({key: value})
        # Check if email already exists in a license
        if occurrences>0:
            sys.exit("Email already exists in another license. Exiting...")

        # VERIFICATION OF EMAIL ADDRESS
        clear_screen()
        email_verification_otp = random.randint(1000, 9999)
        subject = 'Email Verification'
        exiting_message = 'OTP sent!'
        message = f"Your email verification code is {email_verification_otp}. Do not share!"
        
        if processor.send_email(email_address, subject, message, exiting_message):
            user_entered_otp = int(input('Please enter your OTP: '))
            correct_otp = processor.otp_verification(email_verification_otp, user_entered_otp)
            
            if correct_otp:
                old_data = {"license": license_key, "huid": "NONE", "password": dealer_generated_password}
                success = dataupdate.new_user_data(email_address, username_user_entered, password_2fa, old_data)
                # Proceed with user creation or other actions
                pass
            else:
                sys.exit("Incorrect OTP entered. Exiting...")

    else:
        print('PREVIOUS LOGIN DETECTED!')
        unique_id, public_ip, password_license, power_role, license_key = processor.license_verification()
        password_verification = input('Please enter your password linked with your license: ')

        if unique_id == processor.huid and password_license == password_verification:
            clear_screen()
            print('Credentials verified.\n')
            action = 'Logged IN!'
            logscontroller.log_update(action, power_role)

            # MAIN SYSTEM AFTER LOGIN
            if power_role == "user":
                user_choice = processor.main()

            elif power_role == "admin":
                # Inputs for license creation
                license_name = input("Please enter your license key to create: ")
                email_address = input("Enter user's email / NONE ")    
                subject = f"License details"
                message = f"""Your license details are: 
                License key - {license_name}
                Dealer-generated password - """
                exiting_message = "Details sent!"
                processor.license_create(license_name, email_address, subject, message, exiting_message)
                
                action = f'Created a license - {license_name} for -  {email_address}'
                logscontroller.log_update(action, power_role)
        else:
            print("Unable to verify credentials.")

else:
    print("Connection to the database was unsuccessful.")

# Press enter to exit
input(Fore.RED + "Press enter to exit")
