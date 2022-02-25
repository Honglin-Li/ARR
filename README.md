[toc]

# Introduction

[You can see the demo video here](https://youtu.be/ASGLjmLZUbY)

The website implements access to data, basic functions, statistical information. details as follows 

- **fetch reviews, reviewers, review assignments** for all papers across all rolling review cycles (May 2021 to Feb 2022)
- **home page** - reviewer list: paginate all reviewers, click to visit reviewer page
- **reviewer search bar**： is in the navigation bar, so we can search reviewer on every page.
- **reviewer page**: shows 4 parts for a reviewer. reviewer name, statistics(number of reviews and assigned reviews, average word and character length of reviews), unfulfilled review assignments, and reviews.
- **stats page**: shows overall statistics and plot. The style of the page refers to [ARR Statistics](http://stats.aclrollingreview.org/)
- **stats by cycle page**: shows cycle statistics and overall assessment distribution plot.

# How to run the dashboard

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


# Architecture

- website: python flask.
- database: sqlite + SQLAlchemy
- plot: Plotly + Echarts + Pandas
- UI: Bootstrap + CSS

The code is structured as followering:

![structure.png](https://upload-images.jianshu.io/upload_images/4613569-30009d8d2c37dc06.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

# Web Pages

1/4. Home Page(for reviewer list):

![home.png](https://upload-images.jianshu.io/upload_images/4613569-8a80f83d30708a87.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

2/4. Stats Page:
![stats.png](https://upload-images.jianshu.io/upload_images/4613569-0b927f2c8978c8a4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

3/4. Cycle Stats Page:
![cycle.png](https://upload-images.jianshu.io/upload_images/4613569-b13dc08c266a3a15.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

4/4. Reviewer Page(profile and reviews):

![reviewer.png](https://upload-images.jianshu.io/upload_images/4613569-04cc9ea122534921.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)





