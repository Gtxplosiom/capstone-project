from win11toast import notify

def show_notification(title, message):
    notification = notify(title, message)
    notification.show()

if __name__ == "__main__":
    notification_title = "Notification Title"
    notification_message = "This is a sample notification message."

    show_notification(notification_title, notification_message)
