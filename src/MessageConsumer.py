import json
import os

from train_lib.clients import Consumer
from train_lib.clients.rabbitmq import LOG_FORMAT
from MessageDistributor import MessageDistributor
import logging

LOGGER = logging.getLogger(__name__)


class MassageConsumer(Consumer):

    def __init__(self, amqp_url: str, queue: str = "", routing_key: str = None):
        """
        MassageConsumer is a child class of Consumer from the train liberty.
        MassageConsumer listening for rabbitmq messages and calls the corresponding MessageDistributor
        :param amqp_url: the addres of the rabbitmq service
        :param queue:
        :param routing_key: only messages with this key get processed
        """
        super().__init__(amqp_url, queue, routing_key=routing_key)

        self.md = MessageDistributor()

        # Set auto reconnect to true
        self.auto_reconnect = True

    def run(self):
        super().run()

    def on_message(self, _unused_channel, basic_deliver, properties, body):
        """
        on_message defines the behavior at massages.
        Tries to load the body as json; if this is not possible, log the event.
        Calls process_message to interpret the massage.
        Acknowledges the massage using the parent on_message function.
        :param _unused_channel:
        :param basic_deliver:
        :param properties:
        :param body:
        :return:
        """
        try:
            message = json.loads(body)
        except:
            LOGGER.error("Malformed json input")
            super().on_message(_unused_channel, basic_deliver, properties, body)
        self.process_message(message)
        super().on_message(_unused_channel, basic_deliver, properties, body)

    def process_message(self, msg: dict):
        """
        process_message selects the corresponding function in MessageDistributor to the massage type.
        :param msg: the json massage with type and data as attributes
        :return:
        """
        if msg["type"] == "proposalOperationRequired":
            self.md.process_proposal_operation_required(msg["data"])

        elif msg["type"] == "proposalApproved":
            self.md.process_proposal_approved(msg["data"])

        elif msg["type"] == "trainStarted":
            self.md.process_train_started(msg["data"])

        elif msg["type"] == "trainApproved":
            self.md.process_train_approved(msg["data"])

        elif msg["type"] == "trainBuilt":
            self.md.process_train_built(msg["data"])

        elif msg["type"] == "trainFinished":
            self.md.process_train_finished(msg["data"])

        elif msg["type"] == "trainFailed":
            self.md.process_train_failed(msg["data"])

        elif msg["type"] == "trainReceived":
            self.md.process_train_received(msg["data"])

        elif msg["type"] == "trainOperationRequired":
            self.md.process_train_operation_required(msg["data"])

        else:
            LOGGER.info(f"Invalid event {msg['type']}")


def main():

    ampq_url = os.getenv("AMPQ_URL")

    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

    massage_consumer = MassageConsumer(ampq_url, routing_key="en.event")
    massage_consumer.run()


def pprint_json(data):
    """
    helper funktion that prints json in a readabel format
    :param data: json data
    :return:
    """
    print(json.dumps(data, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
