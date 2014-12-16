# -*- coding: utf-8 -*-
"""
=============================================================
AUTHOR: Benoit Sluysmans, UCL-EPL
DATE: 10/11/2014
LINMA2472 - Questions de math discretes
=============================================================
Recommender for one user based on collaborative filtering
"""
from math import sqrt
import sys

def cosine(r1, r2):
    """Compute the cosine distance between ratings r1 and r2 (must be
        dictionaries of the form {1: 3.0, 3: 2.0, 11:5.0})"""
    sumxx, sumxy, sumyy = 0,0,0
    for key in r1:
        x = r1[key]
        sumxx += x*x
        if key in r2:
            y = r2[key]
            sumxy += x*y
    for key in r2:
        y = r2[key]
        sumyy += y*y
    if sumxx*sumyy == 0.0:
        distance = 0.0
    else:
        distance = sumxy/sqrt(sumxx*sumyy)
    return distance

def jaccard(r1, r2):
    """Compute the jaccard similarity between ratings r1 and r2 (must be
        dictionaries of the form {1: 3.0, 3: 2.0, 11:5.0})"""
    intersection, union = 0, 0
    for key in r1:
        if key in r2:
            intersection += 1
        union += 1
    for key in r2:
        if not key in r1:
            union += 1
    distance = float(intersection)/float(union)
    return distance

def basic(r1, r2):
    """Compute the basic distance between ratings r1 and r2 (must be
        dictionaries of the form {1: 3.0, 3: 2.0, 11:5.0})"""
    temp = 0
    n = 0
    for key in r1:
        if key in r2:
            temp += abs(r1[key] - r2[key])
            n += 1
    if n != 0:
        distance = float(temp)/float(n)
    else:
        distance = sys.float_info.max
    return distance

def computeNearestsNeigbhours(U, UM, dist, n):
    distances = []

    nbrUsersAdded = 0
    if dist == "cosine":
        maxCurrentDist = -1.0
    elif dist == "jaccard":
        maxCurrentDist = 0.0
    else:
        maxCurrentDist = sys.float_info.max

    for user in UM:
        if user != U:
            # compute the distance
            if dist == "cosine" or dist == "jaccard":
                if dist == "cosine":
                    distance = cosine(UM[user], UM[U])
                elif dist == "jaccard":
                    distance = jaccard(UM[user], UM[U])
                if nbrUsersAdded < n:
                    distances.append((distance, user))
                    nbrUsersAdded += 1
                elif distance > maxCurrentDist:
                    distances[0] = (distance, user)
                distances = sorted(distances, key=lambda items: items[0], reverse = False)
                maxCurrentDist = distances[0][0]
            else: # use basic distance
                distance = basic(UM[user], UM[U])
                if nbrUsersAdded < n:
                    distances.append((distance, user))
                    nbrUsersAdded += 1
                elif distance < maxCurrentDist:
                    distances[0] = (distance, user)
                distances = sorted(distances, key=lambda items: items[0], reverse = True)
                maxCurrentDist = distances[0][0]

    return distances

def computeAverageU(U,UM):
    """Compute the average rating of U"""
    sumRat = 0.0
    nbrItem = 0
    for item in UM[U]:
        sumRat += UM[U][item]
        nbrItem += 1
    average = sumRat/nbrItem
    return average

def recommend(U, UM, NameItem, m=5, n=500, dist="basic", normalizing="False", averageU = 0.0):
    """Give a list of recommendations for user U based on:
        - Find the n users more similar to u (with the distance "dist")
        - Compute the average (wieghted on distances) of their ratings for items that U didn't rate
        - Sort that list to give the items U could like first
        - Take the m items U is most likely to rate high (or all if there is no m items)"""

    nearests = computeNearestsNeigbhours(U, UM, dist, n)

    # find items those neighbors rated that U didn't
    sumRatingsNearests = {}
    for nearest in nearests:
        neighborRatings = UM[nearest[1]]

        # Scale weight in [0.0 1.0]
        if dist == "cosine":
            weight = (nearest[0]+1.0)/2.0
        elif dist == "jaccard":
            weight = nearest[0]
        else:
            weight = (-1.0*nearest[0]+5.0)/5.0
        userRatings = UM[U]
        for item in neighborRatings:
            if not item in userRatings:
                # sumRatingsNearests[item] = [sumOfRatings nunberOfRateings]
                if not item in sumRatingsNearests:
                    #sumRatingsNearests[item] = [neighborRatings[item], 1]
                    sumRatingsNearests[item] = [neighborRatings[item]*weight, weight]
                else:
                    sumRat = sumRatingsNearests[item][0]
                    nbr = sumRatingsNearests[item][1]
                    sumRatingsNearests[item][0] = sumRat+neighborRatings[item]*weight
                    sumRatingsNearests[item][1] = nbr+weight

    # if similar users rated exactly the same items, no new information...
    if len(sumRatingsNearests) == 0:
        print("The n = " + str(n) + " similar users rated exactly the same items")
        print("Try to increase n")

    # compute the average for the items concerned
    recommendations = []
    nbrItemsAdded = 0
    minCurrentRate = 0.0
    for item in sumRatingsNearests:
        sumRat = sumRatingsNearests[item][0]
        n = sumRatingsNearests[item][1]
        # -1 to delete the \n
        name = NameItem[item][0:len(NameItem[item])-1]
        if normalizing:
            #rating max = 5.0
            rat = min(float(sumRat)/float(n)+float(averageU),5.0)
        else:
            rat = float(sumRat)/float(n)
        if nbrItemsAdded < m:
            # add average on U if we use the normalizing datas
            recommendations.append((name,rat))
            nbrItemsAdded += 1
        elif rat > minCurrentRate:
            recommendations[0] = (name,rat)
        recommendations = sorted(recommendations, key=lambda items: items[1], reverse = False)
        minCurrentRate = recommendations[0][1]

    # sort the recommendations compared to the rating
    recommendations = sorted(recommendations, key=lambda items: items[1], reverse = True)

    return recommendations