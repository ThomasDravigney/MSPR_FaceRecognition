import base64
from io import BytesIO
from PIL import Image
from flask import Flask, render_template, request
from models.post import Post
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
    image = Image.open(imagefile)

    # Déterminer la valeur de AgentId (ou laisser à None si non reconnu)

    # Choix de la vue
    if AgentId is None:
        # Erreur si l'agent n'est pas reconnu
        return render_template('login.html', model="Agent non reconnu, réessayez.")
    else:
        # Affichage des équipements pour l'agent si reconnu
        return render_template('index.html')
        # Avec la base de données : return render_template('index.html', model=db.query(Agent).filter(Agent.AgentId = AgentId))


@server.route('/security_agent')
def security_agent():
    data = SecurityAgent('Thomas', 'Dravigney')
    return render_template('security_agent.html', model=data)


if __name__ == '__main__':
    server.run()
