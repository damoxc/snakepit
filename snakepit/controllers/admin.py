import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from snakepit.lib.base import BaseController, render

log = logging.getLogger(__name__)

class AdminController(BaseController):

    def index(self):
        return render('/admin/index.mao')
    
    def projects(self):
        return render('/admin/projects.mao')