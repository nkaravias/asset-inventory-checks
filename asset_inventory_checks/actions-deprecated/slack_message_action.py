from .base_action import Action


class SlackMessageAction(Action):
    def __init__(self, check):
        super().__init__(check.type)
        self.check = check

    def execute(self):
        # Logic for sending a slack message
        pass
