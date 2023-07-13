========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |github-actions|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/python-geophires-x-client/badge/?style=flat
    :target: https://python-geophires-x-client.readthedocs.io/
    :alt: Documentation Status

.. |github-actions| image:: https://github.com/softwareengineerprogrammer/python-geophires-x-client/actions/workflows/github-actions.yml/badge.svg
    :alt: GitHub Actions Build Status
    :target: https://github.com/softwareengineerprogrammer/python-geophires-x-client/actions

.. |codecov| image:: https://codecov.io/gh/softwareengineerprogrammer/python-geophires-x-client/branch/main/graphs/badge.svg?branch=main
    :alt: Coverage Status
    :target: https://app.codecov.io/github/softwareengineerprogrammer/python-geophires-x-client

.. |version| image:: https://img.shields.io/pypi/v/geophires-x-client.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/geophires-x-client

.. |wheel| image:: https://img.shields.io/pypi/wheel/geophires-x-client.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/geophires-x-client

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/geophires-x-client.svg
    :alt: Supported versions
    :target: https://pypi.org/project/geophires-x-client

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/geophires-x-client.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/geophires-x-client

.. |commits-since| image:: https://img.shields.io/github/commits-since/softwareengineerprogrammer/python-geophires-x-client/v0.0.3.svg
    :alt: Commits since latest release
    :target: https://github.com/softwareengineerprogrammer/python-geophires-x-client/compare/v0.0.3...main



.. end-badges

Wrapper client for GEOPHIRES-X

* Free software: MIT license

Installation
============

::

    pip install geophires-x-client

You can also install the in-development version with::

    pip install https://github.com/softwareengineerprogrammer/python-geophires-x-client/archive/main.zip


Documentation
=============


* https://github.com/softwareengineerprogrammer/python-geophires-x-client/
* https://github.com/softwareengineerprogrammer/python-geophires-x/


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
