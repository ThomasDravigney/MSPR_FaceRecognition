class Post:
    id: int
    caption: str
    text: str = ''
    likes: int = 0

    def __init__(self, id, caption):
        self.id = id
        self.caption = caption
