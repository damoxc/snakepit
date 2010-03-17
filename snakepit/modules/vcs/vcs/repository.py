#
# vcs/repository.py
#
# Copyright (C) 2009 Damien Churchill <damoxc@gmail.com>
#
# Snakepit is free software.
#
# You may redistribute it and/or modify it under the terms of the
# GNU General Public License, as published by the Free Software
# Foundation; either version 3 of the License, or (at your option)
# any later version.
#
# Snakepit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Snakepit. If not, write to:
#   The Free Software Foundation, Inc.,
#   51 Franklin Street, Fifth Floor
#   Boston, MA  02110-1301, USA.
#

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