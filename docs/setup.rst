Setup
===========

Install `docker <https://docs.docker.com/engine/installation/>`_ and `docker-compose <https://docs.docker.com/compose/install/>`_, then

.. code-block:: bash

    $ git clone --recursive https://github.com/aninternetof/rovercode-web.git && cd rovercode-web
    $ sudo docker-compose -f dev.yml build
    $ sudo docker-compose -f dev.yml up
    $ google-chrome localhost:8000

Basic Commands
----------------
rovercode-web is built with Django. During development, you can do regular Django things like this:

.. code-block:: bash

    $ docker-compose -f dev.yml run django python manage.py migrate
    $ docker-compose -f dev.yml run django python manage.py createsuperuser

Running the Tests and Coverage
---------------------------------

.. code-block:: bash

    $ docker-compose -f dev.yml run django pytest

Running the Linter
---------------------------------

.. code-block:: bash

    $ docker-compose -f dev.yml run django prospector

Building the Docs
-------------------

.. code-block:: bash

    $ docker-compose -f dev.yml run django make -C docs html