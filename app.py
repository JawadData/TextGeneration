
from flask import Flask, render_template, request, jsonify
import threading
from model.train_model import train_model


app = Flask(__name__)

training = False
training_complete = False
model_1 = None

def train_model_thread(input_file):
    global training, training_complete, model_1
    training = True
    training_complete = False
    try:
        print("Début de l'entraînement du modèle...")
        model_1 = train_model(input_file)
        training_complete = True
        print("Entraînement terminé et modèle chargé en mémoire.")
    except Exception as e:
        print(f"Erreur lors de l'entraînement: {e}")
        training_complete = False
    finally:
        training = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_training', methods=['POST'])
def start_training():
    global training, training_complete, model_1
    if not training:
        thread = threading.Thread(target=train_model_thread, args=('data/train.txt',))
        thread.start()
        return jsonify({'status': 'Training started'})
    else:
        return jsonify({'status': 'Training already in progress'})

@app.route('/training_status', methods=['GET'])
def training_status():
    global training, training_complete
    if training:
        return jsonify({'status': 'Training in progress'})
    elif training_complete:
        return jsonify({'status': 'Training complete'})
    else:
        return jsonify({'status': 'Not started or failed'})
    
@app.route('/generate', methods=['POST'])
def generate_text():
    global model_1
    user_input = request.json.get('input_text')
    if not model_1:
        return jsonify({'error': 'The model is not trained or loaded.'}), 400

    try:
        generated_text = model_1.autocomplete(user_input)
        if generated_text:
            return jsonify({'generated_text': generated_text})
        else:
            return jsonify({'error': 'Unable to generate text with the provided input'}), 400
    except Exception as e:
        print(f"Error during text generation: {e}")
        return jsonify({'error': 'Error during text generation.'}), 500

@app.route('/generate_page')
def generate_page():
    return render_template('generate.html')

if __name__ == '__main__':
    app.run(debug=True)
