import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # wtform
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default secret key'

    REVIEWERS_PER_PAGE = 21
    FLASK_ENV = 'development'  # DELETE WHEN DEPLOY

    # SQLITE
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'arr.sqlite')

    # OpenReview
    OR_USERNAME = os.environ.get('OR_USERNAME') or 'account@yahoo.com'
    OR_PASSWORD = os.environ.get('OR_PASSWORD') or 'password_here'

    @staticmethod
    def init_app(app):
        pass
