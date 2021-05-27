from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.entity import Entity

engine = create_engine('sqlite:///data/database')
db = scoped_session(sessionmaker(autocommit=False,
                                 autoflush=False,
                                 bind=engine))


def init_db():
    import models
    Entity.metadata.create_all(bind=engine)
