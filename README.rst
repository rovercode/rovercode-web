.. .. image:: http://localhost:8000/static/images/screenshot.jpg
.. image:: https://rovercode.com/static/images/screenshot.jpg

rovercode
=============
rovercode-web
-------------

:License: GPLv3
.. image:: https://badges.gitter.im/rovercode.png
      :target: https://gitter.im/rovercode/Lobby
.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
      :target: https://github.com/pydanny/cookiecutter-django/
      :alt: Built with Cookiecutter Django
.. image:: https://api.travis-ci.org/rovercode/rovercode-web.svg
      :target: https://travis-ci.org/rovercode/rovercode-web
.. image:: https://coveralls.io/repos/github/rovercode/rovercode-web/badge.svg?branch=development
       :target: https://coveralls.io/github/rovercode/rovercode-web?branch=development

rovercode is an open-source educational robotics platform. Students use our web-based drag-and-drop editor to create
code that listens to the rover's sensors and controls its motors.

rovercode is made up of serveral code repositories. You are currently viewing rovercode-web, the web application 
that provides the drag-and-drop coding interface and user management. To learn about the other pieces of rovercode,
visit our `architecture documentation <https://contributor-docs.rovercode.com/architecture.html>`_, or start at `the
root of rovercode's documentation <https://contributor-docs.rovercode.com>`_.


Setup
-----
Install `docker <https://docs.docker.com/engine/installation/>`_ and `docker-compose <https://docs.docker.com/compose/install/>`_, then

.. code-block:: bash

    $ git clone --recursive https://github.com/aninternetof/rovercode-web.git && cd rovercode-web
    $ sudo docker-compose -f dev.yml build
    $ sudo docker-compose -f dev.yml up
    $ google-chrome localhost:8000

Basic Commands
--------------
rovercode-web runs is built with Django. During development, you can do regular Django things like this:

.. code-block:: bash

    $ docker-compose -f dev.yml run django python manage.py migrate
    $ docker-compose -f dev.yml run django python manage.py createsuperuser

More detailed usage instructions can be found `here in the docs <https://contributor-docs.rovercode.com/rovercode/development/setup.html>`_

Docs
-----
Read the complete docs `here <https://contributor-docs.rovercode.com>`_

Contributing
-------------
Check out the `contributing guide <https://contributor-docs.rovercode.com/contributing.html>`_. 

We'd love to chat with you! Say hello in `our Gitter room
<https://gitter.im/rovercode/Lobby>`_.

You can also email developers@rovercode.com.