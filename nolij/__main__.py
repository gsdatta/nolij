from nolij.app import create_app
import gunicorn
import gunicorn.app.base
import sys
from gunicorn.six import iteritems
import multiprocessing

ENVS = ['dev', 'prod']

def print_usage():
    print "usage: run.py <%s>" % '|'.join(ENVS)


def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1


class GunicornNolij(gunicorn.app.base.BaseApplication):

    """
    This is a wrapper for a Gunicorn application in order to simplify
    running Nolij behind gunicorn.
    """

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(GunicornNolij, self).__init__()

    def load_config(self):
        config = dict([(key, value) for key, value in iteritems(self.options)
                       if key in self.cfg.settings and value is not None])
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def init(self, parser, opts, args):  # noqa
        """ Gunicorn/pylint complains without this though unused """
        return None

    def load(self):
        return self.application


def main():
    if len(sys.argv) < 2:
        print "usage: run.py <%s>" % '|'.join(ENVS)
        sys.exit()

    if sys.argv[1] not in ENVS:
        print_usage()
        sys.exit(1)

    app = create_app(__name__, sys.argv[1])

    # http://flask.pocoo.org/docs/0.10/deploying/wsgi-standalone/
    gunicorn_opts = app.config['GUNICORN']

    # If the number of workers is not set, then let's choose a sane number
    if 'workers' not in gunicorn_opts:
        gunicorn_opts['workers'] = number_of_workers()

    GunicornNolij(app, gunicorn_opts).run()


if __name__ == '__main__':
    main()
