Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "coreapp" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'coreapp',
    ]

2. Include the coreapp URLconf in your project urls.py like this::

    url(r'^coreapp/', include('coreapp.urls')),

3. Run `python manage.py migrate` to create the coreapp models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a coreapp (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/coreapp/ to participate in the coreapp.


Requirements :
django-simple-captcha
djangorestframework
markdown       # Markdown support for the browsable API.
django-filter
mongoengine
django-multiselectfield

sudo apt-get install libgdal-dev