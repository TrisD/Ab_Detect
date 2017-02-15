#!/usr/bin/env python

#=====================================================================#
#                            Importing packages                       #
#=====================================================================#

import Ab_Detect_init as self
from Ab_Detect_init import *

#=====================================================================#
#                            Importing data                           #
#=====================================================================#

def Import():

    print "Would you like to imput a data path or use the default y/n?"
    response = raw_input()
    if response == 'y':
        print "What is the path to your data? e.g. /Users/Fabian/Desktop/KODIAQ/spec"
        datapath = raw_input()
    elif response == 'n':
        datapath = '/Users/Fabian/Desktop/spec'
    else:
        print "unsupported option"
    print "Creating QSO list"
    t0 = time.time()
    os.system('find '+datapath+' -type f \( -name "*.fits" ! -name "*.sig.fits" \) > qsolist.dat')
    filelist = np.loadtxt('qsolist.dat',dtype=object)
    qsolist = []
    for line in filelist:
        qsolist.append(line.split('/')[-1].split('.')[0])
    print "QSO list created"
    print "time taken to create file list =", time.time() - t0
    return qsolist, datapath
    
def LoadInfo():
    print "Loading Labortory transition list from atom.dat file"
    labatom = np.genfromtxt('atom.dat',usecols=(0,1,2),dtype=[('labtrans','S6'),('lambda','f8'),('oscstr','f8')])

    redlist = np.loadtxt('redlist.dat',dtype=object)
    
    return labatom,redlist
