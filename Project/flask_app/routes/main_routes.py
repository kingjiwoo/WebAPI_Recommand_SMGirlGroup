from flask import Blueprint

bp = Blueprint('main', __name__,url_prefix='/main')

@bp.route('/')
def index():
    return 'welcome to '