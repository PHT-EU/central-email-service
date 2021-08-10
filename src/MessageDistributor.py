import json
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import requests


class MessageDistributor:
    def __init__(self):
        """
            MessageDistributor has Function for possible event massages from the PHT UI
            and sends emails out to the relevant addresses.
        """
        # Define mail connection
        self.smtp_user = os.getenv("SMTP_USER")
        self.smtp_password = os.getenv("SMTP_PASSWORD")
        self.smtp_mail_from = os.getenv("SMTP_MAIL_FROM")
        self.smtp_host = os.getenv("SMTP_HOST")
        self.port = 587

        # path to the mail template
        self.html_template_path = "/opt/pht-email-service/src/email_template.html"

        # Define the UI api connection
        self.ui_user = os.getenv("UI_USER")
        self.ui_token = os.getenv("UI_TOKEN")
        self.ui_address = os.getenv("UI_ADDRESS")

        # target mail
        self.mail_target = "david.hieber@uni-tuebingen.de"
        self.receiver_name = "David"

        # links to the UI pages
        self.proposal_link = "https://pht.tada5hi.net/proposals/"
        self.train_link = "https://pht.tada5hi.net/trains/"

    # proposal_operation_required

    def process_proposal_operation_required(self, data: dict):
        """
        Processing the message of type proposalOperationRequired
        by loading more information using the UI API using the proposalId,
        and using the returned user_id to get information about the proposal's creator.
        Using this information, an email subject and body are created and send out.
        :param data: dict with the fields "proposalId" ,"stationId"
        :return:
        """
        proposal_json = self._get_proposal_info(data["proposalId"])
        creator_json = self._get_user_info(proposal_json["user_id"])

        subject = "[PHT automated message]  operation required for proposal " + proposal_json["title"]
        body_html = self._create_proposal_operation_required_body_html(proposal_json, creator_json)
        msg = self._build_msg(subject, body_html)
        self._send_email_to(msg)

    def _create_proposal_operation_required_body_html(self, proposal_json: dict, creator_json: dict) -> str:
        """

        :param proposal_json: dict with information of the proposal
        :param creator_json:  dict with information about the person that created the proposal
        :return: The mail body as a html string
        """
        html_template = self._load_html_template()

        text = """<a href="{proposal_link}{proposalID}" target="_blank">{title}</a> is a new proposal from 
        {user_name} ({realm_name}). The proposal wants access to the following data "{requested_data}". 
        The risk is {risk} with the assessment "{risk_comment}". """

        html_with_text = html_template.format(text=text, receiver_name=self.receiver_name)
        html_with_modifications = html_with_text.format(receiver_name=self.receiver_name,
                                                        proposal_link=self.proposal_link,
                                                        proposalID=proposal_json["id"],
                                                        title=proposal_json["title"],
                                                        user_name=creator_json["display_name"],
                                                        realm_name=creator_json["realm"]["name"],
                                                        requested_data=proposal_json["requested_data"],
                                                        risk=proposal_json["risk"],
                                                        risk_comment=proposal_json["risk_comment"]
                                                        )

        return html_with_modifications

    # process_proposal_approved

    def process_proposal_approved(self, data: dict):
        proposal_json = self._get_proposal_info(data["proposalId"])
        creator_json = self._get_user_info(proposal_json["user_id"])

        subject = "[PHT automated message] proposal approved " + proposal_json["title"]
        body_html = self._create_proposal_approved_body_html(proposal_json, creator_json)
        msg = self._build_msg(subject, body_html)
        self._send_email_to(msg)

    def _create_proposal_approved_body_html(self, proposal_json: dict, creator_json: dict) -> str:
        html_template = self._load_html_template()
        text = """The proposal <a href="{proposal_link}{proposalID}" target="_blank">{proposal_name}</a> from the 
        realm {realm_name} was approved. """
        html_with_text = html_template.format(text=text, receiver_name=self.receiver_name)

        html_with_modifications = html_with_text.format(proposal_name=proposal_json["title"],
                                                        realm_name=creator_json["realm"]["name"],
                                                        proposal_link=self.proposal_link,
                                                        proposalID=proposal_json["id"],
                                                        )
        return html_with_modifications

    # train_started

    def process_train_started(self, data: dict):
        proposal_json = self._get_proposal_info(data["proposalId"])

        subject = "[PHT automated message] Train " + data["trainId"] + " started"
        body_html = self._create_train_started_body_html(data, proposal_json)
        msg = self._build_msg(subject, body_html)
        self._send_email_to(msg)

    def _create_train_started_body_html(self, data: dict, proposal_json: dict):
        html_template = self._load_html_template()
        text = """
                The train <a href="{train_link}{train_name}" target="_blank">{train_name}</a> from the
                proposal "{proposal_name}" has started.  
                """
        html_with_text = html_template.format(text=text, receiver_name=self.receiver_name)

        html_with_modifications = html_with_text.format(train_name=data["trainId"],
                                                        proposal_name=proposal_json["title"],
                                                        train_link=self.train_link
                                                        )

        return html_with_modifications

    # process_train_approved

    def process_train_approved(self, data: dict):
        proposal_json = self._get_proposal_info(data["proposalId"])
        subject = "[PHT automated message] Train " + data["trainId"] + " was approved"
        body_html = self._create_train_approved_html(data, proposal_json)
        msg = self._build_msg(subject, body_html)
        self._send_email_to(msg)

    def _create_train_approved_html(self, data: dict, proposal_json: dict):
        html_template = self._load_html_template()
        text = """
                        The train <a href="{train_link}{train_name}" target="_blank">{train_name}</a> from the proposal
                         {proposal_name} was approved.
                        """
        html_with_text = html_template.format(text=text, receiver_name=self.receiver_name)

        html_with_modifications = html_with_text.format(train_name=data["trainId"],
                                                        proposal_name=proposal_json["title"],
                                                        train_link=self.train_link
                                                        )
        return html_with_modifications

    # train_built

    def process_train_built(self, data: dict):
        proposal_json = self._get_proposal_info(data["proposalId"])
        subject = "[PHT automated message] Train " + data["trainId"] + " was built"
        body_html = self._create_train_built_html(data, proposal_json)
        msg = self._build_msg(subject, body_html)
        self._send_email_to(msg)

    def _create_train_built_html(self, data: dict, proposal_json: dict):
        html_template = self._load_html_template()
        text = """
                        The train <a href="{train_link}{train_name}" target="_blank">{train_name}</a> from 
                        the proposal {proposal_name} was built.
                        """
        html_with_text = html_template.format(text=text, receiver_name=self.receiver_name)

        html_with_modifications = html_with_text.format(train_name=data["trainId"],
                                                        proposal_name=proposal_json["title"],
                                                        train_link=self.train_link
                                                        )
        return html_with_modifications

    # train_finished

    def process_train_finished(self, data: dict):
        proposal_json = self._get_proposal_info(data["proposalId"])
        subject = "[PHT automated message] Train " + data["trainId"] + " is finished"
        body_html = self._create_train_finished_html(data, proposal_json)
        msg = self._build_msg(subject, body_html)
        self._send_email_to(msg)

    def _create_train_finished_html(self, data: dict, proposal_json: dict):
        html_template = self._load_html_template()
        text = """
                        The train <a href="{train_link}{train_name}" target="_blank">{train_name}</a> from
                         the proposal {proposal_name} is finished.
                        """
        html_with_text = html_template.format(text=text, receiver_name=self.receiver_name)

        html_with_modifications = html_with_text.format(train_name=data["trainId"],
                                                        proposal_name=proposal_json["title"],
                                                        train_link=self.train_link
                                                        )
        return html_with_modifications

    # train_failed

    def process_train_failed(self, data: dict):
        proposal_json = self._get_proposal_info(data["proposalId"])
        subject = "[PHT automated message] Train " + data["trainId"] + " is finished"
        body_html = self._create_train_failed_html(data, proposal_json)
        msg = self._build_msg(subject, body_html)
        self._send_email_to(msg)

    def _create_train_failed_html(self, data: dict, proposal_json: dict):
        html_template = self._load_html_template()
        text = """
                        The train <a href="{train_link}{train_name}" target="_blank">{train_name}</a> from 
                        the proposal {proposal_name} is failed.
                        """
        html_with_text = html_template.format(text=text, receiver_name=self.receiver_name)

        html_with_modifications = html_with_text.format(train_name=data["trainId"],
                                                        proposal_name=proposal_json["title"],
                                                        train_link=self.train_link
                                                        )
        return html_with_modifications

    # train_received

    def process_train_received(self, data: dict):
        proposal_json = self._get_proposal_info(data["proposalId"])
        subject = "[PHT automated message] New train from " + proposal_json["title"]
        body_html = self._create_train_received_html(data, proposal_json)
        msg = self._build_msg(subject, body_html)
        self._send_email_to(msg)

    def _create_train_received_html(self, data: dict, proposal_json: dict):
        html_template = self._load_html_template()
        text = """There is a new train from the proposal {proposal_name}  with the train id 
        <a href="{train_link}{train_name}" target="_blank">{train_name}</a> that has to be 
        checked. """
        html_with_text = html_template.format(text=text, receiver_name=self.receiver_name)

        html_with_modifications = html_with_text.format(train_name=data["trainId"],
                                                        proposal_name=proposal_json["title"],
                                                        train_link=self.train_link
                                                        )
        return html_with_modifications

    # train_operation_required

    def process_train_operation_required(self, data: dict):
        proposal_json = self._get_proposal_info(data["proposalId"])
        subject = "[PHT automated message] operation required for train " + data["trainId"]
        body_html = self._create_train_operation_required_html(data, proposal_json)
        msg = self._build_msg(subject, body_html)
        self._send_email_to(msg)

    def _create_train_operation_required_html(self, data: dict, proposal_json: dict):
        html_template = self._load_html_template()
        text = """
                                The train <a href="{train_link}{train_name}" target="_blank">{train_name}</a> from the proposal {proposal_name} was requires some operation.
                                """
        html_with_text = html_template.format(text=text, receiver_name=self.receiver_name)

        html_with_modifications = html_with_text.format(train_name=data["trainId"],
                                                        proposal_name=proposal_json["title"],
                                                        train_link=self.train_link
                                                        )
        return html_with_modifications

    # helper functions

    def _send_email_to(self, msg: MIMEMultipart):
        """
        Send an email message.
        :param msg:
        :return:
        """
        smtp_server = self._setup_smtp()
        smtp_server.sendmail(self.smtp_mail_from, msg["To"], msg.as_string())
        smtp_server.quit()

    def _setup_smtp(self) -> smtplib.SMTP:
        """
        create conception to smtp server
        :return:
        """
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

    def _load_html_template(self) -> str:
        """
        loads the tamplate that gets used for the emails
        :return: the html as a sting
        """
        with open(self.html_template_path, "r", encoding='utf-8') as f:
            html_template = f.read()
        return html_template

    def _build_msg(self, subject: str, body_html: str) -> MIMEMultipart:
        """
        fils in the relevant fields for a MIMEMultipart and retruns it
        :param subject:
        :param body_html:
        :return:
        """
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = self.smtp_mail_from
        # TODO later the corect resipienc have to be selectet
        msg["To"] = self.mail_target
        body = MIMEText(body_html, "html")
        msg.attach(body)
        return msg

    def _get_proposal_info(self, proposal_id: int) -> dict:
        get_proposal_url = self.ui_address + "proposals/" + str(proposal_id)
        return requests.get(get_proposal_url, auth=(self.ui_user, self.ui_token)).json()

    def _get_user_info(self, user_id: int) -> dict:
        get_proposal_url = self.ui_address + "users/" + str(user_id)
        return requests.get(get_proposal_url, auth=(self.ui_user, self.ui_token)).json()


def pprint_json(data: dict):
    print(json.dumps(data, indent=2, sort_keys=True))
