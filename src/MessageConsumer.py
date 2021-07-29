import json

from train_lib.clients import Consumer
from train_lib.clients.rabbitmq import LOG_FORMAT
from MessageDistributor import MessageDistributor
import logging

LOGGER = logging.getLogger(__name__)


class MassageConsumer(Consumer):
    def __init__(self, amqp_url: str, queue: str = "", routing_key: str = None, ui_user: str = None,
                 ui_token: str = None , ui_address: str = None):
        super().__init__(amqp_url, queue, routing_key=routing_key)
        self.ui_token = ui_token
        self.ui_user = ui_user
        self.md = MessageDistributor(ui_user, ui_token, ui_address)

    def run(self):
        super().run()

    def on_message(self, _unused_channel, basic_deliver, properties, body):
        pass

    def process_message(self, msg):
        if msg["type"] == "proposalOperationRequired":
            self.md.process_proposal_operation_required(msg["data"])
        elif msg["type"] == "proposalApproved":
            pass
        elif msg["type"] == "trainStarted":
            self.md.process_train_started(msg["data"])
        elif msg["type"] == "trainApproved":
            pass
        elif msg["type"] == "trainBuilt":
            pass
        elif msg["type"] == "trainFinished":
            pass
        elif msg["type"] == "trainFailed":
            pass
        elif msg["type"] == "trainReceived":
            pass
        elif msg["type"] == "trainOperationRequired":
            pass
        else:
            LOGGER.info(f"Invalid event {msg['type']}")


def main():
    # TODO login parameters only for developing later in docker -compose as env varibals
    # only for testign later with os.getenv("smtp_user") etc , ,..
    login_credentials_file = open("../static_setup.json", "r")
    credentials_json = json.load(login_credentials_file)

    AMPQ_URL = credentials_json["AMPQ_URL"]
    ui_user = credentials_json["ui_user"]
    ui_token = credentials_json["ui_token"]
    ui_address = "https://pht.tada5hi.net/api/"

    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    massage_consumer = MassageConsumer(AMPQ_URL, ui_user=ui_user, ui_token=ui_token, ui_address=ui_address,
                                       routing_key="en.event")

    # static test
    sample_message_file = open("../example_message_proposal.json", "r")
    sample_message_json = json.load(sample_message_file)
    pprint_json(sample_message_json)
    massage_consumer.process_message(sample_message_json)


def pprint_json(data):
    print(json.dumps(data, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
