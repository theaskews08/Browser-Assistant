import csv
import numpy as np
import pickle

# Load training data to get vocabulary
with open("training_data.txt") as data0:
    data = np.array(list(csv.reader(data0)))

words = []
for _ in data[:, 0]:
    words.extend(_.split())
words = list(set(words))
words.sort()

print(f"Vocabulary size: {len(words)}")

# Save vocabulary
with open('vocab.pkl', 'wb') as file:
    pickle.dump(set(words), file)
print("Saved vocab.pkl")

# Load the trained model
from keras.models import model_from_json

try:
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    model.load_weights("weights.weights.h5")
    print("Model loaded successfully")

    # Extract and pickle weights
    weights0 = {}
    layers = model.layers
    for i in range(len(layers)):
        layer = layers[i]
        weights0["W"+str(i)] = np.copy(layer.get_weights()[0])
        weights0['b'+str(i)] = np.copy(layer.get_weights()[1])

    with open('weights.pkl','wb') as file:
        pickle.dump(weights0, file)
    print("Saved weights.pkl")

    # Test the model
    input_size = len(words)

    def get_index_of(word):
        try:
            return words.index(word)
        except:
            return -1

    def encode_sent(sentence):
        sent = np.zeros((1, input_size))
        for _ in sentence.split():
            indx = get_index_of(_)
            if indx != -1:
                sent[0][indx] = 1
        return sent

    # Test predictions
    test_commands = [
        "scroll down",
        "set volume to 50",
        "press enter",
        "mouse click"
    ]

    for cmd in test_commands:
        y_pred = model.predict(encode_sent(cmd), verbose=0)
        print(f"Command: '{cmd}' -> Prediction index: {y_pred.argmax()}, Confidence: {y_pred.max():.4f}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
