from functools import wraps
from flask.ext.login import current_user


def admin_required(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        if not current_user.is_admin():
            flash('Nu puteti face aceasta operatie!')
            return redirect(request.referrer)
        
        return f(*args,**kwargs)

    return decorated_function
    