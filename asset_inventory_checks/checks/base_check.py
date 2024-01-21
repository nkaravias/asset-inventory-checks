class Check:
    def __init__(self, check_type, action_type):
        self.type = check_type
        self.actionType = action_type

    def process(self):
        raise NotImplementedError("Must override process in subclass")

    def act(self):
        raise NotImplementedError("Must override act in subclass")
    
    def extract_app(self, name):
        raise NotImplementedError("Must override act in subclass")
