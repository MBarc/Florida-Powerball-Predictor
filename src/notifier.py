import requests
import os

def send_notification(message: str):
    """
    Sends a push notification via IFTTT Webhooks.
    The message is passed as 'value1' which maps to {{value1}} in IFTTT.
    """
    url = os.environ.get("IFTTT_WEBHOOK_URL")
    
    if not url:
        raise RuntimeError("IFTTT_WEBHOOK_URL environment variable not set.")
    
    payload = {"value1": message}

    print(payload)

    try:
        resp = requests.post(url, json=payload)
        resp.raise_for_status()
        print("IFTTT notification sent successfully!")
    except Exception as e:
        raise RuntimeError(f"Failed to send IFTTT notification: {e}")


# Example usage
if __name__ == "__main__":
    send_notification("TEST MESSAGE. . . 1, 2, 3!")

