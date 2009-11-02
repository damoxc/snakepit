import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from snakepit.lib.base import BaseController, render

log = logging.getLogger(__name__)

class ProjectsController(BaseController):

    def index(self):
        return render('/projects/index.mao')