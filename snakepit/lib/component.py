#
# snakepit/lib/component.py
#
# Copyright (C) 2007, 2008 Andrew Resch <andrewresch@gmail.com>
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
# along with snakepit. If not, write to:
# 	The Free Software Foundation, Inc.,
# 	51 Franklin Street, Fifth Floor
# 	Boston, MA  02110-1301, USA.
#

import logging

log = logging.getLogger(__name__)

class ComponentRegistry:
    def __init__(self):
        self.components = {}
        self.depend = {}

    def register(self, name, obj, depend):
        """Registers a component.. depend must be list or None"""
        log.debug("Registered %s with ComponentRegistry..", name)
        self.components[name] = obj
        if depend != None:
            self.depend[name] = depend

    def get(self, name):
        """Returns a reference to the component 'name'"""
        return self.components[name]

    def start(self):
        """Starts all components"""
        for component in self.components.keys():
            self.start_component(component)

    def start_component(self, name):
        """Starts a component"""
        # Check to see if this component has any dependencies
        if self.depend.has_key(name):
            for depend in self.depend[name]:
                self.start_component(depend)

        # Only start if the component is stopped.
        if self.components[name].get_state() == \
            COMPONENT_STATE.index("Stopped"):
            log.debug("Starting component %s..", name)
            self.components[name].start()
            self.components[name]._start()

    def stop(self):
        """Stops all components"""
        for component in self.components.keys():
            self.stop_component(component)

    def stop_component(self, component):
        if self.components[component].get_state() != \
                COMPONENT_STATE.index("Stopped"):
            log.debug("Stopping component %s..", component)
            self.components[component].stop()
            self.components[component]._stop()

    def pause(self):
        """Pauses all components.  Stops calling update()"""
        for component in self.components.keys():
            self.pause_component(component)

    def pause_component(self, component):
        if self.components[component].get_state() not in \
            [COMPONENT_STATE.index("Paused"), COMPONENT_STATE.index("Stopped")]:
            log.debug("Pausing component %s..", component)
            self.components[component]._pause()

    def resume(self):
        """Resumes all components.  Starts calling update()"""
        for component in self.components.keys():
            self.resume_component(component)

    def resume_component(self, component):
        if self.components[component].get_state() == COMPONENT_STATE.index("Paused"):
            log.debug("Resuming component %s..", component)
            self.components[component]._resume()

    def update(self):
        """Updates all components"""
        for component in self.components.keys():
            # Only update the component if it's started
            if self.components[component].get_state() == \
                COMPONENT_STATE.index("Started"):
                self.components[component].update()

        return True

    def shutdown(self):
        """Shuts down all components.  This should be called when the program
        exits so that components can do any necessary clean-up."""
        # Stop all components first
        self.stop()
        for component in self.components.keys():
            log.debug("Shutting down component %s..", component)
            try:
                self.components[component].shutdown()
            except Exception, e:
                log.debug("Unable to call shutdown()")
                log.exception(e)


_ComponentRegistry = ComponentRegistry()

def register(name, obj, depend=None):
    """Registers a component with the registry"""
    _ComponentRegistry.register(name, obj, depend)

def get(component):
    """Return a reference to the component"""
    return _ComponentRegistry.get(component)