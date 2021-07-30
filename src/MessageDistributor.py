import json
import smtplib, ssl
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class MessageDistributor:
    def __init__(self, ui_user, ui_token, ui_address):
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

        self.ui_user = ui_user
        self.ui_token = ui_token
        self.ui_address = ui_address

        self.mail_target = "david.hieber@uni-tuebingen.de"
        self.receiver_name = "David"

    def get_proposal_info(self, id):
        get_proposal_url = self.ui_address + "proposals/" + str(id)
        return requests.get(get_proposal_url, auth=(self.ui_user, self.ui_token)).json()

    def get_user_info(self, id):
        get_proposal_url = self.ui_address + "users/" + str(id)
        return requests.get(get_proposal_url, auth=(self.ui_user, self.ui_token)).json()

    def process_proposal_operation_required(self, data):
        proposal_json = self.get_proposal_info(data["proposalId"])
        creator_json = self.get_user_info(proposal_json["user_id"])

        subject = "[PHT automatet message] " + proposal_json["title"]
        body_html = self.create_proposal_body_mag_html(proposal_json, creator_json)
        print(body_html)
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = self.smtp_mail_from
        msg["To"] = self.mail_target
        body = MIMEText(body_html, "html")
        msg.attach(body)

        # msg = 'Subject: {subject}\n\n{body}'.format(subject=subject, body=body).encode('utf-8')
        # TODO later the corect resipienc have to be selectet
        # self._send_email_to(self.mail_target, msg)

    def create_proposal_body_mag_html(self, proposal_json, creator_json):
        with open("email_html/proposalOperationRequired_email.html", "r", encoding='utf-8') as f:
            text = f.read()
        html = text.format(receiver_name=self.receiver_name,
                           title=proposal_json["title"],
                           user_name=creator_json["display_name"],
                           realm_name=creator_json["realm"]["name"],
                           requested_data=proposal_json["requested_data"],
                           risk=proposal_json["risk"],
                           risk_comment=proposal_json["risk_comment"]
                           )

        return html

    def process_train_started(self, data):
        pass

    def _send_email_to(self, mail_to, msg):
        smtp_server = self._setup_smtp()
        smtp_server.sendmail(self.smtp_mail_from, mail_to, msg.as_string())
        smtp_server.quit()

    def _setup_smtp(self):
        context = ssl.create_default_context()
        try:
            server = smtplib.SMTP(self.smtp_host, self.port)
            server.starttls(context=context)
            server.login(self.smtp_user, self.smtp_password)
        except Exception as e:
            print(e)
            print("connection could be established")
            return None
        return server

    class User:
        def __init__(self):
            self.name = ""
            self.email = ""
            self.realm = ""
            self.send_mail_on_new_train = False
            self.send_mail_on_new_redy_to_build = False


def pprint_json(data):
    print(json.dumps(data, indent=2, sort_keys=True))
