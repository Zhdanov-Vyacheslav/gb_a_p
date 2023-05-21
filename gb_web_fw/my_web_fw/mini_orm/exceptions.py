class DbExecutescriptError(Exception):
    def __init__(self, message):
        super().__init__("Db Executescript error: {}".format(message))


class DbCommitError(Exception):
    def __init__(self, message):
        super().__init__("Db commit error: {}".format(message))


class DbUpdateError(Exception):
    def __init__(self, message):
        super().__init__("Db update error: {}".format(message))


class DbDeleteError(Exception):
    def __init__(self, message):
        super().__init__("Db delete error: {}".format(message))


class ElementNotFound(Exception):
    def __init__(self, message):
        super().__init__("Element not found: {}".format(message))
