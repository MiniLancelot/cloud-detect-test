import base64
import time
from flask import Flask, request, jsonify, g
from flask_socketio import SocketIO, emit, send
from flask_cors import CORS


class ServerSocket:
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)
        self.socket = SocketIO(self.app)
        self.setup_routes()
        self.detect_machine = False

    def setup_routes(self):
        @self.app.route("/")
        def index():
            return "Server is running"

        @self.app.route("/detect", methods=["POST"])
        def get_image():
            if not self.detect_machine:
                return jsonify({"failed": "Detect machine is not connected"})
            file = request.files["image"]
            file_bytes = base64.b64encode(file.read()).decode("utf-8")

            data_receive = False
            res_data = None

            def handle_data(data):
                nonlocal data_receive
                nonlocal res_data
                data_receive = True
                res_data = data

            self.socket.emit("image", file_bytes, callback=handle_data)
            self.socket.sleep(2)

            if data_receive:
                # return jsonify(res_data)
                return jsonify({"plant_detected": res_data})
            else:
                return jsonify({"message": "No data received"})

        @self.socket.on("connect")
        def handle_connect():
            self.detect_machine = True
            print("Detect machine connected")

        @self.socket.on("disconnect")
        def handle_disconnect():
            self.detect_machine = False
            print("Detect machine disconnected")

    def run(self):
        # print("Server is running")
        # self.socket.run(self.app, debug=True, allow_unsafe_werkzeug=True, log_output=True,
        #                 host="0.0.0.0")
        # self.socket.run(self.app)
        self.socket.run(self.app, host="0.0.0.0", allow_unsafe_werkzeug=True, port=3000)
        self.socket.on()