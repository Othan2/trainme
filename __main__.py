from src.garmin.client import Garmin
from getpass import getpass

def main():
    email = input("Enter Garmin username: ")
    password = getpass("Enter Garmin password: ")
    
    with Garmin(email=email, password=password, return_on_mfa=True) as client:
        print("Connected to Garmin Connect")
        workouts = client.get_user_summary('2025-06-06')
        print(workouts)
        
        
        # Add workout operations here

if __name__ == "__main__":
    main()
