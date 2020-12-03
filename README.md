![=Header Image=](images/header_image.jpg)

# Predicting Yelp Review Quality

## Table of Contents
* [Introduction](#Introduction)
    * [Motivation](#Motivation)
    * [The Data](#The-Data)
    * [Business Use Case](#Business-Use-Case)
    * [Central Questions](#Central-Questions)
* [Data Storage](#Data-Storage)
* [Data Pipeline](#Data-Pipeline)
* [Data Analysis](#Data-Analysis)
    * [Logistic Regression](#Logistic-Regression)
    * [Random Forest](#Random-Forest)
* [Conclusions](#Conclusions)
* [Next Steps](#Next-Steps)
* [Photo and Data Credits](#Photo-and-Data-Credits)

<br/><br/>

# Introduction

## Motivation

I have a personal and professional interest in the leisure/tourism industry with a focus on two things:
1. The perceived quality and popularity of places and points of interest. 
    * Examples: Restaurants, Bars/Nightlife, Breweries, Music Venues, Parks and Outdoor Spaces. Very broad focus. Pretty much anything that involves the combination of leisure and being in public.
2. Creating a way to connect people to these places/POIs in a way that is more beneficial to both the places/POIs and the people than current common methods. 

Yelp and other similar companies like Foursquare, Google Places, TripAdvisor, etc. are the current leaders in this space, though I believe there are substantial untapped opportunities in this space.
Working with and better understanding the data available to these companies will help us to more fully take advantage of these opportunities.

## Business Use Case

=Fix This Section=

* Yelp can optimally surface reviews in real time instead of waiting on users to vote on the review quality. 
* Allows Yelp reviews to keep up with changes in the business quality instead of lagging behind it. 
* Like reddit's hot feed instead of the top feed.
* The ability for Yelp to showcase its most useful reviews as they happen allows Yelp to provide the most up to date information to its users which increases user satisfaction, retention, and value to the company. 

## Central Questions
### 1. Can the quality of a review be determined by data surrounding the review?
### 2. What types of data are most useful for predicting review quality?
### 3. What model is the best for predicting the quality of a review?

## The Data

The data for this project comes from the Yelp Open Dataset.  
[Dataset](https://www.yelp.com/dataset), [Documentation](https://www.yelp.com/dataset/documentation/main), [Yelp Github](https://github.com/Yelp/dataset-examples), [Kaggle](https://www.kaggle.com/yelp-dataset/yelp-dataset)

![Yelp Open Dataset Home Page](images/yelp_dataset_homepage_top.png)

### About Yelp 
> ### *<div align="center">"Yelp connects people with great local businesses. With unmatched local business information, photos and review content, Yelp provides a one-stop local platform for consumers to discover, connect and transact with local businesses of all sizes by making it easy to request a quote, join a waitlist, and make a reservation, appointment or purchase. Yelp was founded in San Francisco in 2004."</div>*

[Yelp News](https://www.yelp-press.com/news/default.aspx), [Fast Facts and Stats](https://www.yelp-press.com/company/fast-facts/default.aspx) <--- Say that 10 times fast.

### About the Data 

![Yelp About the Dataset](images/yelp_dataset_homepage_bottom.png)

This dataset consists of 5 seperate json files totaling ~10GB of data uncompressed. Overall there is a mix of datatypes. The major ones are long text strings, datetimes, booleans, and numerical counts/ratings. Plenty of nan/null values but this is partially offset by the size of the dataset. The five files consist of:
* **Users**- ~2 million rows and 22 features
    * User metadata, list of friends, and stats about interactions with other users.
* **Reviews**- ~8 million reviews with 9 features.
    * 8 review metadata features and the review content.
* **Checkins**- ~175000 businesses represented. Looks like a couple million total date-times. 
    * Dates and times for check-ins for each business. 
* **Businesses**- ~210000 rows with around 30 total features.
    * Business name, address, hours, rating, review count, etc. 
    * Also includes dictionaries of more in depth attributes like cost, accepts credit cards, good for kids, etc.
* **Tips**- ~1.3 million rows with 5 features
    * Kind of like a really short review without as much useful metadata.

<br/><br/>

# Data Storage

My original data came in 5 json files. The first step was to simplify, combine, and store these files in a way that would be easily queryable for future data analysis, cleaning, and feature engineering. Using the tools below I converted the original json files into a Postgres database table that could be easily accessed using Pandas.

![Data Storage Process](images/data_storage_process.png)

## Original Working Dataset

|    | review_id              | user_id                | business_id            |   review_stars | review_date         | review_text                  |   review_useful |   review_funny |   review_cool | restaurant_name              | restaurant_address           | restaurant_city   | restaurant_state   | restaurant_postal_code   |   restaurant_latitude |   restaurant_longitude |   restaurant_overall_stars |   restaurant_review_count |   restaurant_is_open | restaurant_categories        |   restaurant_price_range | user_name   |   user_review_count | user_yelping_since   |   user_useful |   user_funny |   user_cool | user_elite               | user_friends                 |   user_fans |   user_average_stars_given |   user_compliment_hot |   user_compliment_more |   user_compliment_profile |   user_compliment_cute |   user_compliment_list |   user_compliment_note |   user_compliment_plain |   user_compliment_cool |   user_compliment_funny |   user_compliment_writer |   user_compliment_photos | restaurant_checkins          |
|---:|:-----------------------|:-----------------------|:-----------------------|---------------:|:--------------------|:-----------------------------|----------------:|---------------:|--------------:|:-----------------------------|:-----------------------------|:------------------|:-------------------|:-------------------------|----------------------:|-----------------------:|---------------------------:|--------------------------:|---------------------:|:-----------------------------|-------------------------:|:------------|--------------------:|:---------------------|--------------:|-------------:|------------:|:-------------------------|:-----------------------------|------------:|---------------------------:|----------------------:|-----------------------:|--------------------------:|-----------------------:|-----------------------:|-----------------------:|------------------------:|-----------------------:|------------------------:|-------------------------:|-------------------------:|:-----------------------------|
|  0 | 48GS5BhOe5Q0exkwH4qIig | r5IC7MVMH9wL-IQKx2CmXg | uh7DUWtPoZkuEE05fghJ_w |              5 | 2016-06-24 14:52:55 | Living in NYC and having ... |               1 |              0 |             0 | Beauty & Essex               | 3708 S Las Vegas Blvd, Le... | Las Vegas         | NV                 | 89109                    |               36.1099 |              -115.175  |                        4   |                      1078 |                    1 | Lounges, Restaurants, Nig... |                        3 | Kelly       |                 122 | 2009-08-19 15:54:29  |           191 |           79 |          41 |                          | 7Mhup6mfEgNAyHyfSBpQ6w, R... |           5 |                       3.81 |                     1 |                      0 |                         0 |                      0 |                      0 |                      0 |                       2 |                      0 |                       0 |                        0 |                        0 | 2016-05-11 02:52:26, 2016... |
|  1 | WxqwVmZhq5-kvvRsUun1-w | 8Dvr-U6jCZTVGD52LwC2qA | orS5gYr8phw6YfV-oEPnTw |              4 | 2018-03-22 03:32:12 | Very, very good rice roll... |               3 |              0 |             2 | Pho Xin Chào                 | 7057 Yonge Street            | Markham           | ON                 | L3T 2A6                  |               43.7996 |               -79.4201 |                        4   |                        49 |                    1 | Desserts, Food, Restauran... |                        2 | Amy         |                 388 | 2015-11-20 04:33:32  |          1149 |           83 |         265 | 2017,2018                | CQ67NJigSe5-uBDX3b_CUw, e... |          41 |                       3.78 |                     7 |                      0 |                         0 |                      0 |                      0 |                      9 |                      13 |                      7 |                       7 |                       12 |                       12 | 2018-03-04 18:29:48, 2018... |
|  2 | 5XwWfBkibiJLn9wBnD2QTQ | 3_a4J7RFtAOSh2maSH1Dlg | ZjKpGYdQCQPxzkYWAsV56w |              5 | 2018-05-18 16:26:27 | The service was quite goo... |               0 |              0 |             0 | Thailicious Authentic Tha... | 19 S Stephanie St, Ste 16... | Henderson         | NV                 | 89012                    |               36.0282 |              -115.049  |                        4.5 |                       604 |                    1 | Restaurants, Thai, Vegeta... |                        2 | Marsha      |                   8 | 2016-02-29 03:03:48  |             0 |            0 |           0 |                          | 8CQRuR-tjDy6uuGU8R7zeg, W... |           0 |                       3.88 |                     0 |                      0 |                         0 |                      0 |                      0 |                      0 |                       0 |                      0 |                       0 |                        0 |                        0 | 2017-09-07 19:49:06, 2017... |
|  3 | B7a8BnvPzCy90yblleT1kQ | 45kX9LyeR_Z4jRcxDAh0cA | ZjKpGYdQCQPxzkYWAsV56w |              5 | 2018-05-05 00:26:20 | The servers were super sw... |               0 |              0 |             0 | Thailicious Authentic Tha... | 19 S Stephanie St, Ste 16... | Henderson         | NV                 | 89012                    |               36.0282 |              -115.049  |                        4.5 |                       604 |                    1 | Restaurants, Thai, Vegeta... |                        2 | Lesly       |                   4 | 2015-11-15 03:55:35  |             0 |            0 |           0 |                          | yDA1FKynHAncG5CiSc8_Zg, x... |           0 |                       3    |                     0 |                      0 |                         0 |                      0 |                      0 |                      0 |                       0 |                      0 |                       0 |                        0 |                        0 | 2017-09-07 19:49:06, 2017... |
|  4 | y0OM430M5gfDJna7I_L5kw | FS6dSo0sGtzeeO9XAoGE4Q | uh7DUWtPoZkuEE05fghJ_w |              4 | 2017-08-07 01:11:41 | Came here with a group of... |               0 |              0 |             0 | Beauty & Essex               | 3708 S Las Vegas Blvd, Le... | Las Vegas         | NV                 | 89109                    |               36.1099 |              -115.175  |                        4   |                      1078 |                    1 | Lounges, Restaurants, Nig... |                        3 | Kristi      |                 224 | 2009-08-31 03:23:42  |           227 |           59 |          90 | 2013,2014,2015,2016,2017 | a4CC6waxI5Qd-QWUnMUOHA, o... |           7 |                       3.95 |                     2 |                      2 |                         2 |                      0 |                      0 |                      3 |                       4 |                      4 |                       4 |                        5 |                        0 | 2016-05-11 02:52:26, 2016... |

<br/><br/>

# Data Pipeline

The original working data was not going to be very usable for analysis and machine learning model training so I created a pipeline that would clean and organize the data as well as add features that could be informative.

![Pipeline](images/pipeline_icon.png)

## Data Cleaning

The main data cleaning steps included:
* Dropping Nan/Null Values 
* Removing Duplicate Records
* Deleting Unecessary Features
* Converting Datatypes
* Organizing Features

## Feature Engineering

Features added included:
* Sums
    * User Upvotes
    * User Compliments
* Counts
    * User Friends Count
    * User Elite Count
    * Restaurant Checkin Count
* Time Based
    * User Years Since Last Elite
    * User Days Active at Review Time
* Composites
    * Review Stars vs. User Average
    * Review Stars vs. Restaurant Average

<br/><br/>

# Data Analysis

## Central Questions:
### Can the quality of a review be determined by data surrounding the review?
### What types of data are most useful for predicting review quality?
### What model is the best for predicting the quality of a review?

The data being used for prediction falls into three categories:
* Data surrounding the review.
* Data about the user that created the review.
* Data about the restaurant being reviewed.

## Basic Analysis

=EDA_and_Graphing=

## Logistic Regression

=model_prep_and_inputs=
=model_results= 
=feature_coefficents_and_p_values=

## Random Forest

=model_prep_and_inputs=
=model_results=
=feature_importances=

<br/><br/>

# Conclusions
### The quality of reviews can be determined by the data surrounding the review with an accuracy significantly better than chance.
### .................... are the most important features to consider when predicting the quality of a review.
### More analysis needs to be completed to improve prediction results.
### Of the two model types tested, the Random Forest model better prediction accuracy compared to Logistic Regression.

### Knowing that quality of reviews can be predicted as well as which pieces of data are the most important for these predictions helps Yelp to better surface reviews that improve user engagement and satisfaction.
### Unfortunately, at this time the magnitude of this knowledge is not large enough to encourage significant action, though this will be improved in the near future.  

<br/><br/>

# Next Steps

Improve the abilty to predict review quality by:
* Streamlining the data storage and cleaning pipeline.
* Utilizing NLP to explore the text of the reviews.
* Collecting current data via the Yelp API.
* Adjusting data for changes over time.
* Scaling up the capacity for data analysis by utilizing AWS and Apache Spark.
* Testing new machine learning models including XG Boost and Neural Networks.
* Creating a machine learning model testing framework for tuning models and cataloging results.
* Creating custom cost functions that better represent the overall goal.    

<br/><br/>

# Photo and Data Credits  
**Cover Photo**: Parsehub Blog ["How to Scrape Yelp Data: Business Information, Ratings, Reviews and more..."](https://www.parsehub.com/blog/scrape-yelp-data/) - 9/5/2019  

**Main Data Source**: [Yelp Open Dataset](https://www.yelp.com/dataset) Datasets and Images 

**Other Credits, Sources, Further Research Links**
* Image Credits
    * Machine Learning by Angela from the Noun Project
    * data storage by Alone forever from the Noun Project
    * JSON by Smashicons from flaticon