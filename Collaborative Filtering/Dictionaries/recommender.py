# -*- coding: utf-8 -*-

"""
=============================================================
AUTHOR: Benoit Sluysmans, UCL-EPL
DATE: 10/11/2014
LINMA2472 - Questions de math discretes
=============================================================
Tests some recommendations
"""
import os, time, pickle
import collabFiltering, preprocess

start_time = time.time()

"""
Parameters
----------
"""
m = 5 # number of items to recommend
n = 100 # number of more similar neighbours to visit
dist = "cosine" # distance to use: "cosine", "jaccard" or "basic"
normalizing = False # "True" to use the normalizing datas, "False" otherwise
U = 6 # recommend movies to U

path = os.curdir()

"""
Generate the "Movies" file
--------------------------
"""
listfiles = os.listdir(os.curdir)
if "Movies" not in listfiles:
    preprocess.CreateMovies()

fMovies = open("Movies","rb")
pM = pickle.Unpickler(fMovies)
Movies = pM.load()
fMovies.close()

os.chdir(path+"/training_set")
"""
Generate the "UM" file
----------------------
"""
listfiles = os.listdir(os.curdir)
if "UM" not in listfiles:
    preprocess.CreateUM(listfiles)

f = open("UM", "rb")
p = pickle.Unpickler(f)
UM = p.load()
f.close()


"""
Generate the "NormalUM" file
------------------------------
"""
if normalizing:
    if "NormalUM" not in listfiles:
        preprocess.CreateNormalUM(UM)
    
    Nf = open("NormalUM", "rb")
    Np = pickle.Unpickler(Nf)
    NormalUM = Np.load()
    Nf.close()
    
elapsed_time = time.time() - start_time
print("\n Load time: "+ str(elapsed_time) +"\n")

"""
Tests
-----
"""
start_time = time.time()

if normalizing:
    averageU = collabFiltering.computeAverageU(U,UM)
    recommendations = collabFiltering.recommend(U, NormalUM, Movies, m, n, dist, normalizing, averageU)
else:
    recommendations = collabFiltering.recommend(U, UM, Movies, m, n, dist, normalizing)
for rec in recommendations:
    print(rec)

elapsed_time = time.time() - start_time
print("\n Recommendation time: "+ str(elapsed_time) +"\n")
