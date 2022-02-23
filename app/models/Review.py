from app import db


class Review(db.Model):
    __tablename__ = 'reviews'

    def __repr__(self):
        return '<Review %r>' % self.invitation

    id = db.Column(db.String, primary_key=True)
    year = db.Column(db.SmallInteger, index=True)
    month = db.Column(db.SmallInteger, index=True)
    timestamp = db.Column(db.DateTime)
    reviewer_id = db.Column(db.String, db.ForeignKey('reviewers.id'))
    paper_id = db.Column(db.String(20)) # String(11)
    invitation = db.Column(db.String(200))

    char_len = db.Column(db.Integer)
    word_len = db.Column(db.Integer)

    # content fields
    author_identity_guess = db.Column(db.String)
    best_paper = db.Column(db.String)
    comments_suggestions_and_typos = db.Column(db.Text)
    confidence = db.Column(db.String)
    datasets = db.Column(db.String)
    needs_ethics_review = db.Column(db.String)
    overall_assessment = db.Column(db.String)
    paper_summary = db.Column(db.Text)
    reproducibility = db.Column(db.String)
    software = db.Column(db.String)
    summary_of_strengths = db.Column(db.Text)
    summary_of_weaknesses = db.Column(db.Text)
