"""This package provides basic functionality for embedding website page as a community app in VK's IFrame

Installation
------------

1. Add ``vk_iframe`` to INSTALLED_APPS
2. Set valid VK_APP_SECRET in settings

Static files & templates
------------

templates/iframe.html
^^^^^^^^^^^^^^^^^^^^^
Modification of ``core/base.html`` without nav menu and with vk js sdk included.
Used by :class:`vk_app.views.VkIframeMixin`.

static/vk.js
^^^^^^^^^^^^
Script for work with js skd. For example, is responsible for generating new community widget.

May be used to show "Please allow messages from our community" dialog & so on.
"""