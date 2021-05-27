import tensorflow.keras
import numpy as np
import base64
from io import BytesIO
from PIL import Image, ImageOps
from flask import Flask, render_template, request
from db import init_db, db
from models.security_agent import SecurityAgent
from models.tools import Tool

server = Flask(__name__, template_folder='views')
with server.app_context():
    init_db()


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
        agent = db.query(SecurityAgent).filter(SecurityAgent.AI == str(agentIndex)).first()
        if agent is not None:
            AgentId = agent.Id

    # Choix de la vue
    if AgentId is None:
        # Erreur si l'agent n'est pas reconnu
        return render_template('login.html', model="Agent non reconnu, taux de ressemblance max :" + str(round(prediction[0][agentIndex]*100)) + "%.")
    else:
        # Affichage des équipements pour l'agent si reconnu
        return render_agent_form(agent, prediction[0][agentIndex], agentIndex)


def render_agent_form(agent, prediction=-1, agentIndex=-1):
    return render_template('index.html', model={
        'Prediction': prediction,
        'AI': agentIndex,
        'agent': agent,
        'available': db.query(Tool).filter(Tool.AgentId != agent.Id).order_by(Tool.TypeId, Tool.Name)
    })
    # Avec la base de données : return render_template('index.html', model=db.query(Agent).filter(Agent.AgentId = AgentId))


@server.route('/take', methods=['GET'])
def take():
    id_tool = request.args.get('id_tool')
    id_agent = request.args.get('id_agent')
    tool = db.query(Tool).filter(Tool.Id == id_tool).first()
    agent = db.query(SecurityAgent).filter(SecurityAgent.Id == id_agent).first()
    if tool is not None and agent is not None:
        tool.AgentId = id_agent
        db.commit()
    return render_agent_form(agent)


@server.teardown_appcontext
def shutdown_session(exception=None):
    db.remove()


if __name__ == '__main__':
    server.run()
