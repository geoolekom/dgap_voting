notifications package
=====================
Provides functions for notifications sending and takes care of user's preferences.
You can use this functions to add notifications functionality to your app.


Subpackages
-----------

.. toctree::

Submodules
----------

notifications\.notify module
----------------------------

.. automodule:: notifications.notify
    :members:
    :private-members: _notify_vk, _notify_telegram, _notify_email
    :show-inheritance:

notifications\.models module
----------------------------

.. automodule:: notifications.models
    :members:
    :show-inheritance:

notifications\.admin module
---------------------------

.. automodule:: notifications.admin
    :members:
    :show-inheritance:

notifications\.app module
-------------------------

.. automodule:: notifications.app
    :members:
    :show-inheritance:

notifications\.signals module
-----------------------------
.. todo:: Currently used to send notifications from apps like :mod:`fin_aid` and :mod:`cycle_storage`. It'll be better
to move this functionality directly to that apps. Maybe create submodule ``notifications.py`` in every package?

.. automodule:: notifications.signals
    :members:
    :show-inheritance:

notifications\.templates module
-------------------------------

.. automodule:: notifications.templates
    :members:
    :show-inheritance:

notifications\.tests module
---------------------------

.. automodule:: notifications.tests
    :members:
    :show-inheritance:


Module contents
---------------

.. automodule:: notifications
    :members:
    :show-inheritance:
