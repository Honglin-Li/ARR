from app import create_app, db
from app.models.Review import Review
from app.models.Reviewer import Reviewer
from app.models.Assignment import Assignment

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Review=Review, Reviewer=Reviewer, Assignment=Assignment)


if __name__ == '__main__':
    app.run()
