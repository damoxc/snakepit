"""The application's model objects"""
import logging

from sqlalchemy import and_, or_
from sqlalchemy.orm import sessionmaker, scoped_session
from snakepit.model.classes import *

log = logging.getLogger(__name__)

engine = None
db = None

def init_model(dbengine):
    """Call me before using any of the tables or classes in the model"""
    global db, engine
    log.info('Initialising the database model')
    
    engine = dbengine
    sm = sessionmaker(autoflush=False, autocommit=False, bind=engine)
    db = scoped_session(sm)