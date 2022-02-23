import pandas as pd
from datetime import datetime


def get_review_cycle_data(reviewer, cycle_number=10):
    """
    this func prepare data for plot

    :param reviewer:
    :param cycle_number: the func will return the last cycle_number cycles from current cycle.
    :return: x, y stand for x and y-axis
    """
    #reviewer = Reviewer.query.get(reviewer_id)
    reviews = reviewer.reviews

    # create DataFrame
    reviews_l = []

    for review in reviews:
        reviews_l.append({
            'year':review.year,
            'month':review.month
        })

    review_df = pd.DataFrame(reviews_l)

    # prepare x-axis
    y = datetime.today().year
    m = datetime.today().month
    x = [f'{y}-{m}']

    for i in range(cycle_number - 1):
        m = m - 1
        if m == 0:
            m = 12
            y = y - 1
        x.append(f'{y}-{m}')

    # prepare y-axis
    review_df['x'] = review_df.year.map(str) + '-' + review_df.month.map(str)
    review_count = review_df.x.value_counts()

    y = []
    for i in x:
        v = review_count.get(i, 0)
        y.append(v)

    return x, y


