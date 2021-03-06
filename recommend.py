"""A Yelp-powered Restaurant Recommendation Program"""

from abstractions import *
from data import ALL_RESTAURANTS, CATEGORIES, USER_FILES, load_user_file
from ucb import main, trace, interact
from utils import distance, mean, zip, enumerate, sample
from visualize import draw_map

#########################
# Unsupervised Learning #
#########################


def find_closest(location, centroids):
    """Return the centroid in centroids that is closest to location.
    If multiple centroids are equally close, return the first one.

    >>> find_closest([3.0, 4.0], [[0.0, 0.0], [2.0, 3.0], [4.0, 3.0], [5.0, 5.0]])
    [2.0, 3.0]
    """
    return min([i for i in centroids], key = lambda x: distance(location,x))

def group_by_first(pairs):
    """ Return a list of pairs that relates each unique key in the [key, value]
    pairs to a list of all values that appear paired with that key.

    Arguments:
    pairs -- a sequence of pairs

    >>> example = [ [1, 2], [3, 2], [2, 4], [1, 3], [3, 1], [1, 2] ]
    >>> group_by_first(example)
    [[2, 3, 2], [2, 1], [4]]
    """
    keys = []

    # Adds key to key list if key is not yet already in list
    [keys.append(key) for key, _ in pairs if key not in keys]

    # Groups values corresponding to each key into individual lists
    return [ [y for x, y in pairs if x == key] for key in keys ]

def group_by_centroid(restaurants, centroids):
    """Return a list of clusters, where each cluster contains all restaurants
    nearest to a corresponding centroid in centroids. Each item in
    restaurants should appear once in the result, along with the other
    restaurants closest to the same centroid.
    """

    # Uses group_by_first method where [key,value] -> [cluster,restaurant]
    return group_by_first([[find_closest(restaurant_location(i),centroids),i] for i in restaurants])

def find_centroid(cluster):
    """Return the centroid of the locations of the restaurants in cluster."""

    # Takes locations of all restaurants in cluster and finds mean
    fn = lambda x: mean([restaurant_location(i)[x] for i in cluster])
    return [fn(0),fn(1)] # 0 for x-coordinate / 1 for y-coordinate

def k_means(restaurants, k, max_updates=100):
    """Simple unsupervised machine learning algorithm that uses k-means to
    best estimate where centroid locations should be placed.
    """
    assert len(restaurants) >= k, 'Not enough restaurants to cluster'
    old_centroids, n = [], 0

    # Select initial centroids randomly by choosing k different restaurants
    centroids = [restaurant_location(r) for r in sample(restaurants, k)]

    # Estimates where centroids are
    while old_centroids != centroids and n < max_updates:
        old_centroids = centroids
        clusts = group_by_centroid(restaurants,old_centroids)
        centroids = [find_centroid(i) for i in clusts]
        n += 1

    return centroids


#######################
# Supervised Learning #
#######################


def find_predictor(user, restaurants, feature_fn):
    """Return a rating predictor (a function from restaurants to ratings),
    for a user by performing least-squares linear regression using feature_fn
    on the items in restaurants. Also, return the R^2 value of this model.

    Arguments: user -- A user
    restaurants -- A sequence of restaurants
    feature_fn -- A function that takes a restaurant and returns a number
    """
    reviews_by_user = {review_restaurant_name(review): review_rating(review)
                       for review in user_reviews(user).values()}

    xs = [feature_fn(r) for r in restaurants]
    ys = [reviews_by_user[restaurant_name(r)] for r in restaurants]

    # Used for sum of squares calculation
    fn = lambda coor,exp=1: [(i-mean(coor))**exp for i in coor]
    sxx = sum(fn(xs,2))
    syy = sum(fn(ys,2))
    sxy = sum([a*b for a,b in zip(fn(xs),fn(ys))])

    b = sxy/sxx
    a, r_squared = mean(ys)-b*mean(xs), sxy**2 / (sxx*syy)

    def predictor(restaurant):
        """Takes in restaurant input and outputs a predicted rating"""
        return b * feature_fn(restaurant) + a

    return predictor, r_squared


def best_predictor(user, restaurants, feature_fns):
    """Find the feature within feature_fns that gives the highest R^2 value
    for predicting ratings by the user; return a predictor using that feature.

    Arguments:
    user -- A user
    restaurants -- A list of restaurants
    feature_fns -- A sequence of functions that each takes a restaurant
    """
    reviewed = user_reviewed_restaurants(user, restaurants)
    # Iterate through feature_fns picking best predictor utilizing lambda function as key
    return max([find_predictor(user,reviewed,i) for i in feature_fns], key = lambda x:x[1])[0]

def rate_all(user, restaurants, feature_fns):
    """Return a dictionary with the predicted ratings of restaurants by user using the best
    predictor based on a function from feature_fns.

    Arguments:
    user -- A user
    restaurants -- A list of restaurants
    feature_fns -- A sequence of feature functions
    """
    predictor = best_predictor(user, ALL_RESTAURANTS, feature_fns)
    user_reviewed = user_reviewed_restaurants(user, restaurants)

    dic = {}
    for t in restaurants:
        if t in user_reviewed_restaurants(user, restaurants):
            dic[restaurant_name(t)] = user_rating(user, restaurant_name(t))
        else:
            dic[restaurant_name(t)] = predictor(t)
    return dic

def search(query, restaurants):
    """Return each restaurant in restaurants that has query as a category.

    Arguments:
    query -- A string
    restaurants -- A sequence of restaurants
    """
    return [i for i in restaurants if query in restaurant_categories(i)]


def feature_set():
    """Return a sequence of feature functions."""
    return [restaurant_mean_rating,
            restaurant_price,
            restaurant_num_ratings,
            lambda r: restaurant_location(r)[0],
            lambda r: restaurant_location(r)[1]]


@main
def main(*args):
    import argparse
    parser = argparse.ArgumentParser(
        description='Run Recommendations',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('-u', '--user', type=str, choices=USER_FILES,
                        default='test_user',
                        metavar='USER',
                        help='user file, e.g.\n' +
                        '{{{}}}'.format(','.join(sample(USER_FILES, 3))))
    parser.add_argument('-k', '--k', type=int, help='for k-means')
    parser.add_argument('-q', '--query', choices=CATEGORIES,
                        metavar='QUERY',
                        help='search for restaurants by category e.g.\n'
                        '{{{}}}'.format(','.join(sample(CATEGORIES, 3))))
    parser.add_argument('-p', '--predict', action='store_true',
                        help='predict ratings for all restaurants')
    parser.add_argument('-r', '--restaurants', action='store_true',
                        help='outputs a list of restaurant names')
    args = parser.parse_args()

    # Output a list of restaurant names
    if args.restaurants:
        print('Restaurant names:')
        for restaurant in sorted(ALL_RESTAURANTS, key=restaurant_name):
            print(repr(restaurant_name(restaurant)))
        exit(0)

    # Select restaurants using a category query
    if args.query:
        restaurants = search(args.query, ALL_RESTAURANTS)
    else:
        restaurants = ALL_RESTAURANTS

    # Load a user
    assert args.user, 'A --user is required to draw a map'
    user = load_user_file('{}.dat'.format(args.user))

    # Collect ratings
    if args.predict:
        ratings = rate_all(user, restaurants, feature_set())
    else:
        restaurants = user_reviewed_restaurants(user, restaurants)
        names = [restaurant_name(r) for r in restaurants]
        ratings = {name: user_rating(user, name) for name in names}

    # Draw the visualization
    if args.k:
        centroids = k_means(restaurants, min(args.k, len(restaurants)))
    else:
        centroids = [restaurant_location(r) for r in restaurants]
    draw_map(centroids, restaurants, ratings)
