"""The base Controller API

Provides the BaseController class for subclassing.
"""

from pylons import config, tmpl_context as c, request
from pylons.controllers import WSGIController
from pylons.decorators.secure import abort
from pylons.templating import render_mako as render

import routes

from snakepit.model import db, Project
from snakepit.lib.helpers import url_for

def connect(*args, **kwargs):
    return config['routes.map'].connect(*args, **kwargs)

_url_for = routes.url_for
def url_for(*args, **kwargs):
    remove_keys = [k for k in request.urlvars.keys() if k not in ('controller', 'action', 'project')]
    if 'controller' in kwargs:
        tmp = dict(zip(remove_keys, (None,) * len(remove_keys)))
        tmp.update(kwargs)
        kwargs = tmp
    return _url_for(*args, **kwargs)
routes.url_for = url_for

class BaseController(WSGIController):
    
    def __before__(self):
        pass

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        try:
            return WSGIController.__call__(self, environ, start_response)
        finally:
            db.remove()
    
    def __after__(self):
        pass

class ProjectsBaseController(BaseController):
    
    menu_items = []
    
    def __before__(self):
        super(ProjectsBaseController, self).__before__()
        c.menu_items = ProjectsBaseController.menu_items
        c.menu_items.sort()
        
        self.project_name = request.urlvars.get('project')
        c.url = request.path_qs
        
        project = request.urlvars.get('project')
        if project:
            c.project = db.query(Project).filter_by(identifier=project).first()
    
    @classmethod
    def register_menu_item(cls, name, menu_item):
        cls.menu_items.append(menu_item)
    
    @classmethod
    def deregister_menu_item(cls, name, menu_item):
        cls.menu_items.remove(menu_item)

class ProjectsMenuItem(object):
    
    def __init__(self, label, weight, class_='', **urlargs):
        self.label = label
        self.weight = weight
        self.class_ = class_
        self.urlargs = urlargs
    
    def __cmp__(self, other):
        return cmp(self.weight, other.weight)
    
    def get_url(self, project):
        url_args = self.urlargs.copy()
        url_args['project'] = project
        return url_for(**url_args)
