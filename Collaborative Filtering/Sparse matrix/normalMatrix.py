# -*- coding: utf-8 -*-

"""
=============================================================
AUTHORS: Alexandre Laterre & Benoit Sluysmans, UCL-EPL
DATE: 28/11/2014
LINMA2472 - Questions de math discretes
=============================================================
Transform utility matrix in normalized matrix and create mean rating for each user
"""

import os, time, pickle
from numpy import *

UMname = "total_matrix_csr.pickle" # utility matrix
NormalUMname = "Normaltotal_matrix_csr.pickle" # normal utility matrix
meansName = "means_total" # means vector
path = os.curdir # path to the files needed

start_time = time.time()

"""
Load UM
-------
"""
f = open(UMname, "rb")
p = pickle.Unpickler(f)
UM = p.load()
f.close()

x = UM.shape[0]
y = UM.shape[1]

def meanUsers(UM,x):
    """ Compute the mean of each user vector for the movies seen """
    
    means = zeros((x,1))
    for i in xrange(x):
        line = UM[i,:].todense()
        line = array(line) # matrix to array to perform search operations
        
        nz = nonzero(line)
        m = mean(line[nz]) # mean of nonzero elements
        means[i] = m
        
    return means
    
def normalize(UM,x,y,means):
    """ Return the normalized utility matrix"""
    
    NormalUM = lil_matrix( (x,y), dtype=int8 )
    for i in xrange(x):
        line = UM[i,:].todense()
        line = array(line) # matrix to array to perform search operations
        
        nz = nonzero(line)
        NormalUM[i,nz[1]] = UM[i,nz[1]]-means[i]
        
    NormalUM = NormalUM.tocsr()
        
    return NormalUM
        
means = meanUsers(UM,x)
NormalUM = normalize(UM,x,y,means)

"""
Write NormalUM and means
------------------------
"""
f = open(NormalUMname, "wb")
p = pickle.Pickler(f)
p.dump(NormalUM)
f.close()

f = open(meansName, "wb")
p = pickle.Pickler(f)
p.dump(means)
f.close()


elapsed_time = time.time() - start_time
print("\n - Normalizing time: "+ str(elapsed_time))