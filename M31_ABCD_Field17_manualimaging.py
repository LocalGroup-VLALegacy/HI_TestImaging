
'''
'Manual' imaging by just passing the full MSs directly to tclean.
There is clearly an issue with how tclean is using the uv-data when multiple
MSs are given as a list (e.g. the beam size is not constant when re-running the same image).
This script uses a concatenated MS instead.

* All data w/ contsub
* All data w/o contsub

Adjust time integrations per config to match 2:2:2:1 and using all the
available time for this field.

NOTE: there are 6.5 hr in A config from 18A-467

'''

from tasks import tclean

from cleanhelper import cleanhelper as clp

import os
from copy import copy

basepath = "/mnt/space/ekoch/VLA_tracks/"

datapath = os.path.join(basepath, '18A-467/HI_allconfig_imagingtests/')
imagepath = os.path.join(datapath, 'ABCD_weighting_and_taper')

if not os.path.exists(imagepath):
    os.mkdir(imagepath)

vis_nocontsub = os.path.join(datapath, 'M31_Field17_HI_ABCD.ms')
vis_contsub = os.path.join(datapath, 'M31_Field17_HI_ABCD.ms.contsub')

# Each config is its own SPW in the concatenated data.
config_to_spwmapping = {'D': 0, 'C': 1, 'B': 2, 'A': 3}


xltime_scans = \
{'A': '1920,1922,1924,1926,1927,1929,1931,1933,1935,1937,1939,1941',
 'C': '1025,1157,1287,1033,909,1295,1041,1219,1309,917,1049,1317,925,1057,933,1065,1195,941,1181,1165,1073,1203,949,1211,1087,963,1095,971,1103,1233,979,1111',
 'B': '1536,1666,1412,1750,1674,1420,1550,1682,1428,1774,1558,1436,1566,1696,1444,1574,1704,1820,1452,1582,1712,1842,1460,1758,1334,1720,1850,1866,1342,1728,1474,1590,1350,1736',
 'D': '908,845,782,719,656,593,530,467,404,341,278,215,152,89,26'}

run_dirtyimaging = False
run_shallowclean = False
run_deepclean = True

# Everything in one:

# with_contsub = [False, True]
with_contsub = [True]

# matched_time = [False, True]
matched_time = [False]

# nchan = 30
nchan = 1
# startvel = '-270km/s'
startvel = '-180km/s'

imaging_setups = [{'weight': 'briggs', 'robust': 1., 'taper': "", 'cell': '0.9arcsec'},
                #   {'weight': 'briggs', 'robust': 0., 'taper': "", 'cell': '0.4arcsec'},
                #   {'weight': 'briggs', 'robust': -1., 'taper': "", 'cell': '0.3arcsec'},
                #   {'weight': 'natural', 'robust': 0., 'taper': "", 'cell': '1.8arcsec'},
                #   {'weight': 'briggs', 'robust': 1., 'taper': "5arcsec", 'cell': '2.2arcsec'},
                #   {'weight': 'briggs', 'robust': 1., 'taper': "10arcsec", 'cell': '3.7arcsec'},
                #   {'weight': 'briggs', 'robust': 1., 'taper': "20arcsec", 'cell': '6.2arcsec'},
                #   {'weight': 'briggs', 'robust': 1., 'taper': "30arcsec", 'cell': '8.6arcsec'},
                  ]

# Set a constant angular size for the image.
ang_size = 1. # deg

# Using all configs here
confs = 'ABCD'

mycleanmask = 'M31_Field17_ABCD_cleanmask_from_15A.mask'

mypblimit = 0.1

for i, setup_dict in enumerate(imaging_setups):

    print("On image test {0}/{1}".format(i + 1, len(imaging_setups)))

    for time_match in matched_time:

        for contsub in with_contsub:

            if contsub is True:
                myvis = vis_contsub
                image_str = 'contsub'
            else:
                myvis = vis_nocontsub
                image_str = 'nocontsub'

            if time_match:
                scan_select = ",".join([xltime_scans[config] for config in confs])
            else:
                scan_select = ""

            myweight = setup_dict['weight']
            myrobust = setup_dict['robust']
            mytaper = setup_dict['taper']
            mycell = setup_dict['cell']

            mycell_float = float(mycell.split('arcsec')[0])

            myimsize = clp.getOptimumSize(int(ang_size * 3600. / mycell_float))

            print("On image size {0} with cell {1}".format(myimsize, mycell))

            imagename_run = os.path.join(imagepath,
                                        'M31_Field17_{0}_{1}_robust{2}_taper_{3}_{4}_{5}_{6}_{7}_concatms'
                                        .format(confs,
                                                myweight,
                                                myrobust,
                                                mytaper if len(mytaper) > 0 else "none",
                                                image_str,
                                                myimsize,
                                                mycell,
                                                'xltimematched' if time_match else "allscans"))

            # Dirty map.
            if run_dirtyimaging:

                out = tclean(vis=myvis,
                            field='M31*',
                            spw='',
                            intent='',
                            datacolumn='corrected',
                            imagename=imagename_run,
                            imsize=myimsize,
                            cell=mycell,
                            scan=scan_select,
                            phasecenter='',  # Only one field
                            nchan=nchan,
                            start=startvel,
                            width='10km/s',
                            specmode='cube',
                            outframe='LSRK',
                            gridder='mosaic',
                            chanchunks=-1,
                            mosweight=True,  # False,
                            pblimit=mypblimit,
                            pbmask=mypblimit,
                            deconvolver='multiscale',
                            scales=[0, 5, 10],
                            restoration=True,
                            pbcor=False,
                            weighting=myweight,
                            robust=myrobust,
                            uvtaper=[mytaper],
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

            # Shallow clean with clean mask.
            if run_shallowclean:

                # Make copies of the dirty image
                os.system("cp -r {0}.image {0}.image_dirty".format(imagename_run))

                mythreshold = '1.5mJy/beam'

                out = tclean(vis=myvis,
                            field='M31*',
                            spw='',
                            intent='',
                            datacolumn='corrected',
                            imagename=imagename_run,
                            imsize=myimsize,
                            cell=mycell,
                            scan=scan_select,
                            phasecenter='',  # Only one field
                            nchan=nchan,
                            start=startvel,
                            width='10km/s',
                            specmode='cube',
                            outframe='LSRK',
                            gridder='mosaic',
                            chanchunks=-1,
                            mosweight=True,  # False,
                            pblimit=mypblimit,
                            pbmask=mypblimit,
                            deconvolver='multiscale',
                            scales=[0, 6, 18, 30, 60, 120, 240],
                            restoration=True,
                            pbcor=False,
                            weighting=myweight,
                            robust=myrobust,
                            uvtaper=[mytaper],
                            niter=100000,
                            cycleniter=500,  # Force many major cycles
                            nsigma=4.,
                            # usemask='auto-multithresh',
                            usemask='user',
                            mask=mycleanmask,
                            sidelobethreshold=1.0,
                            noisethreshold=3.0,
                            lownoisethreshold=1.5,
                            negativethreshold=0.0,
                            minbeamfrac=0.1,
                            growiterations=75,
                            dogrowprune=True,
                            minpercentchange=1.0,
                            fastnoise=False,
                            threshold=mythreshold,
                            interactive=0,
                            savemodel='none',
                            parallel=False,
                            calcres=False,
                            calcpsf=False,
                            smallscalebias=0.0,
                            restfreq='1.42040575177GHz',
                            )


            # Deep clean with NO clean mask.
            if run_deepclean:

                # Make copies of the dirty image
                os.system("cp -r {0}.image {0}.image_stage1".format(imagename_run))
                os.system("cp -r {0}.residual {0}.residual_stage1".format(imagename_run))
                os.system("cp -r {0}.model {0}.model_stage1".format(imagename_run))

                # Delete the existing mask
                os.system("rm -rf {0}.mask".format(imagename_run))

                mythreshold = '1.5mJy/beam'

                out = tclean(vis=myvis,
                            field='M31*',
                            spw='',
                            intent='',
                            datacolumn='corrected',
                            imagename=imagename_run,
                            imsize=myimsize,
                            cell=mycell,
                            scan=scan_select,
                            phasecenter='',  # Only one field
                            nchan=nchan,
                            start=startvel,
                            width='10km/s',
                            specmode='cube',
                            outframe='LSRK',
                            gridder='mosaic',
                            chanchunks=-1,
                            mosweight=True,  # False,
                            pblimit=mypblimit,
                            pbmask=mypblimit,
                            deconvolver='multiscale',
                            scales=[0, 6, 18, 30, 60, 120, 240],
                            restoration=True,
                            pbcor=False,
                            weighting=myweight,
                            robust=myrobust,
                            uvtaper=[mytaper],
                            niter=100000,
                            cycleniter=500,  # Force many major cycles
                            nsigma=4.,
                            # usemask='auto-multithresh',
                            usemask='pb',
                            mask='',
                            sidelobethreshold=1.0,
                            noisethreshold=3.0,
                            lownoisethreshold=1.5,
                            negativethreshold=0.0,
                            minbeamfrac=0.1,
                            growiterations=75,
                            dogrowprune=True,
                            minpercentchange=1.0,
                            fastnoise=False,
                            threshold=mythreshold,
                            interactive=0,
                            savemodel='none',
                            parallel=False,
                            calcres=False,
                            calcpsf=False,
                            smallscalebias=0.0,
                            restfreq='1.42040575177GHz',
                            )