This file is for you to describe the snakepit application. Typically
you would include information such as the information below:

Dependencies
============

Pylons = 0.9.7
Routes >= 1.10
SQLAlchemy >= 0.5

Installation and Setup
======================

Install ``snakepit`` using easy_install::

    easy_install snakepit

Make a config file as follows::

    paster make-config snakepit config.ini

Tweak the config file as appropriate and then setup the application::

    paster setup-app config.ini

Then you are ready to go.
