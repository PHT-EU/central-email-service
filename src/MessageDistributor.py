class MessageDistributor():
    def __init__(self):
        users = self.request_users()
        pass

    def send_email_to(self, name, ):
        pass

    def get_admins_for_realm(self, realm):
        pass

    def request_users(self):
        pass

    def setup_smpt(self):
        pass

    class User():
        def __init__(self):
            self.name = ""
            self.email = ""
            self.realm = ""
            self.send_mail_on_new_train = False
            self.send_mail_on_new_redy_to_build = False
