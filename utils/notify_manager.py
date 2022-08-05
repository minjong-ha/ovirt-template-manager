import notify2

class NotifyManager:
    def __init__(self):
        print("notify init")
        self._notify = notify2.init("ovirt-template-manager")

    def send_notification(self):
        self._notify = notify2.Notification("Download Complete!", "Requested Download complete")
        self._notify.show()
