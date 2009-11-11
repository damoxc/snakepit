"""The base Controller API

Provides the BaseController class for subclassing.
"""
from pylons import config, tmpl_context as c, request
from pylons.controllers import WSGIController
from pylons.decorators.secure import abort
from pylons.templating import render_mako as render

from snakepit.model import db
from snakepit.lib.component import register

def connect(*args, **kwargs):
    return config['routes.map'].connect(*args, **kwargs)

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
    
    @classmethod
    def register_menu_item(cls, menu_item):
        cls.menu_items.append(menu_item)
    
    @classmethod
    def deregister_menu_item(cls, menu_item):
        cls.menu_items.remove(menu_item)

register('ProjectsBaseController', ProjectsBaseController)