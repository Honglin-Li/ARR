from app import db
from sqlalchemy import and_


class Assignment(db.Model):
    __tablename__ = 'assignments'

    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.SmallInteger, index=True)
    month = db.Column(db.SmallInteger, index=True)
    timestamp = db.Column(db.DateTime)
    paper_id = db.Column(db.String(20))
    reviewer_id = db.Column(db.String(200), db.ForeignKey('reviewers.id'))

    @staticmethod
    def get_avg_count_by_cycle():
        cycle_number = db.session.query(Assignment.year, Assignment.month).distinct().count()
        return int(Assignment.get_total_count() / cycle_number)

    @staticmethod
    def get_total_count():
        return Assignment.query.count()

    @staticmethod
    def get_cycle_assign_count(year, month):
        return Assignment.query.filter(and_(Assignment.year == year, Assignment.month == month)).count()