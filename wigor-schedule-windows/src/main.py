import tkinter as tk
from gui import Application
from wigor_client import WigorClient
from auth import authenticate_user
from config import API_ENDPOINT

def main():
    # Initialize the main application window
    root = tk.Tk()
    root.title("Wigor Schedule")

    # Create an instance of the WigorClient
    client = WigorClient(API_ENDPOINT)

    # Authenticate the user
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    if authenticate_user(username, password):
        # Fetch the schedule
        schedule = client.fetch_schedule(username)
        
        # Initialize the GUI with the fetched schedule
        app = Application(root, schedule)
        root.mainloop()
    else:
        print("Authentication failed. Please check your credentials.")

if __name__ == "__main__":
    main()