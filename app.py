from flask import Flask, request, jsonify, render_template
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os

app = Flask(__name__)

# Load trained model
model = load_model("blood_group_model.h5")

# Blood group labels (must match training)
labels = ['A', 'B', 'AB', 'O']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    img_file = request.files['file']
    os.makedirs("uploads", exist_ok=True)
    img_path = os.path.join("uploads", img_file.filename)
    img_file.save(img_path)

    # Preprocess image
    img = image.load_img(img_path, target_size=(128,128))  # Match training size
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0

    # Predict
    predictions = model.predict(img_array)[0]  # Get 1D array
    pred_index = np.argmax(predictions)
    blood_group = labels[pred_index]

    # Create confidence dictionary
    confidence = {labels[i]: float(f"{predictions[i]*100:.2f}") for i in range(len(labels))}

    return jsonify({
        'blood_group': blood_group,
        'confidence': confidence  # Confidence in percentages
    })

if __name__ == "__main__":
    app.run(debug=True)

