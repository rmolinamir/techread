"""
The `__init__.py` file is a special file in Python that is used to mark a directory as a Python package.
It can contain initialization code for the package, or it can be an empty file.

If the `__init__.py` file contains code, then that code will be executed when the package is imported.
This code can be used to set up the package's environment, such as loading data or creating objects.

If the `__init__.py` file is empty, then it will still be executed when the package is imported.
However, it will do nothing by default.

In general, it is a good idea to put any initialization code for a package in the `__init__.py` file.
This will ensure that the code is executed whenever the package is imported, and it will help to keep
the code organized.
"""
from .celery import app as celery_app

# This will make sure the app is always imported when Django starts so that shared_task will use this app.
__all__ = ("celery_app",)
