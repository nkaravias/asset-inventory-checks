from .base_action import Action


class EmailAction(Action):
    def __init__(self, check):
        super().__init__(check.type)
        self.check = check

    def execute(self):
        # Logic for sending an email
        pass
