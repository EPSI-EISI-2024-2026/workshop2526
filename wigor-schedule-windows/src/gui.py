from tkinter import Tk, Label, Button, Entry, messagebox
from wigor_client import WigorClient

class WigorScheduleApp:
    def __init__(self, master):
        self.master = master
        master.title("Wigor Schedule")

        self.label = Label(master, text="Enter your credentials:")
        self.label.pack()

        self.username_label = Label(master, text="Username:")
        self.username_label.pack()
        self.username_entry = Entry(master)
        self.username_entry.pack()

        self.password_label = Label(master, text="Password:")
        self.password_label.pack()
        self.password_entry = Entry(master, show='*')
        self.password_entry.pack()

        self.fetch_button = Button(master, text="Fetch Schedule", command=self.fetch_schedule)
        self.fetch_button.pack()

        self.schedule_label = Label(master, text="")
        self.schedule_label.pack()

    def fetch_schedule(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        client = WigorClient(username, password)
        try:
            schedule = client.get_schedule()
            self.schedule_label.config(text=schedule)
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = Tk()
    app = WigorScheduleApp(root)
    root.mainloop()