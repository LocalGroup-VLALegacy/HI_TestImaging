
'''
Check the relative weighting of each config following the VLA guide:
https://casaguides.nrao.edu/index.php?title=VLA_Data_Combination-CASA5.7.0


'''


import os
from copy import copy

from tasks import plotms, statwt

basepath = "/mnt/space/ekoch/VLA_tracks/"

datapath = os.path.join(basepath, '18A-467/HI_allconfig_imagingtests/')


vis_nocontsubs = {'D': os.path.join(datapath, 'M31_14A-235_HI_spw_0_LSRK.ms_M31_Field17'),
                  'C': os.path.join(datapath, '15A-175_Ctracks_HI_spw_0_LSRK.ms_M31_Field17'),
                  'B': os.path.join(datapath, '15A-175_Btracks_HI_spw_0_LSRK.ms_M31_Field17'),
                  'A': os.path.join(datapath, '18A-467_HI_spw_0_LSRK.ms')}

vis_contsubs = {'D': os.path.join(datapath, 'M31_14A-235_HI_spw_0_LSRK.ms.contsub_M31_Field17'),
                'C': os.path.join(datapath, '15A-175_Ctracks_HI_spw_0_LSRK.ms_M31_Field17.contsub'),
                'B': os.path.join(datapath, '15A-175_Btracks_HI_spw_0_LSRK.ms_M31_Field17.contsub'),
                'A': os.path.join(datapath, '18A-467_HI_spw_0_LSRK.ms.contsub')}

vis_dicts = {#'nocontsub': vis_nocontsubs,
             'contsub': vis_contsubs}

for name in vis_dicts.keys():

    myvis = vis_dicts[name]

    for config in myvis:

        print("On config {}".format(config))

        plotms(vis=myvis[config],
            spw='0',
            averagedata=True,
            avgchannel='4096',
            avgtime='20',
            xaxis='uvwave', yaxis='wt', coloraxis='antenna1',
            title='{} config weights'.format(config),
            plotfile='{2}/{0}_{1}_weights.png'.format(config, name, datapath),
            expformat='png',
            showgui=False)

    # This shows that the A is ridiculously downweighted compared to the others
    # A has a typical weight of ~2, while the other configs are ~700,000 or 1.2e6...

    # Now try to re-run statwt on each. We're just going to try this on the original versions
    # since these weightings are already so discrepant.
    # Each can be reproduced by re-running split_HI_allconfigs


    for config in myvis:

        print("On config {}".format(config))

        print("Reweighting with statwt")

        statwt(myvis[config], datacolumn='DATA')

        print("Plotting the new weights")

        plotms(vis=myvis[config],
            spw='0',
            averagedata=True,
            avgchannel='4096',
            avgtime='20',
            xaxis='uvwave', yaxis='wt', coloraxis='antenna1',
            title='{} config weights'.format(config),
            plotfile='{2}/{0}_{1}_weights_reweight_w_statwt.png'.format(config, name, datapath),
            expformat='png',
            showgui=False)


    # Concat all tracks into single MSs. This is especially due to the changin
    # beam size with imagesize/cellsize in tclean when using multiple MSs

    if name == 'nocontsub':
        concat_name = 'M31_Field17_HI_ABCD.ms'
    else:
        concat_name = 'M31_Field17_HI_ABCD.ms.contsub'

    concat(concatvis=os.path.join(datapath, concat_name),
        vis=[myvis[config] for config in "ABCD"],
        timesort=True,
        respectname=True)
