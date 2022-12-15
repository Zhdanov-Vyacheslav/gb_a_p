class NotFound(Exception):
    code = 404
    text = "Page not found"


class NotAllowed(Exception):
    code = 405
    text = "Unsupported HTTP-method"
