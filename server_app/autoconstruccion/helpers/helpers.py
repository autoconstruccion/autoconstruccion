from flask import Blueprint, current_app
from flask import make_response, render_template

bp = Blueprint('helpers', __name__)
log = current_app.logger


@bp.app_errorhandler(403)
def error_internal_server_error(exception):
    log.error(exception)
    return make_response(render_template('error/err_403.html'), 403)


@bp.app_errorhandler(404)
def error_page_not_found(exception):
    return make_response(render_template('error/err_404.html'), 404)


@bp.app_errorhandler(500)
def error_internal_server_error(exception):
    log.error(exception)
    return make_response(render_template('error/err_500.html'), 500)
