from flask import Flask
from cloud_server_socket import ServerSocket


def run_server():
    server_socket = ServerSocket()
    return server_socket.app


app = ServerSocket()
app.run()
