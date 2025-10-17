def log_message(message):
    """Logs a message to the console."""
    print(f"[LOG] {message}")

def handle_error(error):
    """Handles errors by logging them."""
    log_message(f"[ERROR] {error}")

def format_schedule_data(schedule_data):
    """Formats the schedule data for display."""
    formatted_data = []
    for item in schedule_data:
        formatted_data.append(f"{item['date']}: {item['event']}")
    return "\n".join(formatted_data)