import logging

from pylons import config, request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from snakepit.lib.base import ProjectsBaseController, ProjectsMenuItem, connect, render
from snakepit.model import db, Project

log = logging.getLogger(__name__)

class WikiController(ProjectsBaseController):

    def view(self):
        return render('/wiki/view.mao')

connect('/wiki/{project}', controller='wiki', action='view', page=None)
connect('/wiki/{project}/{page:.*?}', controller='wiki', action='view')
connect('/wiki/{project}/{page:.*?}/{action}', controller='wiki')
ProjectsBaseController.register_menu_item('wiki',
    ProjectsMenuItem('Wiki', controller='wiki', action='view'))