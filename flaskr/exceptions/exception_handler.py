import logging
import traceback

from flask import jsonify

from flaskr.exceptions.apierror import APIError
from flaskr.main import app


# @app.errorhandler(APIError)
# def handle_exception(err):
#     """Return custom JSON when APIError or its children are raised"""
#     response = {"error": err.description, "status code": err.code, "message": ""}
#     if len(err.args) > 0:
#         response["message"] = err.args[0]
#     # Add some logging so that we can monitor different types of errors
#     logging.error(f'{err.description}: {response["message"]}')
#     return jsonify(response)


# @app.errorhandler(500)
# def handle_exception(err):
#     """Return JSON instead of HTML for any other server error"""
#     app.logger.error(f"Unknown Exception: {str(err)}")
#     app.logger.debug(''.join(traceback.format_exception(etype=type(err), value=err, tb=err.__traceback__)))
#     response = {"error": "Sorry, that error is on us, please contact support if this wasn't an accident"}
#     return jsonify(response), 500
