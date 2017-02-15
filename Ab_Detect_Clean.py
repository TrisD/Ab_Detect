#!/usr/bin/env python

#=====================================================================#
#                                 CLEAN                               #
#=====================================================================#

import Ab_Detect_init as self
from Ab_Detect_init import *

def Clean(qsolist,datapath):
    
    from astropy.io import fits
    from astropy.table import Table

    t0 = time.time()
    count = 0

    for spectrum in qsolist:
        FitsHeader = fits.open(datapath+'/'+spectrum+'.fits')
        HeaderData = FitsHeader[0].header
        try:
            offset = float(HeaderData['BZERO'])
            print "offest =", offset
            wa = 10**(HeaderData['CRVAL1']+(HeaderData['CRPIX1']-1+np.arange(HeaderData['NAXIS1']))*HeaderData['CDELT1'])
            fl = FitsHeader[0].data - offset
            FitsHeader = fits.open(spectrum.replace('fits','sig.fits'))
            er = FitsHeader[0].data - offset
            out = open(datapath+'/'+specname+'.dat','w')
            for i in range (0,len(fl)):
                wave = '%.7f'%wa[i]
                flux = '%.7E'%fl[i]
                error = '%7E'%er[i]
                out.write('{0:>15}{1:>20}{2:>20}\n'.format(wave,flux,error))
            out.close()
            count += 1
        except KeyError:
            print "No BZERO key detected in", spectrum
    print "BZERO checking time =", time.time() - t0
    print "The total number of corrections made was =", count



def ErrorCorrect(qsolist,datapath):
    
    t0 = time.time()
    
    for spectrum in qsolist:
        hdulist = fits.open(datapath+'/'+spectrum+'.sig.fits')
        hdu = hdulist[0]
        scidata = hdu.data
        badpix = np.where(scidata==-1)
        np.put(scidata,np.where(scidata==-1)[0],1000000)
        os.system('rm '+datapath+'/'+spectrum+'.sig.fits')
        fits.writeto(datapath+'/'+spectrum+'.sig.fits',scidata)
        print "Error array corrected for ", spectrum

    print "Total time to correct all error array's = ", time.time() - t0
    
def Telluric(wave):
    if wave < 6275 or 6312<wave<6867 or 6884<wave<7594 or 7621<wave:
        return True
    else:
        return False

def MopUp():
    #os.system('rm commands.dat')
    #os.system('rm fort.9')
    #os.system('rm results.dat')
    #os.system('rm termout')
    os.chdir('../')
    print 'Clean up complete'
