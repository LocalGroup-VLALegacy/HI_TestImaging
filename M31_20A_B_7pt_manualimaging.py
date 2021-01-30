
'''
Cover the northern hex mosaic with 15A-175 and 20A-346 with ONLY tracks
taken in B-config.

This is our test for recovering down to thermal noise at only B config.

'''

from tasks import tclean, split

from cleanhelper import cleanhelper as clp

import os
from copy import copy

basepath = "/mnt/space/ekoch/VLA_tracks/"

output_path = os.path.join(basepath, '20A-346/HI_ms')

full_visname =os.path.join(output_path,
                           'M31_20A_15A_14A_ABCD_hex_HI.ms.contsub.regrid2kms')

visname =os.path.join(output_path,
                      'M31_20A_15A_B_hex_HI.ms.contsub.regrid2kms')

# Split out the B config data, only
if not os.path.exists(visname):

    myobs_bconfig = '15~23,42~47'

    split(vis=full_visname,
          outputvis=visname,
          observation=myobs_bconfig,
          datacolumn='DATA')


imagepath = os.path.join(output_path, 'B_7pthex_imaging')

if not os.path.exists(imagepath):
    os.mkdir(imagepath)

run_dirtyimaging = False
run_shallowclean = True
run_deepclean = False

# Everything in one:

# matched_time = [False, True]
matched_time = [False]

random_scan_order = True

def vel_to_channel(target_vel, zero_vel=30., chan=-2.):
        return int((target_vel - zero_vel) / chan)

nchan = 1

startvel = -180
startchan = vel_to_channel(startvel)

myphasecenter = 'J2000 00:44:33.854 +41d57m42.572'

imaging_setups = [{'weight': 'briggs', 'robust': 1., 'taper': "", 'cell': '1.0arcsec'},
                #   {'weight': 'briggs', 'robust': 0., 'taper': "", 'cell': '0.4arcsec'},
                #   {'weight': 'briggs', 'robust': -1., 'taper': "", 'cell': '0.3arcsec'},
                #   {'weight': 'natural', 'robust': 0., 'taper': "", 'cell': '1.8arcsec'},
                #   {'weight': 'briggs', 'robust': 1., 'taper': "5arcsec", 'cell': '2.2arcsec'},
                #   {'weight': 'briggs', 'robust': 1., 'taper': "10arcsec", 'cell': '3.7arcsec'},
                #   {'weight': 'briggs', 'robust': 1., 'taper': "20arcsec", 'cell': '6.2arcsec'},
                #   {'weight': 'briggs', 'robust': 1., 'taper': "30arcsec", 'cell': '8.6arcsec'},
                  ]

# Set a constant angular size for the image.
ang_size = 2. # deg

# Using all configs here
confs = 'B'

mycleanmask = ''
# mycleanmask = 'M31_Field17_ABCD_cleanmask_from_15A.mask'

mypblimit = 0.1

niter_shallow = 5000
niter_deep = 50000

for i, setup_dict in enumerate(imaging_setups):

    print("On image test {0}/{1}".format(i + 1, len(imaging_setups)))

    for time_match in matched_time:

        # myvis = "{0}_channel_{1}".format(visname, startchan)
        myvis = visname

        if time_match:
            if random_scan_order:
                scan_select = ",".join([xltime_scans_random[config] for config in confs])
            else:
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

        if time_match:
            time_string = "xltimematched"
            if random_scan_order:
                time_string += "_randomorder"
        else:
            time_string = "allscans"

        imagename_run = os.path.join(imagepath,
                                    'M31_B_7pthex_{0}_{1}_robust{2}_taper_{3}_cell_{4}_channel_{5}'
                                    .format(confs,
                                            myweight,
                                            myrobust,
                                            mytaper if len(mytaper) > 0 else "none",
                                            mycell,
                                            startchan))

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
                        phasecenter=myphasecenter,  # Only one field
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
                        # perchanweightdensity=False,
                        )

        # Shallow clean with clean mask.
        if run_shallowclean:

            # Make copies of the dirty image
            os.system("cp -r {0}.image {0}.image_dirty".format(imagename_run))

            # Delete the existing mask
            os.system("rm -rf {0}.mask".format(imagename_run))
            # Delete the existing image
            os.system("rm -rf {0}.image".format(imagename_run))

            mythreshold = ''

            out = tclean(vis=myvis,
                        field='M31*',
                        spw='',
                        intent='',
                        datacolumn='corrected',
                        imagename=imagename_run,
                        imsize=myimsize,
                        cell=mycell,
                        scan=scan_select,
                        phasecenter=myphasecenter,  # Only one field
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
                        cycleniter=500,  # Force many major cycles
                        nsigma=2.,
                        usemask='auto-multithresh',
                        # usemask='user',
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
                        # perchanweightdensity=False,
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

            mythreshold = ''

            out = tclean(vis=myvis,
                        field='M31*',
                        spw='',
                        intent='',
                        datacolumn='corrected',
                        imagename=imagename_run,
                        imsize=myimsize,
                        cell=mycell,
                        scan=scan_select,
                        phasecenter=myphasecenter,  # Only one field
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
                        cycleniter=1000,  # Force many major cycles
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
                        # perchanweightdensity=False,
                        )

            impbcor(imagename="{0}.image".format(imagename_run),
                    pbimage="{0}.pb".format(imagename_run),
                    outfile="{0}.image.pbcor".format(imagename_run))
