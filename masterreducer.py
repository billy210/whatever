#########################################################################
import numpy as np
from astropy.io import fits
import glob


#######################################################################


s = raw_input('type glob pattern for image files list: ')
flist = glob.glob(s)
print flist

#creates an empty file to fill with opened input data
inptarray=[]

alignd=fits.open('masterdark.fits')
dark=alignd[0].data

alignf=fits.open('masterflat.fits')
flat=alignf[0].data


#Open the images given at the command line and place them in an array
for i in range(len(flist)): 
     step1 = flist[i]  
     step2 = fits.open(step1)
     step3 = step2[0].data 
     #inptarray.append(step3)

     data_sub=(step3-dark)/flat
     
     final=fits.PrimaryHDU(data_sub)
     final.writeto(flist[i][0:26]+'sub'+str(i)+.fits,clobber='True')
