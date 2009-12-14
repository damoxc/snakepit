import logging

from pylons import config, request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from snakepit.lib.base import ProjectsBaseController, ProjectsMenuItem, connect, render
from snakepit.model import db, Project

log = logging.getLogger(__name__)

class RepositoryController(ProjectsBaseController):
    
    def view(self):
        return render('/repository/view.mao')

connect('/repository/{project}', controller='repository', action='view')
ProjectsBaseController.register_menu_item('repository',
    ProjectsMenuItem('Repository', 5, controller='repository', action='view'))