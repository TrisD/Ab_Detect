#!/usr/bin/env python

import Ab_Detect_init as self
from Ab_Detect_init import *

''' Ab_Dtect Tristan Dwyer 2016  '''

#=====================================================================#
#                       Initial print statement                       #
#=====================================================================#

if len(sys.argv)==1:
    print ""
    print "===================================    Ab_Detect    ==================================="
    print ""
    print "Usage: Ab_Detect  --options"
    print ""
    print "Possible option:"
    print ""
    print "    --detect     ......... : Detect absorption systems in a fits file"
    print ""
    print "    --correction ......... : Apply error correction to a single error array file"
    print ""
    print "    JXXXXX-XXXXX.fits --autodetect ......... : Run Ab_Detect for single QSO in folder"
    print "======================================================================================="
    print ""
    print ""
    quit()

#=====================================================================#
#                           Scripts to call                           #
#=====================================================================#

if '--detect' in sys.argv:
    #self.Import()
    qsolist, datapath = Import()
    #self.Clean(qsolist)
    print "Would you like to check for the BZERO offset, y/n?"
    response = raw_input()
    if response == 'y':
        Clean(qsolist,datapath)
    elif response == 'n':
        print "BZERO key not checked for"
    else:
        print "unsupported response, will now check for the BZERO key"
        print 
        print
        Clean(qsolist,datapath)
    print "Would you like to correct the error array if it contains values of -1 to interface w/ RDGEN, y/n?"
    response = raw_input()
    if response == 'y':
        ErrorCorrect(qsolist,datapath)
    elif response == 'n':
        print "Not correcting error array values"
    else:
        print "unsupported response, checking error arrays"
        print
        print
        ErrorCorrect(qsolist,datapath)
    #Find(qsolist,datapath)
    '''Playing around '''
    
    labatom,redlist = LoadInfo()
    for spectrum in qsolist:
        zem,results,labatom = Find(spectrum,datapath,labatom,redlist)
        vals, stepsize = CrossCorrelate(zem,results,labatom)
        ResultPlot(vals,zem,stepsize,spectrum)
        MopUp()
    ''' old '''
    ##zem,results,labatom = Find(qsolist,datapath)
    ##vals,stepsize = CrossCorrelate(zem,results,labatom)
    ##ResultPlot(vals,zem,stepsize)
