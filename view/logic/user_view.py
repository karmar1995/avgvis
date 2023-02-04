from business_rules.abstract_user_view import AbstractUserView


class QtViewToAbstractUserView(AbstractUserView):
    def __init__(self, view):
        super().__init__()
        self.view = view

    def requestMapData(self):
        return None

    def requestObjectRegistration(self):
        pass

    def askForObjectsRegistration(self):
        return False

