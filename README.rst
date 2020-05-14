|ActionsBadge|_

Introduction
============

``pystethoscope`` is a command line tool to filter and format the events coming
from the MonetDB profiler. The profiler is part of the MonetDB server and works
by emitting two JSON objects: one at the start and one at the end of every MAL
instruction executed. ``pystethoscope`` connects to a MonetDB server process,
reads the objects emitted by the profiler and performs various transformations
specified by the user.

Installation
============

Installation is done via pip:

.. code:: shell

   pip install monetdb-pystethoscope

This project is compatible with Python >= 3.6.

We recommend the use of virtual environments (see `this
primer <https://realpython.com/python-virtual-environments-a-primer/>`__
if you are unfamiliar) for installing and using
``monetdb-pystethoscope``.

Developer notes
===============

``pystethoscope`` is developed using
`Poetry <https://python-poetry.org/>`__, for dependency management and
packaging.

Installation for development
----------------------------

In order to install ``pystethoscope`` do the following:

.. code:: shell

   pip3 install --user poetry
   PYTHON_BIN_PATH="$(python3 -m site --user-base)/bin"
   export PATH="$PATH:$PYTHON_BIN_PATH"

   git clone git@github.com:MonetDBSolutions/monetdb-pystethoscope.git
   cd monetdb-pystethoscope
   poetry install
   poetry run pystethoscope --help

Documentation
=============

For more detailed documentation please see the documentation on `read the docs <https://monetdb-pystethoscope.readthedocs.org>`__.

.. |ActionsBadge| image:: https://github.com/MonetDBSolutions/monetdb-pystethoscope/workflows/Test%20pystethoscope/badge.svg?branch=master
.. _ActionsBadge: https://github.com/MonetDBSolutions/monetdb-pystethoscope/actions
