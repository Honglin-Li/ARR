from app.models.Review import Review
from app.models.Reviewer import Reviewer
from app.models.Assignment import Assignment
from app import db
import openreview
from flask import current_app
from datetime import datetime
from app.main import main
from app.const import MONTHS


@main.cli.command('fetch')
def fetch_arr():
    """
    this function fetch all the review assignments and
    all the reviews for all the papers of all the cycles from 2021 May.
    Then update 3 tables in the arr.sqlite dataset:
        reviews
        reviewers
        assignments

    :return:
    """
    client = openreview.Client(baseurl='https://api.openreview.net', username=current_app.config['OR_USERNAME'],
                               password=current_app.config['OR_PASSWORD'])
    print('connecting to OpenReview Client')
    # read papers by month
    reviewer_id_list = []

    # set cycles to the cycles to be updated
    cycles = ['2021 5', '2021 6', '2021 7', '2021 8', '2021 9',
              '2021 10', '2021 11', '2021 12', '2022 1', '2022 2']

    for cycle in cycles:
        print(f'processing the reviews in cycle {cycle}...')

        year, month = cycle.split()
        month_text = MONTHS[month]

        # iterate every paper to find reviews
        paper_iterator = openreview.tools.iterget_notes(client,
                                                        signature=f'aclweb.org/ACL/ARR/{year}/{month_text}')

        for paper in paper_iterator:
            print(f'processing paper {paper.id}...')
            # read all the reviews for the paper
            reviews = client.get_notes(forum=paper.id)

            for review in reviews:
                if 'Official_Review' in review.invitation:  # pass paper and suppliment
                    review_id = review.id
                    content = review.content
                    paper_id = review.forum
                    cdate = datetime.fromtimestamp(review.cdate * 0.001)
                    char_len = len(str(content))
                    word_len = len(str(content).split())
                    signature = review.signatures[0]
                    invitation = review.invitation

                    # get and save reviewer
                    reviewer = client.get_group(signature)
                    reviewer_id = reviewer.members[0]

                    # create Review
                    review_record = Review(
                        id=review_id,
                        year=int(year),
                        month=int(month),
                        timestamp=cdate,
                        paper_id=paper_id,
                        reviewer_id=reviewer_id,
                        char_len=char_len,
                        word_len=word_len,
                        invitation=invitation,
                        author_identity_guess=content['author_identity_guess'],
                        best_paper=content['best_paper'],
                        comments_suggestions_and_typos=content['comments,_suggestions_and_typos'],
                        confidence=content['confidence'],
                        datasets=content['datasets'],
                        needs_ethics_review=content.get('needs_ethics_review'),
                        overall_assessment=content['overall_assessment'],
                        paper_summary=content['paper_summary'],
                        reproducibility=content.get('reproducibility'),
                        software=content['software'],
                        summary_of_strengths=content['summary_of_strengths'],
                        summary_of_weaknesses=content['summary_of_weaknesses']
                    )
                    # add to review table
                    db.session.add(review_record)

                    if reviewer_id not in reviewer_id_list:
                        # update reviewer table (id, name)
                        reviewer_id_list.append(reviewer_id)

                        reviewer_names = client.get_profile(reviewer_id).content['names'][0]
                        reviewer_name = ' '.join(
                            [reviewer_names['first'], reviewer_names['middle'], reviewer_names['last']]) if reviewer_names[
                            'middle'] else ' '.join([reviewer_names['first'], reviewer_names['last']])

                        # add to database
                        reviewer_record = Reviewer(
                            id=reviewer_id,
                            name=reviewer_name
                        )
                        db.session.add(reviewer_record)

        # iterate every cycle to find assignments
        print('processing Review Assignments...')
        assginment_iterator = openreview.tools.iterget_edges(client,
                                                             invitation=f'aclweb.org/ACL/ARR/{year}/{month_text}/Reviewers/-/Assignment')

        for assignment in assginment_iterator:
            # add to assignments table
            assignment_record = Assignment(
                year=int(year),
                month=int(month),
                timestamp=datetime.fromtimestamp(assignment.cdate * 0.001),
                paper_id=assignment.head,
                reviewer_id=assignment.tail
            )
            db.session.add(assignment_record)

        # update to database every month
        db.session.commit()
