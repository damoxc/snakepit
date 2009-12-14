#
# modules.py
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

# This module is loosely based upon the pluginmanagerbase module within the
# Deluge Bittorrent Client, so props to Andrew Resch for writing the original.

import os
import logging
import pkg_resources

log = logging.getLogger(__name__)

class ModulesManager(object):
    
    def __init__(self, entry_name):
        
        # This is the entry we want to load...
        self.entry_name = entry_name
        
        # Loaded modules
        self.modules = {}
        
        # Enabled modules
        self.enabled_modules = []
        
        # Scan the modules folders for modules
        self.scan_for_modules()
        
        self.enable_module('wiki')
        self.enable_module('vcs')
    
    def scan_for_modules(self):
        """Scans for available modules"""
        
        module_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'modules')
        
        pkg_resources.working_set.add_entry(module_dir)
        self.pkg_env = pkg_resources.Environment([module_dir])
        
        self.available_modules = []
        for name in self.pkg_env:
            log.info('Found module: %s %s',
                self.pkg_env[name][0].project_name,
                self.pkg_env[name][0].version)
            self.available_modules.append(self.pkg_env[name][0].project_name)
    
    def enable_module(self, module_name):
        """Enables a plugin"""
        if module_name not in self.available_modules:
            log.warning("Cannot enable non-existant module %s", module_name)
            return

        if module_name in self.modules:
            log.warning("Cannot enable already enabled module %s", module_name)
            return

        module_name = module_name.replace(" ", "-")
        egg = self.pkg_env[module_name][0]
        egg.activate()
        for name in egg.get_entry_map(self.entry_name):
            entry_point = egg.get_entry_info(self.entry_name, name)
            try:
                cls = entry_point.load()
                instance = cls(module_name.replace("-", "_"))
            except Exception, e:
                log.error("Unable to instantiate plugin!")
                log.exception(e)
                continue
            instance.enable()
            
            module_name = module_name.replace("-", " ")
            self.modules[module_name] = instance
            if module_name not in self.enabled_modules:
                log.debug("Adding %s to enabled_modules list in config",
                    module_name)
                self.enabled_modules.append(module_name)
            log.info("Module %s enabled..", module_name)

    def disable_plugin(self, name):
        """Disables a plugin"""
        try:
            self.plugins[name].disable()
            component.deregister(self.plugins[name].plugin.get_component_name())
            del self.plugins[name]
            self.config["enabled_plugins"].remove(name)
        except KeyError:
            log.warning("Plugin %s is not enabled..", name)

        log.info("Plugin %s disabled..", name)

    def get_plugin_info(self, name):
        """Returns a dictionary of plugin info from the metadata"""
        info = {}.fromkeys(METADATA_KEYS)
        last_header = ""
        cont_lines = []
        for line in self.pkg_env[name][0].get_metadata("PKG-INFO").splitlines():
            if not line:
                continue
            if line[0] in ' \t' and (len(line.split(":", 1)) == 1 or line.split(":", 1)[0] not in info.keys()):
                # This is a continuation
                cont_lines.append(line.strip())
            else:
                if cont_lines:
                    info[last_header] = "\n".join(cont_lines).strip()
                    cont_lines = []
                if line.split(":", 1)[0] in info.keys():
                    last_header = line.split(":", 1)[0]
                    info[last_header] = line.split(":", 1)[1].strip()
        return info