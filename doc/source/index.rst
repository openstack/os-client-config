================
os-client-config
================

.. image:: https://governance.openstack.org/tc/badges/os-client-config.svg
    :target: https://governance.openstack.org/tc/reference/tags/index.html

.. warning::
  `os-client-config` has been superceded by `openstacksdk`_. While
  `os-client-config` will continue to exist, it is highly recommended that
  users transition to using `openstacksdk`_ directly.

.. _openstacksdk: https://docs.openstack.org/openstacksdk/latest

`os-client-config` is a library for collecting client configuration for
using an OpenStack cloud in a consistent and comprehensive manner. It
will find cloud config for as few as 1 cloud and as many as you want to
put in a config file. It will read environment variables and config files,
and it also contains some vendor specific default values so that you don't
have to know extra info to use OpenStack

* If you have a config file, you will get the clouds listed in it
* If you have environment variables, you will get a cloud named `envvars`
* If you have neither, you will get a cloud named `defaults` with base defaults

.. toctree::
   :maxdepth: 2

   install/index
   user/index
   reference/index
   contributor/index

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
