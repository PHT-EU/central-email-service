from typing import Union

from train_lib.clients import Consumer


class MassageConsummer(Consumer):
    def __init__(self, amqp_url: str):
        super().__init__(amqp_url)

    def run(self):
        super().run()

    def on_message(self, _unused_channel, basic_deliver, properties, body):
        pass

    def process_message(self, msg: Union[dict, str]):
        pass


def main():
    # TODO login parameters only for developing later in docker -compose as env varibals
    vault_token = " the token "
    AMPQ_URL = "https://pht.tada5hi.net/api "
    massage_consumer = MassageConsummer(AMPQ_URL)



if __name__ == '__main__':
    main()
