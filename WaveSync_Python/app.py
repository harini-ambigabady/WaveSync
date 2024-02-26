import cv2
from flask import Flask, render_template, Response  # Import Response from flask

app = Flask(__name__)

def capture_and_enhance():
    cap = cv2.VideoCapture(0)

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_rate = int(cap.get(cv2.CAP_PROP_FPS))

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter("output.avi", fourcc, frame_rate, (frame_width, frame_height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Perform enhancement on the frame
        # Here, you can replace this with your enhancement techniques
        blurred_frame = cv2.GaussianBlur(frame, (5, 5), 0)
        enhanced_frame = cv2.convertScaleAbs(blurred_frame, alpha=1.5, beta=0)
            
        # Write the enhanced frame to the output video
        out.write(enhanced_frame)

        # Display the frame
        _, img_encoded = cv2.imencode('.jpg', enhanced_frame)
        img_data = img_encoded.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + img_data + b'\r\n')

    cap.release()
    out.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(capture_and_enhance(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
