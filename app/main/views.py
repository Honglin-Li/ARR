from flask import render_template, current_app, request, session, redirect, url_for
from . import main
from app.models.Reviewer import Reviewer
from app.models.Review import Review
from app.models.Assignment import Assignment
from app.main.forms import ReviewSearchForm, YearMonthFilterForm
from sqlalchemy import and_
from app.utils.plot_data import PlotData
import plotly.express as px


@main.route('/search', methods=['POST'])
def search_reviewer():
    form = ReviewSearchForm(request.form)

    if request.method == 'POST' and form.validate():
        # set to session
        session['search_text'] = form.search_text.data
        return redirect(url_for('.reviewer_list'))


@main.route('/', methods=['GET', 'POST'])
def reviewer_list():
    form = ReviewSearchForm(request.form)

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
    plot_data = PlotData.get_review_cycle_data(reviewer)

    form = ReviewSearchForm(request.form)
    filter_form = YearMonthFilterForm(request.form)

    # POST Form
    if request.method == 'POST' and filter_form.validate():
        reviews = reviewer.reviews.filter(and_(Review.year == int(filter_form.year.data),
                                               Review.month == int(filter_form.month.data))).all()
        return render_template('review.html', reviewer=reviewer, reviews=reviews, form=form, filter_form=filter_form, plot=plot_data)

    reviews = reviewer.reviews.order_by(Review.timestamp.desc()).all()

    return render_template('review.html', reviewer=reviewer, reviews=reviews, form=form, filter_form=filter_form, plot=plot_data)


@main.route('/stats')
def stats():
    form = ReviewSearchForm(request.form)

    stat_data = {
        'reviewer_count': Reviewer.get_total_count(),
        'reviews_per_reviewer': int(Review.get_total_count() / Reviewer.get_total_count()),
        'review_count': Review.get_total_count(),
        'assign_count': Assignment.get_total_count(),
        'avg_reviews': Review.get_avg_count_by_cycle(),
        'avg_words': int(Review.get_avg_word_count()[0]),
        'avg_chars': int(Review.get_avg_char_count()[0])
    }

    # data for list & plot
    plot_df, cycles = PlotData.get_overall_plot_data()

    return render_template('stat.html', form=form, stat_data=stat_data, cycles=cycles)


@main.route('/stats/<cycle>')
def cycle_stats(cycle):
    form = ReviewSearchForm(request.form)

    # prepare stats data
    year, month = cycle.split('-')

    stat_data = {
        'review_count': Review.get_cycle_review_count(year, month),
        'assign_count': Assignment.get_cycle_assign_count(year, month),
        'avg_words': int(Review.get_avg_word_count(year, month)[0]),
        'avg_chars': int(Review.get_avg_char_count(year, month)[0])
    }
    # get score distribution
    score_dist_df = PlotData.get_score_distribution(2022, 1)
    score_dist_fig = px.line(score_dist_df, x='score', y='number', template='simple_white')
    score_dist_fig = score_dist_fig.update_traces(mode='lines+markers').to_html(full_html=False)

    return render_template('cycle_stat.html', form=form, stat_data=stat_data, score_dist_fig=score_dist_fig)