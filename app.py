from flask import Flask, Response
from PIL import Image, ImageDraw, ImageFont
import random
import time
import io
from PIL import ImageSequence

app = Flask(__name__)

# Set screen dimensions
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 1000  # Portrait mode for mobile devices

# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
CYAN = (0, 255, 255)
GREEN = (0, 255, 0)

# Define line width
LINE_WIDTH = 5

font_path = "font2.ttf"
font1 = ImageFont.truetype(font_path, 70)

def generate_random_glitch_color():
    """Generate a random glitch color."""
    return random.choice([RED, CYAN, GREEN])

def generate_text_frame(text, font, color):
    """Generate a frame with the specified text and color."""
    img = Image.new("RGB", (SCREEN_WIDTH, SCREEN_HEIGHT), BLACK)
    draw = ImageDraw.Draw(img)
    text_width, text_height = draw.textsize(text, font=font)
    text_x = (SCREEN_WIDTH - text_width) / 2
    text_y = (SCREEN_HEIGHT - text_height) / 2
    draw.text((text_x, text_y), text, fill=color, font=font)
    return img

def generate_zoom_effect(image_path):
    """Generate frames for zoom-in effect on an image."""
    img = Image.open(image_path)
    img = img.convert("RGB")  # Convert image to RGB mode
    img_width, img_height = img.size
    start_time = time.time()
    while time.time() - start_time <= 1:
        for scale in range(1, 101):
            scaled_img = img.resize((int(img_width * scale / 100), int(img_height * scale / 100)), Image.ANTIALIAS)
            frame_bytes = io.BytesIO()
            scaled_img.save(frame_bytes, format="JPEG")
            frame_bytes.seek(0)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes.read() + b'\r\n')


def generate_glitch_frames():
    # Start time
    start_time = time.time()

    # Main loop
    while True:
        # Check if 5 seconds have passed
        elapsed_time = time.time() - start_time
        
        # Generate glitch frames during the first 2 seconds
        if elapsed_time <= 2:
            img = Image.new("RGB", (SCREEN_WIDTH, SCREEN_HEIGHT), BLACK)
            draw = ImageDraw.Draw(img)
            for x in range(0, SCREEN_WIDTH, LINE_WIDTH):
                glitch_color = generate_random_glitch_color()
                draw.line([(x, 0), (x, SCREEN_HEIGHT)], glitch_color, width=LINE_WIDTH)
            img_bytes = io.BytesIO()
            img.save(img_bytes, format="JPEG")
            img_bytes.seek(0)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + img_bytes.read() + b'\r\n')
        
        # Generate "Welcome to NIMBUS" text frames between 2 and 5 seconds
        elif 2 < elapsed_time <= 6:
            for color in [RED, CYAN, GREEN]:
                text_img = generate_text_frame("Welcom To \nNIMBUS 2k24", font1, color)
                text_bytes = io.BytesIO()
                text_img.save(text_bytes, format="JPEG")
                text_bytes.seek(0)
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + text_bytes.read() + b'\r\n')
        
        # Generate zoom effect after 5 seconds
        else:
            yield from generate_zoom_effect("logo.jpg")  # Replace with your image path
            return


@app.route('/')
def index():
    return Response(generate_glitch_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
