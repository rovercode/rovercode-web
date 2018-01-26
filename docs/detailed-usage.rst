detailed usage
===============

using rovercode with a rovercode-web hosted somewhere other than rovercode.com
-------------------------------------------------------------------------------
By default, when rovercode runs, it registers itself with
`https://rovercode.com`. But what if you want to try your changes to rovercode
with `https://beta.rovercode.com`? Or with your local instance of rovercode-web
(as described in the next section)? You can specify the target rovercode-web
url by creating a .env file in your rovercode directory.

.. code-block:: bash

    # first, navigate to the rovercode root diretory (same level as the Dockerfile), then
    $ echo ROVERCODE_WEB_URL=https://beta.rovercode.com/ > .env

When you start rovercode, it will register itself with `beta.rovercode.com`.

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

Set the url of the rovercode-web target to `http://rovercodeweb:8000`. You will
see in the next step that this is the hostname that we assign to our local
rovercode-web container.

.. code-block:: bash

    # first, navigate to the rovercode root diretory (same level as the Dockerfile), then
    $ echo ROVERCODE_WEB_URL=http://rovercodeweb:8000/ > .env

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
http://localhost:8000/mission-control/rover-list. You can now select this rover
in the mission-control interface, and rover commands will be sent to your
rovercode container.

:Attribution: `DEIS blog post <https://deis.com/blog/2016/connecting-docker-containers-1/>`_
