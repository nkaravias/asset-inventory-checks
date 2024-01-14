from .base_action import Action


class PubSubPublishAction(Action):
    def __init__(self, check):
        super().__init__(check.type)
        self.check = check

    def execute(self):
        # Logic for publishing to Pub/Sub
        pass
