Developer notes
===============

``stethoscope`` is developed using
`Poetry <https://python-poetry.org/>`__, for dependency management and
packaging.

Installation for development
----------------------------

In order to install ``stethoscope`` do the following:

.. code:: shell

   pip3 install --user poetry
   PYTHON_BIN_PATH="$(python3 -m site --user-base)/bin"
   export PATH="$PATH:$PYTHON_BIN_PATH"

   git clone git@github.com:MonetDBSolutions/monetdb-pystethoscope.git
   cd monetdb-pystethoscope
   poetry install
   poetry run stethoscope --help

On 30/04/2020 `pymonetdb
1.3.1 <https://github.com/gijzelaerr/pymonetdb/releases/tag/1.3.1>`__
was released, which includes a feature needed to connect transparently
to the MonetDB server. If you have installed the development version of
``stethoscope``, before that date you need to update:

.. code:: shell

   cd monetdb-pystethoscope
   git pull
   poetry update
