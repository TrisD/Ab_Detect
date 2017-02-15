#!/usr/bin/env python

#=====================================================================#
#                            Importing packages                       #
#=====================================================================#

import Ab_Detect_init as self
from Ab_Detect_init import *

#=====================================================================#
#                            Find Absorption                          #
#=====================================================================#

def Find(spectrum,datapath,labatom,redlist):#Find(qsolist,datapath,labatom,redlist):
    
    ##print "Loading Labortory transition list from atom.dat file"
    ##labatom = np.genfromtxt('atom.dat',usecols=(0,1,2),dtype=[('labtrans','S6'),('lambda','f8'),('oscstr','f8')])
    
    ##redlist = np.loadtxt('redlist.dat',dtype=object)
    
    #if os.path.exists('Analysis')==False:
    #    os.system('mkdir Analysis')
    
    #os.system('cd Analysis')
        
    #for spectrum in qsolist:

    print "Scanning", spectrum
        
    qsoname = spectrum.split('_')[0]
    zem = float(redlist[np.where(redlist[:,0]==qsoname)[0][0],1])
    wmin, wmax = (1 + zem) * 1215.67, (1 + zem) * max(labatom['lambda'])
    print 'Lambda min and max for'+spectrum+'is :', wmin, wmax
    os.system('mkdir -p '+spectrum)
    os.chdir(spectrum)
    #target = 'spec.dat' if flag==1 else 'spec.fits'
    target = 'spec.fits'
    #if flag==1 and os.path.exists('spec.dat')==False:
    #    os.system('ln -s '+datapath+'/'+spectrum+'.dat spec.dat')
    #elif os.path.exists('spec.fits')==False:
    #    os.system('ln -s '+datapath+'/'+spectrum+'.fits spec.fits')
    #    os.system('ln -s '+datapath+'/'+spectrum+'.sig.fits spec.sig.fits')
    if os.path.exists('spec.fits')==False:
        os.system('ln -s '+datapath+'/'+spectrum+'.fits spec.fits')
        os.system('ln -s '+datapath+'/'+spectrum+'.sig.fits spec.sig.fits')
    commands = open('commands.dat','w')
    commands.write('rd '+target+'\n\nab\n\n5\n\n'+str(wmin)+','+str(wmax)+'\nexit')
    commands.close()
    os.system('rdgen < commands.dat > termout')
        
    ''' Load RDGEN output into array + remove telluric regions '''
        
    flag = 0 
    results = np.empty((0,4),dtype=float)
    opfile = open('results.dat','w')
    RDout = np.loadtxt('fort.9',dtype=str,delimiter='\n',skiprows=6)

#    AbsLoad = np.loadtxt('termout',dtype=str,delimiter='\n',skiprows=34)

 #   for i in range(len(AbsLoad)):
  #      if AbsLoad[i][1:4]=='abs' and i < len(AbsLoad)-2:
   #         wave = float(AbsLoad[i][11:19])
    #        error = float(AbsLoad[i][21:26])
     #       if AbsLoad[i][39:45]=='******':
      #          ew = 0.1
       #     else:
        #        ew = float(AbsLoad[i][39:45])
         #   if AbsLoad[i][48:54]=='******':
          #      ewerror = 0.1
           # else:
            #    ewerror = float(AbsLoad[i][48:54])
            #results = np.vstack((results,[wave,error,ew,ewerror]))
              
    for i in range(len(RDout)):
        ##if RDout[i][3:6]=='***':
        ##    warn = 1
        ##    i += 1
        if RDout[i][1:4]=='abs' and (i==len(RDout)-1 or RDout[i+1][1:4]=='abs') and RDout[i][35:45]!='*********':##and warn==0
            wave = float(RDout[i][9:19])
            if Telluric(wave)==True:
                if float(RDout[i][21:26])==0:
                    error = 0.001
                if float(RDout[i][21:26])!=0:
                    error = float(RDout[1][21:26])
                if RDout[i][37:40]!='***':
                    ew = float(RDout[i][35:45]) #37-40
                else:
                    ew = 0.001
                if RDout[i][47:50]=='***' or float(RDout[i][48:54])==0:
                    ewerror = 0.001
                else:
                    ewerror = float(RDout[i][48:54])
                results = np.vstack((results,[wave,error,ew,ewerror]))
                opfile.write('{0:>12}\n'.format('%.5f'%wave))
        if RDout[i][1:4]=='abs' and i<len(RDout)-1 and RDout[i+1][2:5]=='***' and RDout[i][35:45]!='*********':
            flag = 1
            i += 1
        if RDout[i][2:5]=='***' and flag==1:
            wave = float(RDout[i][9:18])
            if Telluric(wave)==True:
                if float(RDout[i][21:26])==0:
                    error = 0.001
                if float(RDout[i][21:26])!=0:
                    error = float(RDout[i][21:26])
                if RDout[i][37:40]!='***':
                    ew = float(RDout[i][34:44])
                else:
                    ew = 0.001
                if RDout[i][47:50]=='***' or float(RDout[i][43:50])==0:
                    ewerror = 0.001
                else:
                    ewerror = float(RDout[i][43:50])
                results = np.vstack((results,[wave,error,ew,ewerror]))
                opfile.write('{0:>12}\n'.format('%.5f'%wave))
        if flag==1 and RDout[i][2:5]!='***':
            flag = 0
    opfile.close

    return(zem,results,labatom)

#=====================================================================#
#                     Statistical Significance                        #
#=====================================================================#
def CrossCorrelate(zem,results,labatom):
    t0 = time.time()
    outfile = open('detections.dat','w')
    vals = []
    stepsize = 0.001
    for z in np.arange(0.1,zem,stepsize):
        nsep = 0
        idarray = np.empty((0,5))
        validationarray = np.empty((0,5))
        for i in range(len(labatom)):
            idx = np.where(abs(results[:,0]-labatom['lambda'][i] * (z+1)) < 1.0)[0]#0.125)[0]
            
            if len(idx)>0:
                for k in idx:
                    idarray = np.vstack((idarray,[labatom['labtrans'][i]
                                                  ,float(labatom['lambda'][i])
                                                  ,float(labatom['oscstr'][i])
                                                  ,float(results[k,2])
                                                  ,float(results[k,3])]))
        #print idarray
        for i in range(len(idarray)):
            idxs = np.where((idarray[i,0]==idarray[:,0]) & (idarray[i,1]!=idarray[:,1]))[0]
            for q in idxs:
                if (float(idarray[i][3]))/float(idarray[q][3]>=1) and float(idarray[i][3])/float(idarray[q][3]) <=float(idarray[i][2])/(float(idarray[q][2])+0.05):
                    if idarray[q][1] not in validationarray:
                        validationarray = np.vstack((validationarray,[idarray[q]]))
                    if idarray[i][1] not in validationarray:
                        validationarray = np.vstack((validationarray,[idarray[i]]))
            if idarray[i][0] not in validationarray and idarray[i][1] not in validationarray:
                validationarray = np.vstack((validationarray,[idarray[i]]))
        transcounter = coll.Counter(validationarray[:,0]).most_common(1)
        if len(transcounter)>0:
            transcounter1 = transcounter[0]
            if float(transcounter1[1])>=2:
                nsep += len(validationarray)
        if nsep>=2:
            outfile.write('{0:>6} {1:>5}\n'.format('%.4f'%z,'%i'%nsep))
            for isep in range(nsep):
                vals.append(z)
    outfile.close()

    print "cross time = ", time.time()-t0

    return vals,stepsize
def MonteCarlo():
    print "HI"

def ResultPlot(vals,zem,stepsize,spectrum):
    if len(vals)==0:
        print "No detections made"
    else:
        binsize = int((zem-0.1)/stepsize) 
        #print vals
        print 'binsize =', binsize
        print
        print
        print 'stepsize =', stepsize
        print 
        print 
        print 'z =', zem
        fig = plt.figure()
        ax = fig.add_subplot(211)
        n, bins, patches = ax.hist(vals,binsize, histtype='step', stacked=True, fill=True, alpha=0.5)
        plt.xlabel('Redshift')
        plt.ylabel('Number of detections')
        plt.savefig('detections.pdf')
        
        print 'Analysis done for qso', spectrum
