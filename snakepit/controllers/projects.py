import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from snakepit.lib.base import BaseController, render
from snakepit.model import db, Project

log = logging.getLogger(__name__)

class ProjectsController(BaseController):

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
        project = request.urlvars.get('id')
        c.project = db.query(Project).filter_by(identifier=project).first()
        return render('/projects/show.mao')
        