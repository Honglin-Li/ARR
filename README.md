## Introduction

[You can see the demo video here](https://youtu.be/fgjLEyevJqk)

This assignment implements the following functions.

- fetch reviews, reviewers, review assignments for all papers across all rolling review cycles (May 2021 to Feb 2022)
- Implements an interface to access data.
   - home page: paginate all reviewers, click to visit reviewer page
   - reviewer search bar： is in the navigation bar, so we can search reviewer on every page.
   - reviewer page: shows 4 parts for a reviewer. reviewer name, statistics(number of reviews and assigned reviews, average word and character length of reviews), unfulfilled review assignments, and reviews.

Home Page:

![Home Reviewer Page](https://upload-images.jianshu.io/upload_images/4613569-128b324cef8bf34e.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

Reviewer Page:

![Reviewer Page](https://upload-images.jianshu.io/upload_images/4613569-dfb4fd10c2eb7a1b.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## How to run the dashboard

### running websete

- install all the required packages and activate virtual env.
- In Windows: open terminal, input command
   - `set FLASK_APP=main.py`
   - `flask run`
- open brower, visit http://127.0.0.1:5000/, then you can see the home page.

### fetch data from OpenReview

the database is also in the github, so you can just use the it. If you want to fetch data from nothing, you can follow the following steps.

- `set FLASK_APP=main.py`
- `flask shell`
- `db.create_all()` to create a sqlite database
- run `flask review fetch` command, you can get all the data. This step needs hours.


## Architecture

- website: python flask.
- database: sqlite + SQLAlchemy
- plot: Echarts + Pandas
- UI: Bootstrap + CSS

The code is structured as followering:

![code structure](https://upload-images.jianshu.io/upload_images/4613569-ef506487df77da4f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
