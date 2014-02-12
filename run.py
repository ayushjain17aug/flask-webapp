"""Web application

Usage:
    run.py test
    run.py server
    run.py server <host>:<port>

Options:
    server   Run server. By default: localhost:5000
    test     Run all unittests

"""
import os

from docopt import docopt

from app.views.base import app
from config import settings


HOST = 'localhost:5000'


def run_server(host=None):
    if host is None:
        host = HOST

    host, port = host.split(':')

    app.run(debug=settings.DEBUG, host=host, port=int(port))


if __name__ == '__main__':
    arguments = docopt(__doc__)

    if arguments.get('server', None):
        run_server(host=arguments.get('<host>:<port>', None))

    elif arguments.get('test', None):
        os.system('python -m unittest discover test')
