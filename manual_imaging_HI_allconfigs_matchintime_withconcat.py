
'''
'Manual' imaging by just passing the full MSs directly to tclean.
There is clearly an issue with how tclean is using the uv-data when multiple
MSs are given as a list (e.g. the beam size is not constant when re-running the same image).
This script uses a concatenated MS instead.

* All data w/ contsub
* All data w/o contsub

Adjust time integrations per config to match 1:1:1:1

NOTE: The ultimate target is 2:2:2:1, though? Check this and re-run if needed.

NOTE: there are 6.5 hr in A config from 18A-467

'''


from tasks import tclean

import os
from copy import copy

basepath = "/mnt/space/ekoch/VLA_tracks/"

datapath = os.path.join(basepath, '18A-467/HI_allconfig_imagingtests/')

vis_nocontsub = os.path.join(datapath, 'M31_Field17_HI_ABCD.ms')

# Each config is its own SPW in the concatenated data.
config_to_spwmapping = {'D': 0, 'C': 1, 'B': 2, 'A': 3}


xltime_scans = \
{'A': '1920,1922,1924,1926,1927,1929,1931,1933,1935,1937,1939,1941',
 'C': '1025,1157,1287,1033,909,1295,1041,1219,1309,917,1049,1317,925,1057,933,1065,1195,941,1181,1165,1073,1203,949,1211,1087,963,1095,971,1103,1233,979,1111',
 'B': '1536,1666,1412,1750,1674,1420,1550,1682,1428,1774,1558,1436,1566,1696,1444,1574,1704,1820,1452,1582,1712,1842,1460,1758,1334,1720,1850,1866,1342,1728,1474,1590,1350,1736',
 'D': '908,845,782,719,656,593,530,467,404,341,278,215,152,89,26'}

run_dirtyimaging = True
run_shallowclean = False
run_deepclean = False

# Everything in one:

with_Aconfig = [True, False]

# with_contsub = [False, True]
with_contsub = [False]
weightings = ['natural']
# weightings = ['natural', 'briggs']
# tapers = ['', '5arcsec']
tapers = ['']

imsizes = [4096, 2048]
cellsizes = ['0.5arcsec', '1arcsec']

for myimsize in imsizes:

    for mycellsize in cellsizes:

        for has_Aconfig in with_Aconfig:

            for contsub in with_contsub:

                if contsub is True:
                    myvis = vis_contsubs
                    image_str = 'contsub'
                else:
                    myvis = vis_nocontsub
                    image_str = 'nocontsub'

                # Remove the last track from A config to compare w/ and w/o A tracks
                if has_Aconfig:
                    confs = 'ABCD'
                else:
                    confs = 'BCD'

                scan_select = ",".join([xltime_scans[config] for config in confs])

                for weight in weightings:

                    for taper in tapers:

                        print("On {0} {1} {2}\nIncludes A conf? {3}".format(weight, taper, image_str, has_Aconfig))

                        print("On image size {0} with cell {1}".format(myimsize, mycellsize))

                        imagename_run = os.path.join(datapath,
                                                    'M31_Field17_{0}_{1}_{2}_{3}_{4}_{5}_xltimematched_concatms'
                                                    .format(confs,
                                                            weight,
                                                            taper,
                                                            image_str,
                                                            myimsize,
                                                            mycellsize))

                        # Dirty map.
                        if run_dirtyimaging:

                            out = tclean(vis=myvis,
                                        field='M31*',
                                        spw='',
                                        intent='',
                                        datacolumn='corrected',
                                        imagename=imagename_run,
                                        imsize=4096,
                                        cell=mycellsize,
                                        scan=scan_select,
                                        phasecenter='',  # Only one field
                                        nchan=30,
                                        start='-270km/s',
                                        width='10km/s',
                                        specmode='cube',
                                        outframe='LSRK',
                                        gridder='mosaic',
                                        chanchunks=-1,
                                        mosweight=True,
                                        pblimit=0.5,
                                        pbmask=0.5,
                                        deconvolver='multiscale',
                                        scales=[0, 5, 10],
                                        restoration=True,
                                        pbcor=False,
                                        weighting=weight,
                                        robust=0.0,
                                        uvtaper=[taper],
                                        niter=0,
                                        cycleniter=100,  # Force many major cycles
                                        nsigma=4.,
                                        usemask='auto-multithresh',
                                        sidelobethreshold=1.0,
                                        noisethreshold=3.0,
                                        lownoisethreshold=1.5,
                                        negativethreshold=0.0,
                                        minbeamfrac=0.1,
                                        growiterations=75,
                                        dogrowprune=True,
                                        minpercentchange=1.0,
                                        fastnoise=False,
                                        threshold='',
                                        interactive=0,
                                        savemodel='none',
                                        parallel=False,
                                        calcres=True,
                                        calcpsf=True,
                                        smallscalebias=0.0,
                                        restfreq='1.42040575177GHz',
                                        )
