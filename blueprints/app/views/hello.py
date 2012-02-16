from flask import render_template
from lib.flask_augment import ensure_args, ensure_presence

def hello():
    return render_template('hello.html')

@ensure_presence(token=1)
@ensure_args(a=(lambda x: x and (int(x) > 10), '"a" should be greater than 10'))
def test_ensure_args():
    return 'test'

def _test_ensure_args_handler(errors):
    return str(errors)

