Docker
======

It is possible to use this plugin from a throw-away docker container. This is done with the help of
`whalebrew <https://github.com/bfirsh/whalebrew>`_.

How
===

Build a docker image:

.. code-block::

    $ make docker

Install my very own brew tap:

.. code-block::

    $ brew tap themalkolm/brew
    $ brew update

Now you can install whalebrew:

.. code-block::

    $ brew install whalebrew

Verify whalebrew installed correctly:

.. code-block::

    $ whalebrew install whalebrew/whalesay
    $ whalesay Hello
     _______ 
    < Hello >
     ------- 
        \
         \
          \
                        ##         .
                  ## ## ##        ==
               ## ## ## ## ##    ===
           /"""""""""""""""""\___/ ===
      ~~~ {~~ ~~~~ ~~~ ~~~~ ~~~ ~ /  ===- ~~~
           \______ o           __/
             \    \         __/
              \____\_______/    

Now you can install docker image as a whalebrew command (note the version!):

.. code-block::

    $ whalebrew install local/ofxstatement-lfs:0.0.1

Now you have a whalebrew command to run this plugin.

.. code-block::

    $ ofxstatement-lfs -h
    $ ofxstatement-lfs list-plugins

Well, yes even though it is named ofxstatement-lfs, in reality it is nothing
more but an ofxstatement installation with ofxstatement-lfs plugin
pre-installed:

.. code-block::

    $ ofxstatement-lfs convert -t lfs Kontoutdrag.xls statements.ofx
