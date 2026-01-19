from datetime import datetime, timezone


def format_message(username, message):
    timestamp = datetime.now(timezone.utc).strftime('%H:%M:%S')
    return f"[{timestamp} ] | {username}: {message} \n"