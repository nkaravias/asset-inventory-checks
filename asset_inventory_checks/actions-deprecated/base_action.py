class Action:
    def __init__(self, action_type):
        self.type = action_type

    def execute(self):
        raise NotImplementedError("Must override execute in subclass")
