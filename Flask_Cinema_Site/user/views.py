from flask import render_template, Blueprint


user_blueprint = Blueprint(
    'user', __name__,
    template_folder='templates'
)


@user_blueprint.route('/', methods=['GET'])
def user():
    return render_template('user.html')
