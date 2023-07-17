from xnbtd.settings.prod import *  # noqa:F401,F403


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'xnbtd.sqlite3',
        'DEBUG_NAME': 'xnbtd-debug.sqlite3',
    },
}
