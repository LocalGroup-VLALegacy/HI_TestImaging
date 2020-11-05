
'''
'Manual' imaging by just passing the full MSs directly to tclean.

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

vis_contsubs = {'D': os.path.join(datapath, 'M31_14A-235_HI_spw_0_LSRK.ms.contsub_M31_Field17'),
                'C': os.path.join(datapath, '15A-175_Ctracks_HI_spw_0_LSRK.ms_M31_Field17.contsub'),
                'B': os.path.join(datapath, '15A-175_Btracks_HI_spw_0_LSRK.ms_M31_Field17.contsub'),
                'A': os.path.join(datapath, '18A-467_HI_spw_0.ms.contsub')}

vis_nocontsubs = {'D': os.path.join(datapath, 'M31_14A-235_HI_spw_0_LSRK.ms_M31_Field17'),
                  'C': os.path.join(datapath, '15A-175_Ctracks_HI_spw_0_LSRK.ms_M31_Field17'),
                  'B': os.path.join(datapath, '15A-175_Btracks_HI_spw_0_LSRK.ms_M31_Field17'),
                  'A': os.path.join(datapath, '18A-467_HI_spw_0.ms')}

equivtime_scans = \
    {'A': "4,6,8,10,12,14",
     'C': "9,17,25,135,149,157,257,287,387,395,403,411,465,495,517,525",
     'B': "9,17,25,33,133,141,149,157,165,257,273,281,311,387,395,409",
     'D': "26,89,152,215,278,341,404,467,530,593,656,719,782,845,908"}

xltime_scans = \
    {'A': '4,6,8,10,12,14,16,18,19,21,23,25',
     'C': '9,17,25,33,41,49,57,65,135,149,157,165,173,187,195,257,265,287,295,303,317,387,395,403,411,449,465,479,495,503,517,525',
     'B': '9,17,25,33,41,49,63,71,79,133,141,149,157,165,173,187,195,203,211,257,265,273,281,295,303,311,333,387,395,409,417,433',
     'D': '26,89,152,215,278,341,404,467,530,593,656,719,782,845,908'}

run_dirtyimaging = True
run_shallowclean = False
run_deepclean = False

# Everything in one:

with_Aconfig = [True, False]

# with_contsub = [False, True]
with_contsub = [False]
weightings = ['natural', 'briggs']
# tapers = ['', '5arcsec']
tapers = ['']

for has_Aconfig in with_Aconfig:

    for contsub in with_contsub:

        if contsub is True:
            myvis = vis_contsubs
            image_str = 'contsub'
        else:
            myvis = vis_nocontsubs
            image_str = 'nocontsub'

        # Remove the last track from A config to compare w/ and w/o A tracks
        if has_Aconfig:
            confs = 'ABCD'
        else:
            confs = 'BCD'

        myvis = [myvis[config] for config in confs]
        # scan_select = [equivtime_scans[config] for config in confs]
        scan_select = [xltime_scans[config] for config in confs]


        for weight in weightings:

            for taper in tapers:

                print("On {0} {1} {2}\nIncludes A conf? {3}".format(weight, taper, image_str, has_Aconfig))

                imagename_run = os.path.join(datapath,
                                            'M31_Field17_{0}_{1}_{2}_{3}_xltimematched'
                                            .format(confs,
                                                    weight,
                                                    taper,
                                                    image_str))

                # Dirty map.
                if run_dirtyimaging:

                    out = tclean(vis=myvis,
                                field='M31*',
                                spw='0',
                                intent='',
                                datacolumn='corrected',
                                imagename=imagename_run,
                                imsize=2048,
                                cell='1arcsec',
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
