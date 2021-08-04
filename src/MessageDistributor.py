import json
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import requests


class MessageDistributor:
    def __init__(self, ui_user, ui_token, ui_address):
        docker = True
        if not docker:
            login_credentials_file = open("../static_setup.json", "r")
            credentials_json = json.load(login_credentials_file)
            self.smtp_user = credentials_json["smtp_user"]
            self.smtp_password = credentials_json["smtp_password"]
        else:
            self.smtp_user = os.getenv("SMTP_USER")
            self.smtp_password = os.getenv("SMTP_PASSWORD")

        self.smtp_mail_from = "pht@medizin.uni-tuebingen.de"
        self.port = 587
        self.smtp_host = "smtpserv.uni-tuebingen.de"
        if not docker:
            self.html_template_path = "email_template.html"
        else:
            self.html_template_path = "/opt/pht-email-service/src/email_template.html"
        self.ui_user = ui_user
        self.ui_token = ui_token
        self.ui_address = ui_address

        self.mail_target = "david.hieber@uni-tuebingen.de"
        self.receiver_name = "David"
        print(self.ui_address)

    # proposal_operation_required

    def process_proposal_operation_required(self, data):
        proposal_json = self._get_proposal_info(data["proposalId"])
        creator_json = self._get_user_info(proposal_json["user_id"])

        subject = "[PHT automated message]  operation required for proposal " + proposal_json["title"]
        body_html = self._create_proposal_operation_required_body_html(proposal_json, creator_json)
        msg = self._build_msg(subject, body_html)
        self._send_email_to(msg)

    def _create_proposal_operation_required_body_html(self, proposal_json, creator_json):
        html_template = self._load_html_template()

        text = """
        {title} is a new proposal from {user_name} ({realm_name}).
        The proposal wants access to the following data "{requested_data}".
        The risk is {risk} with the assessment "{risk_comment}".
        """

        html_with_text = html_template.format(text=text, receiver_name=self.receiver_name)

        html_with_modifications = html_with_text.format(receiver_name=self.receiver_name,
                                                        title=proposal_json["title"],
                                                        user_name=creator_json["display_name"],
                                                        realm_name=creator_json["realm"]["name"],
                                                        requested_data=proposal_json["requested_data"],
                                                        risk=proposal_json["risk"],
                                                        risk_comment=proposal_json["risk_comment"]
                                                        )

        return html_with_modifications

    # process_proposal_approved

    def process_proposal_approved(self, data):
        proposal_json = self._get_proposal_info(data["proposalId"])
        creator_json = self._get_user_info(proposal_json["user_id"])

        subject = "[PHT automated message] proposal approved " + proposal_json["title"]
        body_html = self._create_proposal_approved_body_html(proposal_json, creator_json)
        msg = self._build_msg(subject, body_html)
        self._send_email_to(msg)

    def _create_proposal_approved_body_html(self, proposal_json, creator_json):
        html_template = self._load_html_template()
        text = """
                The proposal {proposal_name} from the realm {realm_name} was approved.
                """
        html_with_text = html_template.format(text=text, receiver_name=self.receiver_name)

        html_with_modifications = html_with_text.format(proposal_name=proposal_json["title"],
                                                        realm_name=creator_json["realm"]["name"])
        return html_with_modifications

    # train_started

    def process_train_started(self, data):
        proposal_json = self._get_proposal_info(data["proposalId"])

        subject = "[PHT automated message] Train " + data["trainId"] + " started"
        body_html = self._create_train_started_body_html(data, proposal_json)
        msg = self._build_msg(subject, body_html)
        self._send_email_to(msg)

    def _create_train_started_body_html(self, data, proposal_json):
        html_template = self._load_html_template()
        text = """
                The train {train_name} from the proposal "{proposal_name}" has started.  
                """
        html_with_text = html_template.format(text=text, receiver_name=self.receiver_name)

        html_with_modifications = html_with_text.format(train_name=data["trainId"],
                                                        proposal_name=proposal_json["title"]
                                                        )

        return html_with_modifications

    # process_train_approved

    def process_train_approved(self, data):
        proposal_json = self._get_proposal_info(data["proposalId"])
        subject = "[PHT automated message] Train " + data["trainId"] + " was approved"
        body_html = self._create_train_approved_html(data, proposal_json)
        msg = self._build_msg(subject, body_html)
        self._send_email_to(msg)

    def _create_train_approved_html(self, data, proposal_json):
        html_template = self._load_html_template()
        text = """
                        The train {train_name} from the proposal {proposal_name} was approved.
                        """
        html_with_text = html_template.format(text=text, receiver_name=self.receiver_name)

        html_with_modifications = html_with_text.format(train_name=data["trainId"],
                                                        proposal_name=proposal_json["title"]
                                                        )
        return html_with_modifications

    # train_built

    def process_train_built(self, data):
        proposal_json = self._get_proposal_info(data["proposalId"])
        subject = "[PHT automated message] Train " + data["trainId"] + " was built"
        body_html = self._create_train_built_html(data, proposal_json)
        msg = self._build_msg(subject, body_html)
        self._send_email_to(msg)

    def _create_train_built_html(self, data, proposal_json):
        html_template = self._load_html_template()
        text = """
                        The train {train_name} from the proposal {proposal_name} was approved.
                        """
        html_with_text = html_template.format(text=text, receiver_name=self.receiver_name)

        html_with_modifications = html_with_text.format(train_name=data["trainId"],
                                                        proposal_name=proposal_json["title"]
                                                        )
        return html_with_modifications

    # train_finished

    def process_train_finished(self, data):
        proposal_json = self._get_proposal_info(data["proposalId"])
        subject = "[PHT automated message] Train " + data["trainId"] + " is finished"
        body_html = self._create_train_finished_html(data, proposal_json)
        msg = self._build_msg(subject, body_html)
        self._send_email_to(msg)

    def _create_train_finished_html(self, data, proposal_json):
        html_template = self._load_html_template()
        text = """
                        The train {train_name} from the proposal {proposal_name} is finished.
                        """
        html_with_text = html_template.format(text=text, receiver_name=self.receiver_name)

        html_with_modifications = html_with_text.format(train_name=data["trainId"],
                                                        proposal_name=proposal_json["title"]
                                                        )
        return html_with_modifications

    # train_failed

    def process_train_failed(self, data):
        proposal_json = self._get_proposal_info(data["proposalId"])
        subject = "[PHT automated message] Train " + data["trainId"] + " is finished"
        body_html = self._create_train_failed_html(data, proposal_json)
        msg = self._build_msg(subject, body_html)
        self._send_email_to(msg)

    def _create_train_failed_html(self, data, proposal_json):
        html_template = self._load_html_template()
        text = """
                        The train {train_name} from the proposal {proposal_name} is failed.
                        """
        html_with_text = html_template.format(text=text, receiver_name=self.receiver_name)

        html_with_modifications = html_with_text.format(train_name=data["trainId"],
                                                        proposal_name=proposal_json["title"]
                                                        )
        return html_with_modifications

    # train_received

    def process_train_received(self, data):
        proposal_json = self._get_proposal_info(data["proposalId"])
        subject = "[PHT automated message] New train from " + proposal_json["title"]
        body_html = self._create_train_received_html(data, proposal_json)
        msg = self._build_msg(subject, body_html)
        self._send_email_to(msg)

    def _create_train_received_html(self, data, proposal_json):
        html_template = self._load_html_template()
        text = """There is a new train from the proposal {proposal_name}  with the train id {train_name}  that has to be 
        checked. """
        html_with_text = html_template.format(text=text, receiver_name=self.receiver_name)

        html_with_modifications = html_with_text.format(train_name=data["trainId"],
                                                        proposal_name=proposal_json["title"]
                                                        )
        return html_with_modifications

    # train_operation_required

    def process_train_operation_required(self, data):
        proposal_json = self._get_proposal_info(data["proposalId"])
        subject = "[PHT automated message] operation required for train " + data["trainId"]
        body_html = self._create_train_operation_required_html(data, proposal_json)
        msg = self._build_msg(subject, body_html)
        self._send_email_to(msg)

    def _create_train_operation_required_html(self, data, proposal_json):
        html_template = self._load_html_template()
        text = """
                                The train {train_name} from the proposal {proposal_name} was requires some operation.
                                """
        html_with_text = html_template.format(text=text, receiver_name=self.receiver_name)

        html_with_modifications = html_with_text.format(train_name=data["trainId"],
                                                        proposal_name=proposal_json["title"]
                                                        )
        return html_with_modifications

    # helper functions

    def _send_email_to(self, msg):
        """
        Send an email message.
        :param msg:
        :return:
        """
        smtp_server = self._setup_smtp()
        smtp_server.sendmail(self.smtp_mail_from, msg["To"], msg.as_string())
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
            print(self.smtp_host)
            print(self.port)
            print(self.smtp_user)
            print(self.smtp_password)
            return None
        return server

    def _load_html_template(self):
        with open(self.html_template_path, "r", encoding='utf-8') as f:
            html_template = f.read()
        return html_template

    def _build_msg(self, subject, body_html):
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = self.smtp_mail_from
        # TODO later the corect resipienc have to be selectet
        msg["To"] = self.mail_target
        body = MIMEText(body_html, "html")
        msg.attach(body)
        return msg

    def _get_proposal_info(self, proposal_id):
        get_proposal_url = self.ui_address + "proposals/" + str(proposal_id)
        return requests.get(get_proposal_url, auth=(self.ui_user, self.ui_token)).json()

    def _get_user_info(self, user_id):
        get_proposal_url = self.ui_address + "users/" + str(user_id)
        return requests.get(get_proposal_url, auth=(self.ui_user, self.ui_token)).json()

    class User:
        def __init__(self):
            self.name = ""
            self.email = ""
            self.realm = ""
            self.send_mail_on_new_train = False
            self.send_mail_on_new_redy_to_build = False


def pprint_json(data):
    print(json.dumps(data, indent=2, sort_keys=True))
