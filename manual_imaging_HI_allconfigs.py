
'''
'Manual' imaging by just passing the full MSs directly to tclean.

* All data w/ contsub
* All data w/o contsub
* Dirty maps
* Shallow clean (~5 sigma)
* Deeper/fully clean (~2 sigma)

Notes:

* with all data included, the beam is 8.3x7.3 arcsec with briggs robust=0.5 weighting
*

'''

from tasks import tclean

import os
from copy import copy

basepath = "/mnt/space/ekoch/VLA_tracks/"

datapath = os.path.join(basepath, '18A-467/HI_allconfig_imagingtests/')

vis_contsubs = [os.path.join(datapath, 'M31_14A-235_HI_spw_0_LSRK.ms.contsub_M31_Field17'),
                os.path.join(datapath, '15A-175_Ctracks_HI_spw_0_LSRK.ms_M31_Field17.contsub'),
                os.path.join(datapath, '15A-175_Btracks_HI_spw_0_LSRK.ms_M31_Field17.contsub'),
                os.path.join(datapath, '18A-467_HI_spw_0_LSRK.ms.contsub')]

vis_nocontsubs = [os.path.join(datapath, 'M31_14A-235_HI_spw_0_LSRK.ms_M31_Field17'),
                  os.path.join(datapath, '15A-175_Ctracks_HI_spw_0_LSRK.ms_M31_Field17'),
                  os.path.join(datapath, '15A-175_Btracks_HI_spw_0_LSRK.ms_M31_Field17'),
                  os.path.join(datapath, '18A-467_HI_spw_0_LSRK.ms')]

run_dirtyimaging = True
run_shallowclean = False
run_deepclean = False

# Everything in one:

with_Aconfig = [True, False]

with_contsub = [False, True]
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
            pass
        else:
            myvis = copy(myvis)[:-1]

        for weight in weightings:

            for taper in tapers:

                print("On {0} {1} {2}\nIncludes A conf? {3}".format(weight, taper, image_str, has_Aconfig))

                imagename_run = os.path.join(datapath,
                                            'M31_Field17_{0}_{1}_{2}_{3}'
                                            .format('ABCD' if with_Aconfig else 'BCD',
                                                    weight,
                                                    taper,
                                                    image_str))

                # Dirty map.
                if run_dirtyimaging:

                    tclean(vis=myvis,
                        field='M31*',
                        spw='0',
                        intent='',
                        datacolumn='corrected',
                        imagename=imagename_run,
                        imsize=4096,
                        cell='0.5arcsec',
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
