from plyer import notification

title = "Take a Break"

message = "You have been coding for a while. PLease stretch and drink water!"

notification.notify(
    title = title, 
    message = message,
    app_name = "Python Notifier",
    timeout = 10
)

print("Notification sent successfully")