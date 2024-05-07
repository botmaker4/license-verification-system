import processor
from colorama import Fore, init
# Initialize colorama
init(autoreset=True)

def new_user_data(email_address,username_user_entered,password_2fa,old_data):
    # Define the new values to set
                new_data = {
                    "$set": {
                        "email_address": email_address,
                        "username": username_user_entered,
                        "huid": processor.huid,
                        "password": password_2fa,
                        "ip": processor.get_public_ip(), 
                        "power": "user" 
                    }
                }
                 # Update the document in the collection
                result = processor.license_collection.update_one(old_data, new_data)

                # Check if the update was successful
                if result.modified_count > 0:
                    print("Data updated! Re-login.")
                    input(Fore.RED + "Press enter to exit")
                    return True
                else:
                    print(" FAILED TO UPDATE DATA (Invalid license key!) ")
                    input(Fore.RED + "Press enter to exit")
                    return False