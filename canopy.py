import pandas as pd

unames=['user_id', 'gender', 'age', 'occupation', 'zip']
users=pd.read_table('enthought/pydata-book-master/ch02/movielens/users.dat', sep='::', header=None, names=unames)
rnames=['user_id', 'movie_id', 'rating', 'timestamp']
ratings = pd.read_table('enthought/pydata-book-master/ch02/movielens/ratings.dat', sep='::', header=None, names=rnames)
mnames=['user_id', 'title', 'genres']
movies = pd.read_table('enthought/pydata-book-master/ch02/movielens/movies.dat', sep='::', header=None, names=mnames)

data=pd.merge(pd.merge(ratings, users), movies)

mean_ratings=data.pivot_table('rating', index='title', columns='gender', aggfunc='mean')
