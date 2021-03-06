from AdvancedDevelopment.wsgi import application as app

# App Engine by default looks for a main.py file at the root of the app
# directory with a WSGI-compatible object called app.
# This file imports the WSGI-compatible object of your Django app,
# application from mysite/wsgi.py and renames it app so it is discoverable by
# App Engine without additional configuration.
# Alternatively, you can add a custom entrypoint field in your app.yaml:
# entrypoint: gunicorn -b :$PORT mysite.wsgi
# https://stackoverflow.com/questions/52395695/modulenotfounderror-no-module-named-main-when-attempting-to-start-service
