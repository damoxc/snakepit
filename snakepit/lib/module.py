#
# module.py
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
# deluge is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with deluge.    If not, write to:
#   The Free Software Foundation, Inc.,
#   51 Franklin Street, Fifth Floor
#   Boston, MA  02110-1301, USA.

import sys
from sqlalchemy import Table
from snakepit import model

class ModuleBase(object):
    
    def __init__(self, name):
        self.name = name
    
    def disable(self):
        pass
    
    def enable(self):
        pass
    
    def initialize_model(self, module):
        for attr in dir(module):
            if isinstance(getattr(module, attr), Table):
                setattr(model, attr, getattr(module, attr))
            if hasattr(getattr(module, attr), '_sa_class_manager'):
                setattr(model, attr, getattr(module, attr))
    
    def register_controller(self, name, module):
        sys.modules['snakepit.controllers.' + name] = module