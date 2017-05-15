detailed usage
===============

develop rovercode and rovercode-web on the same machine at the same time
--------------------------------------------------------------------------


Get, build, and bring up rovercode-web as usual:

.. code-block:: bash

    $ git clone --recursive https://github.com/aninternetof/rovercode-web.git && cd rovercode-web
    $ sudo docker-compose -f dev.yml build
    $ sudo docker-compose -f dev.yml up
    $ google-chrome localhost:8000

Get and build rovercode as usual:

.. code-block:: bash

    $ git clone --recursive https://github.com/aninternetof/rovercode.git && cd rovercode
    $ sudo docker build -t rovercode .

Open `app.py` and comment/uncomment the `ROVERCODE_WEB_REG_URL` lines to select
`rovercodeweb:8000`. You want it to end up like this:

.. code-block:: python

    ''' Default. Use with rovercode-web running at rovercode.com '''
    #ROVERCODE_WEB_REG_URL = "https://rovercode.com/mission-control/rovers/"
    ''' Uncomment this line to use with rovercode-web running at beta.rovercode.com '''
    #ROVERCODE_WEB_REG_URL = "https://beta.rovercode.com/mission-control/rovers/"
    ''' Uncomment this line to use with a local rovercodeweb docker container '''
    ROVERCODE_WEB_REG_URL = "http://rovercodeweb:8000/mission-control/rovers/"


Finally, when you bring up the rovercode container, add a `link` flag to allow access
between this container and your rovercode-web container.

.. code-block:: bash

    $ sudo docker run -t --link rovercodeweb_django_1:rovercodeweb --net rovercodeweb_default --name rovercode -v $PWD:/var/www/rovercode -p 80:80 -d rovercode

docker-compose named it `rovercodeweb_django_1`, but notice that
we used a colon to rename it simply `rovercodeweb`. This is necessary,
because this becomes the hostname, and Django does not like underscores in
hostname headers.

We also had to add a `net rovercodeweb_default` flag, because docker-compose put rovercode-web on
its own network instead of on the default one. (If you're curious, you can find
its name using the command `sudo docker network ls`.)

rovercode is now running, and you can see that it has registered itself with
your local rovercodeweb container by going to
http://localhost:8000/mission-control/rovers. You can now select this rover
in the mission-control interface, and rover commands will be sent to your
rovercode container.

:Attribution: `DEIS blog post <https://deis.com/blog/2016/connecting-docker-containers-1/>`_
