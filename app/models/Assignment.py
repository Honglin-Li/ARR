from app import db


class Assignment(db.Model):
    __tablename__ = 'assignments'

    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.SmallInteger, index=True)
    month = db.Column(db.SmallInteger, index=True)
    timestamp = db.Column(db.DateTime)
    paper_id = db.Column(db.String(20))
    reviewer_id = db.Column(db.String(200), db.ForeignKey('reviewers.id'))