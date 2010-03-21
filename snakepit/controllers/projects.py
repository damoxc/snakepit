import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from snakepit.lib.base import ProjectsBaseController, ProjectsMenuItem, render
from snakepit.model import db, Project

log = logging.getLogger(__name__)

class ProjectsController(ProjectsBaseController):

    def index(self):
        c.projects = db.query(Project).all()
        return render('/projects/index.mao')
    
    def add(self):
        if request.POST:
            c.name = request.POST.get('name')
            c.description = request.POST.get('description')
            c.identifier = request.POST.get('identifier')
            c.homepage = request.POST.get('homepage')
            c.is_public = request.POST.get('is_public') or False
            
            if not c.name:
                c.error = 'You must enter a name'
                return render('/projects/add.mao')

            if not c.identifier:
                c.error = 'You must enter an identifier'
                return render('/projects/add.mao')
            
            project = Project()
            project.name = c.name
            project.description = c.description
            project.homepage = c.homepage
            project.is_public = c.is_public
            project.identifier = c.identifier
            db.add(project)
            db.commit()
            redirect_to(action='show', id=c.identifier)
        
        return render('/projects/add.mao')
    
    def show(self):
        return render('/projects/show.mao')
    
    def activity(self):
        return render('/projects/activity.mao')
    
    def settings(self):
        c.tabs = [
            ('info', 'Information'),
            ('modules', 'Modules'),
            ('members', 'Members'),
            ('versions', 'Versions')
        ]
        return render('/projects/settings.mao')

ProjectsBaseController.register_menu_item('overview',
    ProjectsMenuItem('Overview', 0, controller='projects', action='show'))
ProjectsBaseController.register_menu_item('activity',
    ProjectsMenuItem('Activity', 1, controller='projects', action='activity'))
ProjectsBaseController.register_menu_item('settings',
    ProjectsMenuItem('Settings', 99, controller='projects', action='settings'))
