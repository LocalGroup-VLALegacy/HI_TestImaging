
'''
Find the time on source for all tracks covering M31LARGE_17 (or M31_Field17)
pointing.

The final time on source for the whole project will be:

A: 180, B: 180, C: 180, D: 90

With the times below, the "time-matched" version gives:
A: 90, B: 90, C: 90, D: 45
Effectively, this is half the depth. However, the mosaic will provide ~2
improvement for each point within the inner parts of the mosaic.
**So these archival data are closer to 25% of the depth.**

Using all the time available, we have:
A: 380, B: 142, C: 165, D: 46

'''

import os

import random
random.seed(42)

import analysisUtils as au

basepath = "/mnt/space/ekoch/VLA_tracks/"

datapath = os.path.join(basepath, '18A-467/HI_allconfig_imagingtests/')


vis_nocontsubs = {'D': os.path.join(datapath, 'M31_14A-235_HI_spw_0_LSRK.ms_M31_Field17'),
                  'C': os.path.join(datapath, '15A-175_Ctracks_HI_spw_0_LSRK.ms_M31_Field17'),
                  'B': os.path.join(datapath, '15A-175_Btracks_HI_spw_0_LSRK.ms_M31_Field17'),
                  'A': os.path.join(datapath, '18A-467_HI_spw_0_LSRK.ms')}

time_on_source = dict.fromkeys(['D', 'C', 'B', 'A'])

for config in vis_nocontsubs:

    out = au.timeOnSource(vis_nocontsubs[config])

    time_on_source[config] = out[0]['minutes_on_source']

print(time_on_source)
# {'A': 386.16666671435036, 'C': 164.25, 'B': 142.64999993642172, 'D': 46.25}

ratios = [time_on_source[config] / time_on_source['D'] for config in "ABCD"]

# This is the full XL setup, with half the time in D compared to the rest
ratios_full = [time_on_source[config] / (0.5 * time_on_source['D']) for config in "ABCD"]

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

def accumulate_to(scantime_dict, target=time_on_source['D'],
                  reorder_scans=True):
    '''
    Return the first N scans that match the target integration time.
    '''

    total = 0.
    scans = []

    scan_nums = list(scantime_dict.keys())

    if reorder_scans:
        random.shuffle(scan_nums)

    for scan in scan_nums:
        total += scantime_dict[scan]

        scans.append(scan)

        if total >= target:
            break

    return scans

equivtime_scans = dict.fromkeys(['D', 'C', 'B', 'A'])
xltime_scans = dict.fromkeys(['D', 'C', 'B', 'A'])

for config in vis_nocontsubs:

    out = au.timeOnSource(vis_nocontsubs[config])

    equivtime_scans[config] = accumulate_to(out['minutes_on_science_per_scan'])

    xltime_scans[config] = accumulate_to(out['minutes_on_science_per_scan'],
                                         target=time_on_source['D'] * 2.)


    # If this is D config, this should be ALL the scans. Do sanity check:
    if config == 'D':
        assert all([scan in equivtime_scans['D'] for scan in list(out['minutes_on_science_per_scan'].keys())])

    equivtime_scans[config].sort()
    xltime_scans[config].sort()

# For reference
print(equivtime_scans)
# {'A': [4, 6, 8, 10, 12, 14],
# 'C': [9, 17, 25, 135, 149, 157, 257, 287, 387, 395, 403, 411, 465, 495, 517, 525],
# 'B': [9, 17, 25, 33, 133, 141, 149, 157, 165, 257, 273, 281, 311, 387, 395, 409],
# 'D': [26, 89, 152, 215, 278, 341, 404, 467, 530, 593, 656, 719, 782, 845, 908]}

# NOTE: these are NOT necessarily in time order. But that might actually be better?
# Better uv-coverage if taking scans from different tracks?

print(xltime_scans)
# {'A': [4, 6, 8, 10, 12, 14, 16, 18, 19, 21, 23, 25],
# 'C': [9, 17, 25, 33, 41, 49, 57, 65, 135, 149, 157, 165, 173, 187, 195, 257, 265, 287, 295, 303, 317, 387, 395, 403, 411, 449, 465, 479, 495, 503, 517, 525],
# 'B': [9, 17, 25, 33, 41, 49, 63, 71, 79, 133, 141, 149, 157, 165, 173, 187, 195, 203, 211, 257, 265, 273, 281, 295, 303, 311, 333, 387, 395, 409, 417, 433],
# 'D': [26, 89, 152, 215, 278, 341, 404, 467, 530, 593, 656, 719, 782, 845, 908]}

# With a random order used to choose the scans in each config.
print(xltime_scans)
# {'A': [6, 8, 23, 27, 31, 63, 74, 81, 83, 85, 87, 91],
# 'C': [9, 17, 33, 41, 49, 57, 95, 103, 119, 127, 157, 165, 195, 211, 225, 257, 265, 287, 295, 303, 317, 325, 341, 349, 387, 403, 411, 441, 457, 479, 487, 517, 541],
# 'B': [9, 25, 33, 41, 49, 63, 79, 87, 103, 141, 149, 157, 173, 187, 195, 203, 211, 219, 249, 257, 273, 295, 303, 311, 319, 333, 357, 379, 387, 417, 425, 433],
# 'D': [26, 89, 152, 215, 278, 341, 404, 467, 530, 593, 656, 719, 782, 845, 908]}

# We also want the mapping for the concatented MS.
# Here, we account for the different configs by SPW, since each has a slight
# offset in SPW and they're not transformed to match.

concat_vis = os.path.join(datapath, 'M31_Field17_HI_ABCD.ms')

config_to_spwmapping = {'D': 0, 'C': 1, 'B': 2, 'A': 3}

config_scans = dict.fromkeys(['D', 'C', 'B', 'A'])

msmd.open(concat_vis)

for config in config_to_spwmapping:

    config_scans[config] = msmd.scansforspw(spw=config_to_spwmapping[config])

msmd.close()

scan_time_dict = au.timeOnSource(concat_vis, field='0')['minutes_on_science_per_scan']
scan_time_dict.update(au.timeOnSource(concat_vis, field='1')['minutes_on_science_per_scan'])

xltime_scans_concat = dict.fromkeys(['D', 'C', 'B', 'A'])

for config in config_scans:

    this_config_scan_times = {scan: scan_time_dict[scan] for scan in config_scans[config]}

    print(config, this_config_scan_times.keys())

    xltime_scans_concat[config] = accumulate_to(this_config_scan_times,
                                                target=time_on_source['D'] * 2.)

print(xltime_scans_concat)

# With a random scan order
# {'A': [1884, 1894, 1948, 1922, 1890, 1939, 1952, 1871, 1903, 1896, 1916, 1926],
#  'C': [1219, 1181, 1041, 1127, 1149, 1095, 1333, 1203, 1271, 979, 1249, 1287, 1233, 987, 963, 1211, 949, 1017, 1157, 1033, 971, 1165, 1049, 1295, 1279, 1103, 995, 1003, 925, 1309, 1025, 1141],
#  'B': [1390, 1566, 1704, 1512, 1728, 1590, 1350, 1474, 1520, 1766, 1482, 1674, 1812, 1850, 1558, 1750, 1642, 1774, 1628, 1650, 1658, 1666, 1866, 1574, 1404, 1582, 1498, 1550, 1682, 1444, 1620, 1374, 1452],
#  'D': [719, 782, 26, 404, 593, 845, 467, 152, 530, 89, 215, 278, 341, 656, 908]}