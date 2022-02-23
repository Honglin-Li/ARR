from app import db
from sqlalchemy import func
from .Review import Review


class Reviewer(db.Model):
    __tablename__ = 'reviewers'

    def __repr__(self):
        return '<Reviewer %r>' % self.name

    id = db.Column(db.String(200), primary_key=True)
    name = db.Column(db.String(200), index=True)

    # relationship 
    reviews =db.relationship('Review', backref='reviewer', lazy='dynamic')
    assignments = db.relationship('Assignment', backref='reviewer', lazy='dynamic')

    @property
    def avg_words_count(self):
        return db.session.query(func.avg(Review.word_len)).filter(Review.reviewer_id == self.id).one()

    @property
    def avg_chars_count(self):
        return db.session.query(func.avg(Review.char_len)).filter(Review.reviewer_id == self.id).one()

    @property
    def unfulfilled_assignments(self):
        review_id_set = {review.id for review in self.reviews}
        assignment_id_set = {ass.paper_id for ass in self.assignments}
        unfulfilled = review_id_set.difference(assignment_id_set)
        return unfulfilled




