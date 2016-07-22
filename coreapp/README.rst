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
    sudo apt-get install python-dev
    sudo apt-get install libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk
    sudo pip install django-simple-captcha
djangorestframework
markdown       # Markdown support for the browsable API.
django-filter
mongoengine
django-multiselectfield

sudo apt-get install libgdal-dev

installing rabbitMQ
https://www.rabbitmq.com/install-debian.html
sudo invoke-rc.d rabbitmq-server stop/start/etc


pip install django-celery
Add djcelery to INSTALLED_APPS.
python manage.py migrate djcelery
python manage.py syncdb
Configure celery to use the django-celery backend.

For the database backend you must use:

app.conf.update(
    CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend',
)
For the cache backend you can use:

app.conf.update(
    CELERY_RESULT_BACKEND='djcelery.backends.cache:CacheBackend',
)
If you have connected Celery to your Django settings then you can add this directly into your settings module (without the app.conf.update part)
