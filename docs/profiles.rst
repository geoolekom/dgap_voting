profiles package
================

* Handling OAuth-2 authorization and user authentication.
* Verification of students.

User can log in (and sign up) through one of the available OAuth providers (VK, Google). For each social auth a new user
(instance of :class:`django.contrib.auth.models.User`) is created. This process is handled by :const:`core.settings.SOCIAL_AUTH_PIPELINE`.
For each new user an :class:`profiles.models.UserProfile` is created (See :mod:`profiles.signals`).

:class:`profiles.models.StudentInfo` stores info about all DGAP students (received from administration). If system can
associate logged user with DGAP student (:func:`profiles.psa.approve_student`), then link to :class:`UserProfile` is created.

Each student have only one :class:`StudentInfo` but can have multile :class:`User` (one for each OAuth provider)

.. todo:: Refactoring in auth system needed. Now multiple accounts of singe student are linked through User -> UserProfile -> StudentInfo.
   Super stupid.

profiles\.models module
-----------------------

.. automodule:: profiles.models
    :members:
    :show-inheritance:


profiles\.admin module
----------------------

.. automodule:: profiles.admin
    :members:
    :show-inheritance:

profiles\.psa module
--------------------

.. automodule:: profiles.psa
    :members:
    :show-inheritance:

profiles\.app module
--------------------

.. automodule:: profiles.app
    :members:
    :show-inheritance:

profiles\.signals module
------------------------

.. automodule:: profiles.signals
    :members:
    :show-inheritance:

profiles\.tests module
----------------------

.. automodule:: profiles.tests
    :members:
    :undoc-members:
    :show-inheritance:

profiles\.urls module
---------------------

.. automodule:: profiles.urls
    :members:
    :show-inheritance:

profiles\.views module
----------------------

.. automodule:: profiles.views
    :members:
    :show-inheritance:


Module contents
---------------

.. automodule:: profiles
    :members:
    :show-inheritance:
