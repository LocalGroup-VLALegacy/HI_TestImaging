
'''
The whole thing with the new 20A data and D-config from 14A-235.

'''

from tasks import tclean

from cleanhelper import cleanhelper as clp

import os
from copy import copy

basepath = "/mnt/space/ekoch/VLA_tracks/"

datapath = os.path.join(basepath, '20A-346/HI_ms/')
imagepath = os.path.join(datapath, 'BCD_testimaging')

if not os.path.exists(imagepath):
    os.mkdir(imagepath)

vis_contsub = os.path.join(datapath, 'M31_20A_14A_BCD_HI.ms.contsub.regrid2kms')

run_dirtyimaging = False
run_shallowclean = False
run_deepclean = True
run_restoreonly = False

# Everything in one:

# with_contsub = [False, True]
with_contsub = [True]

# matched_time = [False, True]
matched_time = [True]


def vel_to_channel(target_vel, zero_vel=30., chan=-2.):
        return int((target_vel - zero_vel) / chan)

nchan = 1

startvel = -180
startchan = vel_to_channel(startvel)

imaging_setups = [{'weight': 'briggs', 'robust': 1., 'taper': "", 'cell': '2.0arcsec'},
                #   {'weight': 'briggs', 'robust': 0., 'taper': "", 'cell': '0.4arcsec'},
                #   {'weight': 'briggs', 'robust': -1., 'taper': "", 'cell': '0.3arcsec'},
                #   {'weight': 'natural', 'robust': 0., 'taper': "", 'cell': '1.8arcsec'},
                #   {'weight': 'briggs', 'robust': 1., 'taper': "5arcsec", 'cell': '2.2arcsec'},
                #   {'weight': 'briggs', 'robust': 1., 'taper': "10arcsec", 'cell': '3.7arcsec'},
                #   {'weight': 'briggs', 'robust': 1., 'taper': "20arcsec", 'cell': '6.2arcsec'},
                #   {'weight': 'briggs', 'robust': 1., 'taper': "30arcsec", 'cell': '8.6arcsec'},
                  ]

# Set a constant angular size for the image.
ang_size = 5. # deg
# myimsize = [13500, 15000]

# Using all configs here
confs = 'BCD'

# mycleanmask = 'M31_Field17_ABCD_cleanmask_from_15A.mask'
mycleanmask = ''

mypblimit = 0.1

scan_select = ''

myvis = vis_contsub

niter_shallow = 5000
niter_deep = 15000

cycleniter_shallow = 500
cycleniter_deep = 1500

for i, setup_dict in enumerate(imaging_setups):

    print("On image test {0}/{1}".format(i + 1, len(imaging_setups)))

    for time_match in matched_time:

        for contsub in with_contsub:

            myweight = setup_dict['weight']
            myrobust = setup_dict['robust']
            mytaper = setup_dict['taper']
            mycell = setup_dict['cell']

            mycell_float = float(mycell.split('arcsec')[0])

            myimsize = clp.getOptimumSize(int(ang_size * 3600. / mycell_float))

            print("On image size {0} with cell {1}".format(myimsize, mycell))

            imagename_run = os.path.join(imagepath,
                                        'M31_BCD_20A_14A_{0}_{1}_robust{2}_taper_{3}_cell_{4}'
                                        .format(confs,
                                                myweight,
                                                myrobust,
                                                mytaper if len(mytaper) > 0 else "none",
                                                mycell))

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
                            phasecenter="J2000 00h42m44.350 +41d16m08.63",
                            nchan=nchan,
                            start=startchan,
                            width=1,
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
                            # fastnoise=False,
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
                            phasecenter="J2000 00h42m44.350 +41d16m08.63",
                            nchan=nchan,
                            start=startchan,
                            width=1,
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
                            niter=niter_shallow,
                            cycleniter=cycleniter_shallow,  # Force many major cycles
                            nsigma=2.,
                            usemask='auto-multithresh',
                            # mask=mycleanmask,
                            mask='',
                            sidelobethreshold=1.0,
                            noisethreshold=3.0,
                            lownoisethreshold=1.5,
                            negativethreshold=0.0,
                            minbeamfrac=0.1,
                            growiterations=75,
                            dogrowprune=True,
                            minpercentchange=1.0,
                            # fastnoise=False,
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
                # Delete the existing image
                os.system("rm -rf {0}.image".format(imagename_run))

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
                            phasecenter="J2000 00h42m44.350 +41d16m08.63",
                            nchan=nchan,
                            start=startchan,
                            width=1,
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
                            niter=niter_deep,
                            cycleniter=cycleniter_deep,  # Force many major cycles
                            nsigma=2.,
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
                            # fastnoise=False,
                            threshold=mythreshold,
                            interactive=0,
                            savemodel='none',
                            parallel=False,
                            calcres=False,
                            calcpsf=False,
                            smallscalebias=0.0,
                            restfreq='1.42040575177GHz',
                            )

            impbcor(imagename="{0}.image".format(imagename_run),
                    pbimage="{0}.pb".format(imagename_run),
                    outfile="{0}.image.pbcor".format(imagename_run))

            # Restore only.
            if run_restoreonly:

                out = tclean(vis=myvis,
                            field='M31*',
                            spw='',
                            intent='',
                            datacolumn='corrected',
                            imagename=imagename_run,
                            imsize=myimsize,
                            cell=mycell,
                            scan=scan_select,
                            phasecenter="J2000 00h42m44.350 +41d16m08.63",
                            nchan=nchan,
                            start=startchan,
                            width=1,
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
                            # fastnoise=False,
                            threshold='',
                            interactive=0,
                            savemodel='none',
                            parallel=False,
                            calcres=False,
                            calcpsf=False,
                            smallscalebias=0.0,
                            restfreq='1.42040575177GHz',
                            )

            impbcor(imagename="{0}.image".format(imagename_run),
                    pbimage="{0}.pb".format(imagename_run),
                    outfile="{0}.image.pbcor".format(imagename_run))
