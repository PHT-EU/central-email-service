import json
import smtplib, ssl


class MessageDistributor:
    def __init__(self):
        # users = self.request_users()
        # TODO send emails to spesific users , for know send only to me for testing
        # only for testign later with os.getenv("smtp_user") etc , ,..
        login_credentials_file = open("../static_setup.json", "r")
        credentials_json = json.load(login_credentials_file)
        self.smtp_user = credentials_json["smtp_user"]
        self.smtp_password = credentials_json["smtp_password"]
        self.smtp_mail_from = "pht@medizin.uni-tuebingen.de"
        self.port = 587
        self.smtp_host = "smtpserv.uni-tuebingen.de"

        self.mail_target = "david.hieber@uni-tuebingen.de"

        self._setup_smtp()

    def process_proposal_operation_required(self, data):
        pprint_json(data)
        self._send_email_to()

    def process_train_started(self, data):
        pass

    def _send_email_to(self, name, body):
        pass

    def request_users(self):
        pass

    def _setup_smtp(self):
        pass

    class User:
        def __init__(self):
            self.name = ""
            self.email = ""
            self.realm = ""
            self.send_mail_on_new_train = False
            self.send_mail_on_new_redy_to_build = False


def pprint_json(data):
    print(json.dumps(data, indent=2, sort_keys=True))
