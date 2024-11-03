class MessageStrategy:
    def process_message(self, message):
        raise NotImplementedError("This method should be overridden by subclasses")


class ZApiStrategy(MessageStrategy):
    def process_message(self, message):
        phone_number = message['phone']
        text = message['text']['message']

        return phone_number, text