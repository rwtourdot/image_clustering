#!/usr/bin/env python

import sys,math,copy
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from cluster import *
from scipy.spatial import Delaunay,Voronoi,voronoi_plot_2d

def load_png_image_file(fid,channel):
	img = mpimg.imread(path_to_file)
        org_img = copy.deepcopy(img)
	lum_img = img[:,:,channel]  #chooseing one of three img[:,:,1] img[:,:,2]
	len_lum = np.shape(lum_img)	
	return lum_img,len_lum,org_img

# this line of code reads image data into an RGB array with three values
path_to_file = str(sys.argv[1])
cutoff = float(sys.argv[2])

magfile = path_to_file.split('/')[-1]
directory = path_to_file.split('/')[0:-1]
print "/".join(directory) + "/" + magfile

#img = mpimg.imread(path_to_file)
channel = 0
lum_img,len_lum,ori_img = load_png_image_file(path_to_file,channel)

# this code seperates out the R G or B color channels
# cutoff 0.5,0.6,0.7

#ori_img = img
#lum_img = img[:,:,channel]  #img[:,:,1] img[:,:,2]

#cutoff = 0.6
lum_img[lum_img > cutoff] = np.nan
lum_img[abs(lum_img) < cutoff] = 1.0
lum_img[lum_img == np.nan] = 0.0
len_lum = np.shape(lum_img)
group_img = locate_clusters(lum_img,len_lum)
print "done locate_clusters"
clust = generate_clusters(group_img)
print "done generate_clusters"
clust_cut = cluster_cleanup(clust)
for c in clust_cut:
	c.geometry_calculations()
print "done cluster_cleanup"

xypos = []
vorxy = []
for c in clust_cut:
	xypos.append((c.xcent,c.ycent))
	vorxy.append((c.ycent,c.xcent))

tri = Delaunay(xypos)
vor = Voronoi(vorxy)

cmx = [ clu.xcent for clu in clust_cut ] 
cmy = [ clu.ycent for clu in clust_cut ] 
rga = [ clu.Rg/4.0 for clu in clust_cut ] 
aratio = [ clu.relative_shape for clu in clust_cut ]

plt.close('all')
fig,((ax1, ax2),(ax3, ax4)) = plt.subplots(nrows=2,ncols=2)

#lum_img[lum_img == 0.0] = np.nan 
ax1.imshow(ori_img,interpolation='nearest')  #lum_img
ax1.set_title('Raw RGB')
ax1.set_aspect('equal',adjustable='box')

ax2.set_title('Clusters')
if len(cmx) > 0:
	#ax1.triplot(cmy,cmx,tri.simplices.copy())
	ax2.scatter(cmy,cmx,s=rga,c=aratio,alpha = 0.6)
ax2.set_xlim([0,1000])
ax2.set_ylim([0,1000])
ax2.invert_yaxis()
ax2.set_aspect('equal',adjustable='box')

ax3.set_title('Connectivity')
if len(cmx) > 0:
	ax3.triplot(cmy,cmx,tri.simplices.copy())
	#ax3.scatter(cmy,cmx,s=rga,c=aratio,alpha = 0.6)
ax3.set_xlim([0,1000])
ax3.set_ylim([0,1000])
ax3.invert_yaxis()
ax3.set_aspect('equal',adjustable='box')

ax4.set_title('Voronoi')
if len(cmx) > 0:
	voronoi_plot_2d(vor,ax4)
	#ax4.scatter(cmy,cmx,s=rga,c=aratio,alpha = 0.6)
ax4.set_xlim([0,1000])
ax4.set_ylim([0,1000])
ax4.invert_yaxis()
ax4.set_aspect('equal',adjustable='box')



plt.tight_layout()
#plt.show()
fig.savefig("/".join(directory) + "/voronoi_cluster_cutoff_"+ str(cutoff) +"_"+magfile,dpi=300)

