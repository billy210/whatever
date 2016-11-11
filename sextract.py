
#######Comments 
#
#
####10/21 the code currently takes in a set of transit images, finds the brightest star for each image, and reads out the value. will need to set higher threshold because occasionally 2 stars are measured.
#
#
#####Step 2 will be to read values out to a .txt file where they can be plotted from. real master flats are darks will need to be incorporated first. for now it works for what it needs to do and plotting can come later.

#########################################################################
import numpy as np
import sep
import glob

# additional setup for reading the test image and displaying plots
from astropy.io import fits
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.patches import Ellipse
import pylab as pl

rcParams['figure.figsize'] = [10., 8.]

#######################################################################


s = raw_input('type glob pattern for file list: ')
flist = glob.glob(s)
print flist

#creates an empty file to fill with opened input data
inptarray=[]
jd = np.zeros(len(flist))
f= open('fluxout.txt','w')
#Open the images given at the command line and place them in an array
for i in range(len(flist)): 
     step1 = flist[i]  
     step2 = fits.open(step1)
     #align1 = step2[0].data 
     jd[i]=step2[0].header['JD']
     data_sub = step2[0].data   
     ###############inptarray.append(step3)

     #alignd=fits.open('dark_2s_-001.fit')
     #dark=alignd[0].data

     #alignf=fits.open('masterflat.fits')
     #flat=alignf[0].data

     #data_sub=((align1-dark)/flat)

     ####objects = sep.extract(data_sub, 1.5, err=bkg.globalrms)
     sep.set_extract_pixstack(50000) 
     data_sub = data_sub.byteswap().newbyteorder()
     objects = sep.extract(data_sub, 3000)

     # how many objects were detected
     len(objects)

     # plot background-subtracted image
     fig, ax = plt.subplots()
     m, s = np.mean(data_sub), np.std(data_sub)
     im = ax.imshow(data_sub, interpolation='nearest', cmap='gray',
                    vmin=m-s, vmax=m+s, origin='lower')

     # plot an ellipse for each object
     for j in range(len(objects)):
     #for i in range(1):
         e = Ellipse(xy=(objects['x'][j], objects['y'][j]),
                     width=7*objects['a'][j],
                     height=7*objects['b'][j],
                     angle=objects['theta'][j] * 180. / np.pi)
         e.set_facecolor('none')
         e.set_edgecolor('red')
         ax.add_artist(e)
         #pl.draw()
         #pl.show()

         # available fields
         #print objects.dtype.names

         flux, fluxerr, flag = sep.sum_circle(data_sub, objects['x'], objects['y'],
                                     3.0, gain=1.0)
         xval= objects['x']
         yval= objects['y']

 
         #for j in range(len(objects)):
         for k in range(1):
             print("object {:d}: flux = {:f} {:f}".format(j, flux[j], fluxerr[j], xval[j], yval[j]))
	     print(i,jd[i])
             outline="%s %s %s %s\n"%(j,jd[i],flux[j],fluxerr[j])
             f.write(outline)
	     step2.close()
f.close()
#before loop
#f=file.open('fluxout.txt,'w')

#in loop
#outline="%s %s\n"%(var1,var)
#f.write(outline)
#after loop
#f.close()

             
#data=[]
#for ( looopy  )
#data.append([values values vals])

