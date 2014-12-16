# -*- coding: utf-8 -*-

"""
=============================================================
AUTHORS: Alexandre Laterre & Benoit Sluysmans, UCL-EPL
DATE: 28/11/2014
LINMA2472 - Questions de math discretes
=============================================================
Recommender for one user based on collaborative filtering
"""

from numpy import *
from scipy import *
from scipy.sparse import *
from numpy.linalg import norm
        
def normesUsers(UM,x):
    """ Compute the norm of each user vector """
    
    normes = zeros((x,1))
    for i in xrange(x):
        norme = norm(UM[i,:].todense())
        if norme == 0.0:
            normes[i] = -1 # no movie seen
        else:
            normes[i] = norme
        
    return normes
    
def ratingsUser(UM,U):
    """ Output: list of movies seen by U and their ratings """
    
    line = UM[U,:].todense()
    line = array(line) # matrix to array to perform search operations
        
    moviesSeen = nonzero(line) # column with index of movies seen by U
    moviesRat = line[moviesSeen] # column with ratings of movies seen by U
    
    ratingsUser = column_stack((moviesRat,moviesSeen[1]))
   
    return ratingsUser
    

def recommend(U, UM, m=5, n=100, meanU = 0, normalizing = False):
    """Give a list of recommendations for user U based on collaborative filtering:
        - Find the n users more similar to U (with the cosine similarity)
        - Compute the average (weighted by similarity to U) of their ratings for 
            items that U didn't rate
        - Sort that list to give the items U could like first
        - Take the m items U is most likely to rate high

        Parameters
        ----------
        U: we compute recommandations for user U
        UM: utility matrix, must be a "csr" matrix (see scipy sparse matrix)
        m: number of items to recommend
        n: number of more similar neighbours to visit
        meanU: mean of U ratings
        normalizig: True if used normalized UM, False otherwise
        
        Output
        ------
        recommendations: a matrix (m x 2) that contains the m items desribed 
            above, and their approximate ratings
        """
        
    x = UM.shape[0]
    y = UM.shape[1]
    
    # --- index the users and the movies ---
    users = arange(x)
    movies = arange(y)
        
    # --- Compute the norms ---
    normes = normesUsers(UM,x)  
    normeU = normes[U]
    
    # --- Compute the cosine similarity of other users ---
    cosineSim = UM.dot(UM[U,:].T)
    cosineSim = cosineSim/(normes*normeU)
    
    # --- Sort and select the n more similar users ---
    simUsers = column_stack((cosineSim,users))
    simUsers = delete(simUsers, U, 0) # delete the user U himself
    simUsers = array(simUsers) # matrix to array to perform search operations
    
    I = argsort(simUsers[:,0])
    simUsers = simUsers[I[::-1],:] # more simalar users above of the list
    simUsers = simUsers[0:n,:] # keep the n more similar users
    
    # --- Remember movies U have seen ---
    seenByU = ratingsUser(UM,U)[:,1]
    
    # --- Initialize wich will contain the weighted ratings of the movies ---
    sumRatingsNearests = column_stack((zeros((y,3)),movies))
    
    for line in simUsers:
        sim = line[0] # similarity
        user = line[1] # user
        
        # --- Compute the ratings of each user in simUsers ---
        ratings = ratingsUser(UM,user)
        
        for line2 in ratings:
            rating = line2[0]
            movie = line2[1]
            
            # --- Add these ratings to sumRatingsNearests with weight = similarity ---
            if movie not in seenByU: # don't recommand movies seen by U
                sumRatingsNearests[movie, 1] += rating*sim  # weighted rating
                sumRatingsNearests[movie, 2] += sim
            
                sumR = sumRatingsNearests[movie, 1]    
                sumW = sumRatingsNearests[movie, 2]
            
                sumRatingsNearests[movie, 0] = sumR/sumW # normalized sum of weighted ratings
            

    # --- Sort these weighted ratings ---
    I = argsort(sumRatingsNearests[:,0])
    sumRatingsNearests = sumRatingsNearests[I[::-1],:] 
    
    # --- Recommand the m movies with highest ratings ---
    recMov = sumRatingsNearests[0:m,3]
    if normalizing:
        recRat = sumRatingsNearests[0:m,0] + meanU
    else:
        recRat = sumRatingsNearests[0:m,0]
        
    recommendations = column_stack((recMov,recRat))
    
    return recommendations
    