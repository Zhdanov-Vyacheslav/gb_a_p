import os

from wsgiref.simple_server import make_server
from main import app

HOST = os.getenv("SERVER_HOST", "0.0.0.0")
PORT = int(os.getenv("SERVER_PORT", "8000"))

if __name__ == "__main__":
    with make_server(host=HOST, port=PORT, app=app) as web:
        print("Server started {host}:{port}".format(host=HOST, port=PORT))
        web.serve_forever()
