#Make simbad query, this is where we start

from astroquery.simbad import Simbad #Import astroquerey Simbad module
from pylab import *

Vmag_limits = [4,5,6,7,8,9,10]

#Set properties from Simbad to store 
Simbad.add_votable_fields('flux(V)') #Store V-mag
Simbad.add_votable_fields('pmra') #Store proper motion in RA
Simbad.add_votable_fields('pmdec') #Store proper motion in Dec.

for Vmag_limit in Vmag_limits: #Loop to make seperate lists for a variety of 
	#Query Simbad
	#Note we are including spectral types A0Va, A0Vb, and A0Vs
	objects = Simbad.query_criteria("(maintype=* | maintype=dS* | maintype=*iA | maintype=*iC) & Vmag < "+str(Vmag_limit)+" & (sptype=A0Va | sptype=A0Vb | sptype=A0Vs | sptype=A0V) & dec > -30")
	objects['PMRA'][isnan(objects['PMRA'])] = 0.0
	objects['PMDEC'][isnan(objects['PMDEC'])] = 0.0
	objects = objects[objects.argsort(keys='RA')] #Sort by RA
	lines = [] #Set up list to store lines for later outputting to file
	for i, obj in enumerate(objects):
		lines.append( str(i) + ' "' + obj['MAIN_ID'] +', V=%0.1f' % obj['FLUX_V'] + '" ' + obj['RA'] + ' ' + obj['DEC'] + ' 2000.00 %0.6f' % (obj['PMRA']/(15.0*1e3)) + ' %0.6f' % (obj['PMDEC']/1e3) )
	savetxt('A0V_min_Vmag_'+str(Vmag_limit)+'.wrk', lines, fmt="%s")