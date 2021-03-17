from flask import Flask
from flask_socketio import SocketIO
import numpy as np
import base64
from io import BytesIO
from PIL import Image
from augmentation_functions import add_noise, rotate_image

app = Flask(__name__)
# enable cors
socketio = SocketIO(app, cors_allowed_origins="*")  # allow all origins

''' demo code for creating json response
@app.route("/")
def home():
    return jsonify(home="WebSocket", code=200, status="OK")
'''
'''demo code for sending static file response
@app.route("/")
def home():
    return send_file("frontend/build/index.html")
'''


@socketio.on("connect")
def connected_successfully():
    pass


# images received to apply operations
@socketio.on("apply_operations")
def images_received(images_data):
    processed_data = []
    for single_image_data in images_data:
        # convert str to array
        head64data, body64data = single_image_data["src"].split(',')
        image = Image.open(BytesIO(base64.b64decode(body64data)))
        image = image.convert("RGB")
        img = np.array(image)

        # operations started
        img = add_noise(img)
        img = rotate_image(img, deg=10)

        # convert array to str
        pil_img = Image.fromarray((img * 255).astype(np.uint8))
        buff = BytesIO()
        pil_img.save(buff, format="PNG")
        head64data = "data:image/png;base64,"
        body64data = base64.b64encode(buff.getvalue()).decode("utf-8")

        # update data
        single_image_data["src"] = head64data + body64data
        processed_data.append(single_image_data)

    # send processed data
    socketio.emit("processed_images", processed_data)


if __name__ == '__main__':
    socketio.run(app)
