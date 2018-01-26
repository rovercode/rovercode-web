.. .. image:: http://localhost:8000/static/images/screenshot.jpg
.. image:: https://rovercode.com/static/images/screenshot.jpg

rovercode
=============
rovercode-web
-------------

:License: GPLv3
.. image:: https://img.shields.io/badge/chat-on%20Slack-41AB8C.svg?style=flat
      :target: http://chat.rovercode.com/
.. image:: https://img.shields.io/badge/join-mailing%20list-yellow.svg?style=flat
      :target: https://1988.onlinegroups.net/groups/rovercode-developers/
.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
      :target: https://github.com/pydanny/cookiecutter-django/
      :alt: Built with Cookiecutter Django
.. image:: https://api.travis-ci.org/rovercode/rovercode-web.svg
      :target: https://travis-ci.org/rovercode/rovercode-web
.. image:: https://coveralls.io/repos/github/rovercode/rovercode-web/badge.svg?branch=development
       :target: https://coveralls.io/github/rovercode/rovercode-web?branch=development


rovercode is easy-to-use package for controlling robots (rovers) that can sense and react to their environment. The Blockly editor makes it easy to program and run your bot straight from your browser. Just drag and drop your commands to drive motors, read values from a variety of supported sensors, and see what your rover sees with the built in webcam viewer.
rovercode runs on any single-board-computer supported by the `Adafruit Python GPIO wrapper library <https://github.com/adafruit/Adafruit_Python_GPIO>`_, including the NextThingCo CHIP, Raspberry Pi, and BeagleBone Black. Once installed, just connect to your rover and get started.

**rovercode is made up of two parts.** rovercode-web (this repo) is the web app that is hosted on the Internet. rovercode (`a different repo <https://github.com/aninternetof/rovercode>`_) is the service that runs on the rover.

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

If anything gives you trouble, see the detailed `cookiecutter-django Docker documentation`_.

.. _`cookiecutter-django Docker documentation`: http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html

Docs
-----
Read the complete docs `here <http://rovercode-web.readthedocs.io/en/latest/>`_.

Contact
--------
Please join the rovercode developer mailing list! `Go here
<https://1988.onlinegroups.net/groups/rovercode-developers/>`_, then
click "register".

Also, we'd love to chat with you! Join the `the rovercode Slack channel
<http://chat.rovercode.com>`_.

You can also email brady@rovercode.com.
