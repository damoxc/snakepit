import logging

from pylons import config, request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from snakepit.lib.base import ProjectsBaseController, ProjectsMenuItem, connect, render
from snakepit.model import db, Project, WikiPage

log = logging.getLogger(__name__)

DEFAULT = """
= ${title} =
"""

class WikiController(ProjectsBaseController):
    
    def edit(self):
        title = request.urlvars.get('page')
        if not title:
            title = c.project.wiki.start_page

        page = db.query(WikiPage).filter_by(title=title,
                                            wiki_id=c.project.wiki.id).first()
        c.page = page
        c.title = title
        if not page:
            c.contents = DEFAULT % {'title': title}
        return render('/wiki/edit.mao')

    def view(self):
        title = request.urlvars.get('page')
        if not title:
            title = c.project.wiki.start_page

        page = db.query(WikiPage).filter_by(title=title,
                                            wiki_id=c.project.wiki.id).first()
        c.page = page
        c.title = title
        if not page:
            c.contents = DEFAULT % {'title': title}
        return render('/wiki/view.mao')

connect('/wiki/{project}', controller='wiki', action='view', page=None)
connect('/wiki/{project}/{page:.*?}/edit', controller='wiki', action='edit')
connect('/wiki/{project}/{page:.*?}', controller='wiki', action='view')
ProjectsBaseController.register_menu_item('wiki',
    ProjectsMenuItem('Wiki', controller='wiki', action='view'))