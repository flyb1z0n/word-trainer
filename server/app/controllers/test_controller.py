from flask import Blueprint

bp = Blueprint('test', __name__)

@bp.route('/test')
def test():
    return 'Test12221!'
