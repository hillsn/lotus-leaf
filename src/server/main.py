"""A program that launches the UW Solar web server.

This launcher should only be used for development purposes. It is not suitable
for production deployments. A WSGI container such as Green Unicorn or uWSGI, or
a PaaS such as Amazon Elastic Beanstalk or Google App Engine should be used to
deploy the application for production purposes.
"""

import argparse
import logging
import os.path
import api_server
import bottle
import db
import www_server


def parse_arguments():
  """Parses command-line options.

  Returns:
    An object containing parsed program arguments.
  """
  # General program arguments
  parser = argparse.ArgumentParser()
  parser.add_argument(
      '--debug',
      action='store_true',
      help='Whether to run the server in debug mode.')
  parser.add_argument(
      '--log_level', default='WARNING', help='The logging threshold.')
  parser.add_argument(
      '--www_path',
      default=os.path.dirname(__file__) + '/../../dist/www',
      help='The directory where web resources are stored.')

  # HTTP server arguments
  http_group = parser.add_argument_group('http', 'HTTP server arguments.')
  http_group.add_argument(
      '--host',
      default='0.0.0.0',
      help='The hostname to bind to when listening for requests.')
  http_group.add_argument(
      '--port',
      type=int,
      default=8080,
      help='The port on which to listen for requests.')

  # Database connectivity arguments
  db_group = parser.add_argument_group('database',
                                       'Database connectivity arguments.')
  db_group.add_argument(
      '--db_type',
      choices=['mysql+mysqlconnector', 'sqlite'],
      default='sqlite',
      help='Which database type should be used.')
  db_group.add_argument(
      '--db_user', default='uwsolar', help='The database user.')
  db_group.add_argument(
      '--db_password', default='', help='The database password.')
  db_group.add_argument(
      '--db_host', default=':memory:', help='The database host.')
  db_group.add_argument(
      '--db_name', default='uwsolar', help='The database name.')
  db_group.add_argument(
      '--db_pool_size', type=int, default=3, help='The database pool size.')

  return parser.parse_args()


def main():
  """Parses command-line arguments and initializes the server."""
  args = parse_arguments()

  # Initialize logging.
  logging.basicConfig(level=logging.getLevelName(args.log_level))

  # Initialize the database connection.
  db_options = db.DatabaseOptions(args.db_type, args.db_user, args.db_password,
                                  args.db_host, args.db_name,
                                  args.db_pool_size)
  db_accessor = db.Database(db_options)

  # Initialize and start the web application.
  app = www_server.WwwServer(args.www_path).app()
  app.mount('/_/', api_server.ApiServer(db_accessor).app())
  bottle.run(app=app, host=args.host, port=args.port, debug=args.debug)


if __name__ == '__main__':
  main()
