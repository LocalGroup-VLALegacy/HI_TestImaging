
'''
Find the time on source for all tracks covering M31LARGE_17 (or M31_Field17)
pointing.
'''

import os
from copy import copy

import analysisUtils as au

basepath = "/mnt/space/ekoch/VLA_tracks/"

datapath = os.path.join(basepath, '18A-467/HI_allconfig_imagingtests/')


vis_nocontsubs = {'D': os.path.join(datapath, 'M31_14A-235_HI_spw_0_LSRK.ms_M31_Field17'),
                  'C': os.path.join(datapath, '15A-175_Ctracks_HI_spw_0_LSRK.ms_M31_Field17'),
                  'B': os.path.join(datapath, '15A-175_Btracks_HI_spw_0_LSRK.ms_M31_Field17'),
                  'A': os.path.join(datapath, '18A-467_HI_spw_0.ms')}

time_on_source = dict.fromkeys(['D', 'C', 'B', 'A'])

for config in vis_nocontsubs:

    out = au.timeOnSource(vis_nocontsubs[config])

    time_on_source[config] = out[0]['minutes_on_source']

print(time_on_source)
# {'A': 386.16666671435036, 'C': 164.25, 'B': 142.64999993642172, 'D': 46.25}

ratios = [time_on_source[config] / time_on_source['D'] for config in "ABCD"]

print(ratios)
# [8.3495495505805479, 3.0843243229496586, 3.5513513513513515, 1.0]

# If we were using the full 3:1 for successive configs:
# 27:9:3:1

# NOTE: We have way more A config than the other configs, as expected.
# C-D: about the rule of thumb 3:1
# B-C: about 1:1
# A-B: about the rule of thumb 3:1

# Now compute which scans should be selected to reach 1:1:1:1
# I'm just going to go from the start to end in the tracks and will
# explore different combinations if there's an issue with those scans
# (for whatever reason, should be fine, though)

def accumulate_to(scantime_dict, target=time_on_source['D']):
    '''
    Return the first N scans that match the target integration time.
    '''

    total = 0.
    scans = []

    for scan in scantime_dict:
        total += scantime_dict[scan]

        scans.append(scan)

        if total >= target:
            break

    return scans

equivtime_scans = dict.fromkeys(['D', 'C', 'B', 'A'])

for config in vis_nocontsubs:

    out = au.timeOnSource(vis_nocontsubs[config])

    equivtime_scans[config] = accumulate_to(out['minutes_on_science_per_scan'])

    # If this is D config, this should be ALL the scans. Do sanity check:
    if config == 'D':
        assert equivtime_scans['D'] == list(out['minutes_on_science_per_scan'].keys())

# For reference
print(equivtime_scans)
# {'A': [4, 6, 8, 10, 12, 14],
# 'C': [257, 387, 517, 135, 9, 395, 525, 17, 465, 403, 149, 495, 25, 411, 157, 287],
# 'B': [409, 257, 387, 133, 311, 9, 395, 273, 141, 17, 149, 281, 25, 157, 33, 165],
# 'D': [908, 845, 782, 719, 656, 593, 530, 467, 404, 341, 278, 215, 152, 89, 26]}

# NOTE: these are NOT necessarily in time order. But that might actually be better?
# Better uv-coverage if taking scans from different tracks?
