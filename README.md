# machinelearning-with-yelp

Using a Voronoi diagram superimposed onto a specified map location (Ex. Downtown Berkeley), creates a simple visualization of predicted restaurant ratings in any area based on a compiled dataset of preexisting Yelp reviews nearby.

Visualization created utilizing a combination of simple least-squares linear regression and k-means algorithm. Check out the recommend.py file for specific code implementation. 

Default sample data has been queried from restaurants near and around the UC Berkeley campus where I live. Feel free to query for your own specific location using the Fusion API.

The default user profile that will be used is based around my personal tastes and reviews. Feel free to create your own user profile and use that instead. Make sure to follow the format as set by the Users Data Abstraction within abstractions.py, and place it in the Users directory.

     Ex. File called Donald.dat

          make_user(

               'Donald Trump', # name

                    [ # reviews

                         make_review('Mar-a-lago', 5.0),
                         
                         etc…

                    ]

KEY: (Yellow is expected 5 star rating -> Blue is expected 1 star rating) (Restaurants are represented by dots with specific colors corresponding to their individual locations)

Run recommend.py to use this tool, --help for specific documentation on optional arguments that can be made to manipulate visualization.

     optional arguments:

     -h, --help                      show this help message and exit
                                     
     -u USER, --user USER            USER user file, i.e. {test_user,one_cluster,likes_everything}
                                     
     -k K, --k                       K for k-means
                                       
     -q QUERY, --query QUERY                 
                                     search for restaurants by category e.g. 
                                     {Vegetarian, Wine & Spirits, Chinese, Sports Bar}
                                      
     -p, --predict                   predict ratings for all restaurants
                                      
     -r, --restaurants               outputs a list of restaurant names

As an example, a possible command you might make.

     python recommend.py -u really_rich_person -k 2 -p -q Sandwiches 

This would result in a visualization of predicted ratings based on a user profile of someone who likes expensive restaurants filtering specifically for sandwich restaurants only.
