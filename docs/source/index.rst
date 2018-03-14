============
Meerkat Nest
============

Meerkat Nest preprocesses, stores and forwards form-based data based on its configurations. The default role of Nest in
the Meerkat stack is to receive raw submission data from ODK Aggregate, process it and to forward it to Meerkat Drill
for delivery.

We use flaskRESTful to create the API and flask-sqlalchemy to access the db

---------
Structure
---------

__init__.py - Sets up the flask app and all the URLs

util/__init__.py - Various utility methods

resources/: Folder containing the following files:

* upload_data.py - Endpoint for uploading a single data point
* amend_data.py - *NOT YET FULLY IMPLEMENTED* Endpoint for amending previously uploaded submissions
* deactivate_data.py - *NOT YET FULLY IMPLEMENTED* Endpoint for deactivating previously uploaded submissions
* download_data.py - *NOT YET FULLY IMPLEMENTED* Endpoint for accessing previously uploaded submissions

---------
Nest URLs
---------

.. autoflask:: meerkat_nest:app
   :undoc-static:

-------
Testing
-------

When new features for Meerkat Nest are developed they should be properly tested. The test are done using the python unittest library.
All the tests are in the meerkat_nest/test directory.

**Upload unit test functions**

.. automodule:: meerkat_nest.test.test_upload
    :members:

**Pipeline test functions**

.. automodule:: meerkat_nest.test.test_pipeline
    :members:

------------------
Utility Functions
------------------

Meerkat Nest utility functions

.. automodule:: meerkat_nest.util
   :members:
