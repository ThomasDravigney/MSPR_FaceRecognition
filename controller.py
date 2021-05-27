from flask import Flask, render_template
from models.post import Post
from models.security_agent import SecurityAgent

server = Flask(__name__, template_folder='views')


@server.route('/')
def index():
    data = {
        'title': 'Posts',
        'posts': [
            Post(1, 'Post #1'),
            Post(2, 'Post #2')
        ]
    }
    return render_template('index.html', model=data)



@server.route('/security_agent')
def security_agent():
    data = SecurityAgent('Thomas', 'Dravigney')
    return render_template('security_agent.html', model=data)

if __name__ == '__main__':
    server.run()
