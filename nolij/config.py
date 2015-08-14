class Config(object):
    PORT = 12345
    SECRET_KEY = 'woahimabadass'


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgres://aditya:temp@localhost:5432/nolij"
    SECRET_KEY = 'woahimabadass'
    PORT = 5000
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_PASSWORD_SALT = SECRET_KEY
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,

        'formatters': {
            'console': {
                'format': '[%(asctime)s][%(levelname)s] %(filename)s: | %(message)s',
                'datefmt': '%H:%M:%S',
            },
        },

        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'console',
                'stream': 'ext://sys.stderr'
            },
        },

        'loggers': {
            '': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True,
            },
        },
    }
    GUNICORN = {
        'bind': '%s:%s' % ('0.0.0.0', PORT),
        'worker-class': 'gevent',
        'workers': 1
    }
