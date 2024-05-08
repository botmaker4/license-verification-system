import processor
import logscontroller
import socket
from colorama import Fore, init
# Initialize colorama
init(autoreset=True)

def new_user_data(email_address,username_user_entered,password_2fa,old_data):
    # Define the new values to set
                ip=processor.get_public_ip()
                new_data = {
                     "$set": {
                         "email_address": email_address,
                         "username": username_user_entered,
                         "huid": processor.huid,
                         "password": password_2fa,
                         "ip": ip, 
                         "power": "user" 
                     }
                 }
                if(ip==None):
                 hostname = socket.gethostname()
                 new_data = {
                     "$set": {
                         "email_address": email_address,
                         "username": username_user_entered,
                         "huid": processor.huid,
                         "password": password_2fa,
                         "ip": socket.gethostbyname(hostname), 
                         "power": "user" 
                     }
                 }
                 # Update the document in the collection
                result = processor.license_collection.update_one(old_data, new_data)

                # Check if the update was successful
                if result.modified_count > 0:
                    print("Data updated! Re-login.")
                    action =f'Data update (New User!) '
                    logscontroller.log_update(action,"user")
                    return True
                else:
                    print(" FAILED TO UPDATE DATA (Invalid license key!) ")
                    return False