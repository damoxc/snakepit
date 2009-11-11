import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from snakepit.lib.base import BaseController, render
from snakepit.model import db, Project

log = logging.getLogger(__name__)

class MainController(BaseController):

    def index(self):
        c.latest_projects = db.query(Project)[-5:]
        return render('/main/index.mao')
