import os
from flask import Flask
from flask_cors import CORS

def create_app(test_config=None):
	app = Flask(__name__, instance_relative_config=True)
	CORS(app)
	app.config.from_mapping(
		SECRET_KEY='dev',
		DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
	)

	if test_config is None:
		app.config.from_pyfile('config.py', silent=True)
	else:
		app.config.from_mapping(test_config)

	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass

	@app.route('/hello')
	def hello():
		return 'Hello is running'

	from . import db
	db.init_app(app)

	from . import auth
	app.register_blueprint(auth.bp)

	from . import operations
	app.register_blueprint(operations.bp)
	app.add_url_rule('/', endpoint='index')

	return app