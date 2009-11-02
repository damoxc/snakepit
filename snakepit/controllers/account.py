import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from snakepit.lib.base import BaseController, render

log = logging.getLogger(__name__)

class AccountController(BaseController):

    def login(self):
        return render('/account/login.mao')