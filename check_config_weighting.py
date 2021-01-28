
'''
Check the relative weighting of each config following the VLA guide:
https://casaguides.nrao.edu/index.php?title=VLA_Data_Combination-CASA5.7.0


'''


import os

from tasks import plotms, statwt

basepath = "/mnt/space/ekoch/VLA_tracks/"

datapath = os.path.join(basepath, '18A-467/HI_allconfig_imagingtests/')

run_plotinitialweights = False
run_statwt = False
run_plotfinalweights = False
run_plotfinalweights_xltimematched = True
run_concat = False

vis_nocontsubs = {'D': os.path.join(datapath, 'M31_14A-235_HI_spw_0_LSRK.ms_M31_Field17'),
                  'C': os.path.join(datapath, '15A-175_Ctracks_HI_spw_0_LSRK.ms_M31_Field17'),
                  'B': os.path.join(datapath, '15A-175_Btracks_HI_spw_0_LSRK.ms_M31_Field17'),
                  'A': os.path.join(datapath, '18A-467_HI_spw_0_LSRK.ms')}

vis_contsubs = {'D': os.path.join(datapath, 'M31_14A-235_HI_spw_0_LSRK.ms.contsub_M31_Field17'),
                'C': os.path.join(datapath, '15A-175_Ctracks_HI_spw_0_LSRK.ms_M31_Field17.contsub'),
                'B': os.path.join(datapath, '15A-175_Btracks_HI_spw_0_LSRK.ms_M31_Field17.contsub'),
                'A': os.path.join(datapath, '18A-467_HI_spw_0_LSRK.ms.contsub')}

xltime_scans = \
{'A': [4, 6, 8, 10, 12, 14, 16, 18, 19, 21, 23, 25],
 'C': [9, 17, 25, 33, 41, 49, 57, 65, 135, 149, 157, 165, 173, 187, 195, 257, 265, 287, 295, 303, 317, 387, 395, 403, 411, 449, 465, 479, 495, 503, 517, 525],
 'B': [9, 17, 25, 33, 41, 49, 63, 71, 79, 133, 141, 149, 157, 165, 173, 187, 195, 203, 211, 257, 265, 273, 281, 295, 303, 311, 333, 387, 395, 409, 417, 433],
 'D': [26, 89, 152, 215, 278, 341, 404, 467, 530, 593, 656, 719, 782, 845, 908]}

vis_dicts = {'nocontsub': vis_nocontsubs,}
            #  'contsub': vis_contsubs}

for name in vis_dicts.keys():

    myvis = vis_dicts[name]

    if run_plotinitialweights:
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

        if run_statwt:
            print("Reweighting with statwt")

            statwt(myvis[config], datacolumn='DATA')

        if run_plotfinalweights:
            print("Plotting the new weights")

            plotms(vis=myvis[config],
                spw='0',
                averagedata=True,
                avgchannel='4096',
                avgtime='20',
                xaxis='uvwave', yaxis='wt', coloraxis='antenna1',
                title='{} config weights'.format(config),
                plotfile='{2}/{0}_{1}_weights_reweight_w_statwt_casa57.png'.format(config, name, datapath),
                expformat='png',
                showgui=False)

        if run_plotfinalweights_xltimematched:
            print("Plotting the new weights using only the time-matched scans")

            plotms(vis=myvis[config],
                spw='0',
                scan=",".join([str(x) for x in xltime_scans[config]]),
                averagedata=True,
                avgchannel='4096',
                avgtime='20',
                xaxis='uvwave', yaxis='wt', coloraxis='antenna1',
                title='{} config weights'.format(config),
                plotfile='{2}/{0}_{1}_weights_reweight_w_statwt_xltimematch.png'.format(config, name, datapath),
                expformat='png',
                showgui=False)

            plotms(vis=myvis[config],
                spw='0',
                scan=",".join([str(x) for x in xltime_scans[config]]),
                averagedata=True,
                avgchannel='4096',
                avgtime='20',
                xaxis='uvwave', yaxis='wt', coloraxis='observation',
                title='{} config weights'.format(config),
                plotfile='{2}/{0}_{1}_weights_reweight_w_statwt_xltimematch_obscolour.png'.format(config, name, datapath),
                expformat='png',
                showgui=False)


    # Concat all tracks into single MSs. This is especially due to the changin
    # beam size with imagesize/cellsize in tclean when using multiple MSs

    if run_concat:
        if name == 'nocontsub':
            concat_name = 'M31_Field17_HI_ABCD.ms'
        else:
            concat_name = 'M31_Field17_HI_ABCD.ms.contsub'

        concat(concatvis=os.path.join(datapath, concat_name),
            vis=[myvis[config] for config in "ABCD"],
            timesort=True,
            respectname=True)
