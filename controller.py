import tensorflow.keras
import numpy as np
import base64
from io import BytesIO
from PIL import Image, ImageOps
from flask import Flask, render_template, request
from models.security_agent import SecurityAgent


server = Flask(__name__, template_folder='views')


@server.route('/', methods=['GET'])
def index():
    return render_template('login.html')


@server.route('/', methods=['POST'])
def login():
    # Récupération du champ "photo" du formulaire
    prefix, data = request.form['photo'].split(',')
    # Décodage de l'image en base 64
    imagefile = BytesIO(base64.b64decode(data))

    # Le code Teachable machine ici en utilisant le code de chargement d'image ci-dessous
    AgentId = None

    # Disable scientific notation for clarity
    np.set_printoptions(suppress=True)

    # Load the model
    model = tensorflow.keras.models.load_model('data/keras_model.h5')

    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1.
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # Replace this with the path to your image
    image = Image.open(imagefile)

    # resize the image to a 224x224 with the same strategy as in TM2:
    # resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS).convert('RGB')

    # turn the image into a numpy array
    image_array = np.asarray(image)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # run the inference
    prediction = model.predict(data)

    # Déterminer la valeur de AgentId (ou laisser à None si non reconnu)

    agentIndex = np.argmax(prediction[0])
    print(prediction[0][agentIndex])
    print(agentIndex)
    if prediction[0][agentIndex] > 0.8:


        db_list = [1, 4, 5, 6, 3, 2]
        if agentIndex < len(db_list):
            AgentId = db_list[agentIndex]
            print(AgentId)


        # agent = db.query(SecurityAgent).filter(SecurityAgent.AI=agentIndex).first()
        #if agent is not None:
            # AgentId = agent.id

    # Choix de la vue
    if AgentId is None:
        # Erreur si l'agent n'est pas reconnu
        return render_template('login.html', model="Agent non reconnu, réessayez.")
    else:
        # Affichage des équipements pour l'agent si reconnu
        return render_template('index.html', model={'Prediction':prediction[0][agentIndex], 'AI':agentIndex, 'AgentId':AgentId})
        # Avec la base de données : return render_template('index.html', model=db.query(Agent).filter(Agent.AgentId = AgentId))


if __name__ == '__main__':
    server.run()
