Rovercode API
=============

.. image:: https://img.shields.io/badge/License-GPLv3-blue.svg
      :target: https://www.gnu.org/licenses/gpl-3.0
.. image:: https://img.shields.io/badge/chat-zulip-brightgreen.svg?style=flat
      :target: https://rovercode.zulipchat.com/
.. image:: https://img.shields.io/badge/board-zenhub-blue.svg?style=flat
      :target: https://app.zenhub.com/workspaces/rovercode-development-5c7e819df524621425116d03/boards
.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
      :target: https://github.com/pydanny/cookiecutter-django/
      :alt: Built with Cookiecutter Django
.. image:: https://api.travis-ci.org/rovercode/rovercode-web.svg
      :target: https://travis-ci.org/rovercode/rovercode-web
.. image:: https://coveralls.io/repos/github/rovercode/rovercode-web/badge.svg?branch=alpha
       :target: https://coveralls.io/github/rovercode/rovercode-web?branch=alpha

rovercode is an open-source educational robotics platform. Students use our web-based drag-and-drop editor to create
code that listens to the rover's sensors and controls its motors.

rovercode is made up of several code repositories. You are currently viewing rovercode-web, the web application backend
that provides the API for the `frontend <https://github.com/rovercode/rovercode-ui/>`_. To learn about the other pieces of rovercode,
visit our `architecture documentation <https://contributor-docs.rovercode.com/architecture.html>`_, or start at `the
root of Rovercode's documentation <https://contributor-docs.rovercode.com>`_.


Setup
-----
Install `docker <https://docs.docker.com/engine/installation/>`_ and `docker-compose <https://docs.docker.com/compose/install/>`_, then

.. code-block:: bash

    $ git clone --recursive https://github.com/rovercode/rovercode-web.git && cd rovercode-web
    $ sudo docker-compose -f dev.yml build
    $ sudo docker-compose -f dev.yml up
    $ google-chrome localhost:8000/docs

Basic Commands
--------------
rovercode-web is built with Django. During development, you can do regular Django things like this:

.. code-block:: bash

    $ docker-compose -f dev.yml run django python manage.py migrate
    $ docker-compose -f dev.yml run django python manage.py createsuperuser

More detailed usage instructions can be found `here in the docs <https://contributor-docs.rovercode.com/rovercode-web/development/detailed-usage.html>`_

Docs
-----
Read the complete docs `here <https://contributor-docs.rovercode.com>`_

Contributing
-------------
Help make rovercode better! Check out the `contributing guide <https://contributor-docs.rovercode.com/getting_started.html>`_. 

We'd love to chat with you! Say hello in `our chat room
<https://rovercode.zulipchat.com/>`_.
