# -*- coding: utf-8 -*-

"""
=============================================================
AUTHORS: Alexandre Laterre & Benoit Sluysmans, UCL-EPL
DATE: 28/11/2014
LINMA2472 - Questions de math discretes
=============================================================
Tests some recommendations
"""

import os, time, pickle
import numpy as np
from scipy import where
from collabFiltering import recommend


"""
Parameters
----------
"""
m = 5 # number of items to recommend
n = 100 # number of more similar neighbours to visit
U = 6 # recommand movies to U
normalizing = True # True to use normalized UM, False otherwise

UMname = "total_matrix_csr.pickle" # utility matrix
NormalUMname = "Normaltotal_matrix_csr.pickle" # normal utility matrix
meansName = "means_total" # means vector

path = os.curdir # path to the files needed

"""
Load files
----------
"""
start_time = time.time()

# --- Link to netflix' users numbers ---
f = open("users_list.idx","rb")
Users = np.fromfile(f,dtype=np.dtype('uint32'),count=-1,sep="")
f.close()
Ubis = where(Users == U)[0][0]

# --- Link to the names of the movies ---
f = open("movies_list.idx","rb")
p = pickle.Unpickler(f)
Movies = p.load()
f.close()

# --- Utility matrix ---
if normalizing:
    f = open(NormalUMname, "rb")
else:
    f = open(UMname, "rb")
p = pickle.Unpickler(f)
UM = p.load()
f.close()

# --- Means vector ---
if normalizing:
    f = open(meansName, "rb")
    p = pickle.Unpickler(f)
    means = p.load()
    f.close()

elapsed_time = time.time() - start_time
print("\n - Load time: "+ str(elapsed_time))

"""
Tests
-----
"""
start_time = time.time()

# --- Compute the recommendations for U ---
if normalizing:
    recommendations = recommend(Ubis, UM, m, n, means[U], normalizing)
else:
    recommendations = recommend(Ubis, UM, m, n)

elapsed_time = time.time() - start_time
print(" - Recommendation time: "+ str(elapsed_time) +"\n")

# --- Print the results ---
print("Top " + str(m) +" movies user "+str(U)+ " may like")
print("----------------------------\n")
for rec in recommendations:
    name = Movies[int(rec[0])][0:len(Movies[int(rec[0])])-1]
    rating = rec[1]
    print(name+": "+str(rating))
