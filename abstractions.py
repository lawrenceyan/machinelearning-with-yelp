"""Data Abstractions"""

from utils import mean

# Reviews

def make_review(restaurant_name, rating):
    """Return a review data abstraction."""
    return [restaurant_name, rating]

def review_restaurant_name(review):
    """Return the restaurant name of the review, which is a string."""
    return review[0]

def review_rating(review):
    """Return the number of stars given by the review, which is a
    floating point number between 1 and 5."""
    return review[1]


# Users

def make_user(name, reviews):
    """Return a user data abstraction.

    Arguments: name -- a name
    reviews -- a list of review data abstractions
    """
    return [name, {review_restaurant_name(r): r for r in reviews}]

def user_name(user):
    """Return the name of the user, which is a string."""
    return user[0]

def user_reviews(user):
    """Return a dictionary of restaurant names -> reviews by the user."""
    return user[1]

def user_reviewed_restaurants(user, restaurants):
    """Return the subset of restaurants reviewed by user.

    Arguments: user -- a user
    restaurants -- a list of restaurant data abstractions
    """
    return [r for r in restaurants if restaurant_name(r) in list(user_reviews(user))]

def user_rating(user, restaurant_name):
    """Return the rating given for restaurant_name by user."""
    return review_rating(user_reviews(user)[restaurant_name])


# Restaurants

def make_restaurant(name, location, categories, price, reviews):
    """Return a restaurant data abstraction."""
    return {
        'name': name,
        'location': location,
        'categories': categories,
        'price': price,
        'reviews': reviews
    }

def restaurant_name(restaurant):
    """Return the name of the restaurant, which is a string."""
    return restaurant['name']

def restaurant_location(restaurant):
    """Return the location of the restaurant, which is a list containing
    latitude and longitude."""
    return restaurant['location']

def restaurant_categories(restaurant):
    """Return the categories of the restaurant, which is a list of strings."""
    return restaurant['categories']

def restaurant_price(restaurant):
    """Return the price of the restaurant, which is a number."""
    return restaurant['price']

def restaurant_ratings(restaurant):
    """Return a list of ratings, which are numbers from 1 to 5, of the
    restaurant based on the reviews of the restaurant."""
    return [review_rating(i) for i in restaurant['reviews']]

def restaurant_num_ratings(restaurant):
    """Return the number of ratings for the restaurant."""
    return len(restaurant['reviews'])

def restaurant_mean_rating(restaurant):
    """Return the average rating for the restaurant."""
    return sum([review_rating(i) for i in restaurant['reviews']]) / restaurant_num_ratings(restaurant)
