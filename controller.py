from flask import Flask, render_template
from models.post import Post

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


if __name__ == '__main__':
    server.run()
