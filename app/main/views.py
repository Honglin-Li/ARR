from flask import render_template, current_app, request, session, redirect, url_for
from . import main
from app.models.Reviewer import Reviewer
from app.models.Review import Review
from app.main.forms import ReviewSearchForm, YearMonthFilterForm
from sqlalchemy import and_
from .plot_data import get_review_cycle_data


@main.route('/', methods=['GET', 'POST'])
def reviewer_list():
    form = ReviewSearchForm(request.form)

    # POST Form
    if request.method == 'POST' and form.validate():
        # set to session
        session['search_text'] = form.search_text.data
        return redirect(url_for('.reviewer_list'))

    # only search results
    search_text = session.pop('search_text', None)
    if search_text:
        reviewers = Reviewer.query.filter(Reviewer.name.ilike(f'%{search_text}%')).all()
        return render_template('reviewers.html', reviewers=reviewers, form=form)

    # all reviewers pagination
    page = request.args.get('page', 1, type=int)
    pagination = Reviewer.query.order_by(Reviewer.name).paginate(
        page, per_page=current_app.config['REVIEWERS_PER_PAGE'],
        error_out=False)
    reviewers = pagination.items

    return render_template('reviewers.html', reviewers=reviewers, pagination=pagination, form=form)


@main.route('/reviewer/<reviewer_id>', methods=['GET', 'POST'])
def reviewer(reviewer_id):
    reviewer = Reviewer.query.get_or_404(reviewer_id)
    x, y = get_review_cycle_data(reviewer)

    form = ReviewSearchForm(request.form)
    filter_form = YearMonthFilterForm(request.form)

    # POST Form
    if request.method == 'POST':
        if form.validate():
            session['search_text'] = form.search_text.data
            return redirect(url_for('.reviewer_list'))
        if filter_form.validate():
            reviews = reviewer.reviews.filter(and_(Review.year == int(filter_form.year.data),
                                                   Review.month == int(filter_form.month.data))).all()
            return render_template('review.html', reviewer=reviewer, reviews=reviews, form=form, filter_form=filter_form, x=x, y=y)

    reviews = reviewer.reviews.order_by(Review.timestamp.desc()).all()

    return render_template('review.html', reviewer=reviewer, reviews=reviews, form=form, filter_form=filter_form, x=x, y=y)
