import pandas as pd
from datetime import datetime
from app.models.Review import Review
from app.models.Assignment import Assignment
from sqlalchemy import and_
from app import db


class PlotData:
    # Tool Class, for getting all kinds of data, mainly serve for plot
    @staticmethod
    def get_cycles(cycle_number, reverse=True):
        """
        helper func for x-axis. generate last cycle_number months from current month

        :param cycle_number:
        :return:cycle list
        """
        y = datetime.today().year
        m = datetime.today().month
        cycles = [f'{y}-{m}']

        for i in range(cycle_number - 1):
            m = m - 1
            if m == 0:
                m = 12
                y = y - 1
            v = f'{y}-{m}'

            if v == '2021-4':  # min 2021-4
                break

            cycles.append(v)

        if reverse:
            return cycles[::-1]  # ordered by date ase

        return cycles

    @staticmethod
    def get_y(x, data):
        # helper func for y-axis
        y = []
        for i in x:
            v = data.get(i, 0)
            y.append(v)
        return y

    @staticmethod
    def get_review_cycle_data(reviewer, cycle_number=10):
        """
        this func prepare data for plot

        :param reviewer:
        :param cycle_number: the func will return the last cycle_number cycles from current cycle.
        :return: {x, y} stand for x and y-axis
        """
        # create DataFrame
        reviews_l = [{'year':review.year, 'month':review.month} for review in reviewer.reviews]

        review_df = pd.DataFrame(reviews_l)

        # prepare x-axis
        x = PlotData.get_cycles(cycle_number)

        # prepare y-axis
        review_df['x'] = review_df.year.map(str) + '-' + review_df.month.map(str)
        review_count = review_df.x.value_counts()

        y = [ str(item) for item in PlotData.get_y(x, review_count)]

        return { 'x': x, 'y': y}

    @staticmethod
    def get_score_distribution(year, month):
        x = ['0', '0.5', '1', '1.5', '2', '2.5', '3', '3.5', '4', '4.5', '5']

        # get overall assessment
        reviews = Review.query.filter(and_(Review.year == year, Review.month == month)).all()
        score_l = [review.overall_assessment for review in reviews]

        score_df = pd.DataFrame({'score': score_l})
        score_df['score'] = score_df.score.str.split().apply(lambda x: x[0])
        score_count = score_df.score.value_counts()

        y = PlotData.get_y(x, score_count)

        return pd.DataFrame({'score': x, 'number': y})

    @staticmethod
    def get_overall_plot_data(cycle_number=10):
        # return reviews and assignments over cycle { cycle, submissions, assignments }
        x = PlotData.get_cycles(cycle_number)  # plot: reverse. other: original

        # prepare reivews
        review_df = pd.DataFrame([{'year': review.year, 'month': review.month}
                                  for review in db.session.query(Review.year, Review.month).all()])

        review_df['x'] = review_df.year.map(str) + '-' + review_df.month.map(str)
        review_count = review_df.x.value_counts()

        # prepare assignments
        assign_df = pd.DataFrame([{'year': assign.year, 'month': assign.month}
                                  for assign in db.session.query(Assignment.year, Assignment.month).all()])

        assign_df['x'] = assign_df.year.map(str) + '-' + assign_df.month.map(str)
        assign_count = assign_df.x.value_counts()

        review_y = PlotData.get_y(x, review_count)
        assign_y = PlotData.get_y(x, assign_count)

        # card list data
        plot_df = pd.DataFrame({'cycle': x, 'submissions': review_y, 'assignments': assign_y})
        list_df = plot_df[plot_df['submissions'] != 0].iloc[::-1]  # remove the cycles without any reviews

        # plot data
        df_r = pd.DataFrame({'cycle': x, 'number': review_y, 'series': 'submissions'})
        df_a = pd.DataFrame({'cycle': x, 'number': assign_y, 'series': 'assignments'})
        plot_df = pd.concat([df_r, df_a])

        return plot_df, list_df.to_dict('records')





