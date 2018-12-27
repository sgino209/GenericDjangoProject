# (c) Shahar Gino, April-2018, sgino209@gmail.com

(*) References:  https://docs.djangoproject.com

(*) Note: Python 2.7 cannot be used with Django 2.0 (The Django 1.11.x series is the last to support Python 2.7).

(*) Note: The file requirements.txt can be invoked by:  % pip3 freeze > requirements.txt 

(*) Main flow diagram:
                    -------------  FWD the request to       --------------
    HTTP request -->|   URLs    |-------------------------->|    View    |---> HTTP response
    (HTML)          | (urls.py) |  appropriate view  ------>| (views.py) |     (HTML)
                    -------------                    |   -->|            |
                    ---------------                  |   |  --------------
                    |   Models    |<------------------   |                               
                    | (models.py) | read/write data    Template                          
                    ---------------                    (*.html)

------------------------------------------------------------------------------------------------------------------------------------------
 ____            _
| __ )  __ _ ___(_) ___ ___
|  _ \ / _` / __| |/ __/ __|
| |_) | (_| \__ \ | (__\__ \
|____/ \__,_|___/_|\___|___/

(*) Django installation:
    https://docs.djangoproject.com/en/2.1/intro/install/

(*) Check Django version:
    % python -m django --version

(*) Start a new project:
    % cd MyProject                       ----> It's recommended to make this folder a git repository
    % django-admin startproject mysite   ----> This will create a 'mysite' directory in your current directory
    % cd mysite
    % python manage.py startapp catalog  ----> Creates an app called 'catalog'

(*) FileStructure:

        mysite/mysite
            __init__.py
            __pycache__/
            settings.py
            urls.py
            wsgi.py
        
        mysite/catalog
            __init__.py
            admin.py
            apps.py
            migrations/
            models.py
            tests.py
            views.py

(*) Switch for VirtualEnv:
    % bash
    % virtualenv -p $(which python3) env
    % source env/bin/activate
    end with:  deactivate

(*) First time setup:
    % pip install -r requirements.txt
    % python3 manage.py makemigrations
    % python3 manage.py migrate --run-syncdb
    % python3 manage.py createsuperuser
    % python3 manage.py runserver
    browse to http://127.0.0.1:8000/
    browse to http://127.0.0.1:8000/admin

(*) Reloading the server after code-changes:
    % python3 manage.py makemigrations
    % python3 manage.py migrate --run-syncdb
    % python3 manage.py runserver

(*) Starting fresh (no history):
    % rm db.sqlite3
    % rm -rf catalog/__pycache__
    % python3 manage.py makemigrations
    % python3 manage.py migrate --run-syncdb
    % python manage.py shell < db_init.py  
    % python3 manage.py runserver

    Note:
    A superuser can also be generated explicitly with:
    % python3 manage.py createsuperuser

(*) Database inspection (useful, show all model attributes):
    % python manage.py inspectdb

(*) Connect to django shell:
    % python manage.py shell       --> Standard shell
    % python manage.py shell_plus  --> Extended shell (recommended)

(*) Static handling (e.g. images, JavaScript, CSS):
    (-) Important variables in settings.py:
        --> STATIC_URL:  specifies what url should static files map to under
        --> STATICFILES_DIRS:  specifies all the folders on your system where Django should look for static files
        --> STATIC_ROOT:  specifies where Django will copy all the static files to and not where the static files are already at
    (-) STATICFILES_STORAGE can replace STATICFILES_DIRS, e.g. see http://whitenoise.evans.io/en/stable
    (-) Update static files (copy all the static files from from all files within STATICFILES_DIRS to STATIC_ROOT):
    % python3 manage.py collectstatic

(*) Self-testing:
    % python3 manage.py test

    (-) In case of getting errors similar to: ValueError: Missing staticfiles manifest entry 
        Try to:  % python3 manage.py collectstatic

------------------------------------------------------------------------------------------------------------------------------------------
 _   _                _
| | | | ___ _ __ ___ | | ___   _
| |_| |/ _ \ '__/ _ \| |/ / | | |
|  _  |  __/ | | (_) |   <| |_| |
|_| |_|\___|_|  \___/|_|\_\\__,_|

(*) Deploy on Heroku server (with Heroku CLI, assuming app is already in some Git repo):
    Reference:  https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Deployment
    % heroku login
    % heroku create
    % git push heroku master
    % heroku run python manage.py migrate
    % heroku run python manage.py createsuperuser
    % heroku open

    (-) Note: it might be needed to migrate with the "--run-syncdb" flag

(*) Check the add-ons to the app:
    % heroku addons

(*) Check the configutarion variables:
    % heroku config

(*) Set configutarion variables (e.g. DJANGO_DEBUG and DJANGO_SECRET_KEY, use your own secret key...):
    % heroku config:set DJANGO_SECRET_KEY='cg#p$g+j9tax!#a3cup@1$8obt2_+&k3q+pmu)5%asj6yjpkag'
    % heroku config:set DJANGO_DEBUG=

(*) Heroku app info:
    % heroku pg:info

(*) Heroku database reset (be careful..):
    % heroku pg:reset DATABASE [--confirm <APP_NAME>]
    % heroku run python manage.py migrate
    % heroku run python manage.py migrate --run-syncdb
    
    Start Fresh:
    % heroku run python manage.py createsuperuser
    
    Load initial data (including groups and users):
    % heroku run python manage.py shell < db_init.py  

(*) Update local git and deploy to Git and to Heroku server:
    % git add <files>
    % git commit -m '<comment>'
    % git push origin master
    % git push heroku master

(*) Debug with Heroku CLI:
    % heroku logs                              ---> Show current logs
    % heroku logs --tail                       ---> Show current logs and keep updating with any new results
    % heroku config:set DEBUG_COLLECTSTATIC=1  ---> Add additional logging for collectstatic (this tool is run automatically during a build)
    % heroku ps                                ---> Display dyno status

(*) Connect to Heroku shell:
    % heroku run bash
    % ...
    % exit

(*) Heroku CLI update:
    % heroku update

(*) Heroku Automated Certification Management (requires Hobby+ plan):
    % heroku certs:auto:enable   ---> Enable
    % heroku certs:auto          ---> Check status

