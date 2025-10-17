class Schedule:
    def __init__(self, events=None):
        self.events = events if events is not None else []

    def add_event(self, event):
        self.events.append(event)

    def remove_event(self, event):
        self.events.remove(event)

    def get_events(self):
        return self.events

    def __repr__(self):
        return f"Schedule(events={self.events})"


class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return f"User(username={self.username}, email={self.email})"