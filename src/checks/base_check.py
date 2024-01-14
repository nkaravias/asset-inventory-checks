class Check:
    def __init__(self, status, check_type, action_type):
        self.status = status
        self.type = check_type
        self.actionType = action_type

    def process(self):
        raise NotImplementedError("Must override process in subclass")

    def act(self):
        raise NotImplementedError("Must override act in subclass")
