from flask import Blueprint

bp = Blueprint('hello', __name__)

@bp.route("/api/hello")
def hello():
    return {"message": "Hello from the restructured backend!"}
