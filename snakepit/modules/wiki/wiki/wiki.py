#
# wiki.py
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

from snakepit.lib.module import ModuleBase

class WikiModule(ModuleBase):
    
    def disable(self):
        super(WikiModule, self).disable()
        import controller
        self.unregister_controller(controller)
    
    def enable(self):
        super(WikiModule, self).enable()
        import model
        self.initialize_model(model)

        import controller
        self.register_controller('wiki', controller)