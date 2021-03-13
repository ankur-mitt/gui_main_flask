from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
# enable cors
socketio = SocketIO(app, cors_allowed_origins="*")  # allow all origins
app.debug = True

''' demo code for creating json response
@app.route("/")
def home():
    return {
        "home": "WebSocket",
        "code": 200,
        "status": "OK",
    }

@app.route("/")
def every():
    return jsonify(home="WebSocket", code=200, status="OK")
'''


@socketio.on("connect")
def connected_successfully():
    print("success")


@socketio.on("images")
def images_received(data):
    print("images data received:", data)
    # do something with data
    #
    #
    #
    # do something with data
    socketio.emit("processed_images", {"image1": "image/base64 string", "image2": "image/base64 string"})


if __name__ == '__main__':
    socketio.run(app)
