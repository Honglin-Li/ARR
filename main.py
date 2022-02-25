from app import create_app, db
from app.models.Review import Review
from app.models.Reviewer import Reviewer
from app.models.Assignment import Assignment
from app.utils.plot_data import PlotData
from app.fetch_command import fetch

app = create_app()
app.cli.add_command(fetch)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Review=Review, Reviewer=Reviewer, Assignment=Assignment, PlotData=PlotData)


if __name__ == '__main__':
    app.run()
