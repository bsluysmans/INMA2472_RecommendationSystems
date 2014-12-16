# -*- coding: utf-8 -*-
""" 
=============================================================
AUTHOR: Benoit Sluysmans, UCL-EPL
DATE: 10/11/2014
LINMA2472 - Questions de math discretes
=============================================================
Read the netflix datas and write the UM and the normalized UM in a file
"""
import time, pickle

def CreateMovies():
    """ Create a file that contains the link between the number of a movie and his name """    
    start_time = time.time()
    
    # Create the Movies structure
    Movies = {}
    with open("movie_titles.txt","r") as f:
        for line in f:
            split = line.split(',',2) # care if "," in the title
    	    Movies[int(split[0])] = split[2]
    	f.close()
    
    # Write Movies in a file
    with open("Movies","wb") as f:
        p = pickle.Pickler(f)
        p.dump(Movies)
        f.close()
    
    elapsed_time = time.time() - start_time
    print("\n Crating ""Movies"": "+ str(elapsed_time) +"s\n")
    	   
    return 1

def CreateUM(files):
    """ Create a file that contains the utility matrix """
    start_time = time.time()

    # Create the utility matrix
    UM = {}
    for filename in files:
        if filename.endswith(".txt"):
            with open(filename,"r") as f:
    	       firstline = f.readline()
    	       firstsplit = firstline.split(":")
    	       Num_movie = int(firstsplit[0])
    	       for line in f:
    	           split = line.split(",")
    	           UM.setdefault(int(split[0]), {})[Num_movie] = float(split[1])
    	       f.close()
    
    # Write utility matrix in a file
    with open("UM","wb") as f:
        p = pickle.Pickler(f)
        p.dump(UM)
        f.close()
        
    elapsed_time = time.time() - start_time
    print("\n Crating ""UM"": "+ str(elapsed_time) +"s\n")
    
    return 1
    
def CreateNormalUM(UM):
    """ Create a file that contains the normalized utility matrix """
    start_time = time.time()

    NormalUM = {}
    for user in UM:
        sumOnUser = 0.0
        nbrItem = 0
        for item in UM[user]:
            sumOnUser += UM[user][item]
            nbrItem += 1
        average = sumOnUser/nbrItem
        for item in UM[user]:
            NormalUM.setdefault(user, {})[item] = UM[user][item]-average
            
    # Write rouding utility matrix in a file
    with open("NormalUM","wb") as f:
        p = pickle.Pickler(f)
        p.dump(NormalUM)
        f.close()
        
    elapsed_time = time.time() - start_time
    print("\n Crating ""NormalUM"": "+ str(elapsed_time) +"s\n")
    
    return 1