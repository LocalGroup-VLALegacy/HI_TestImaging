
'''
These MSs are only HI and have already have continuum subtraction
and regridding to the same spectral config (-700 to 30 km/s, 2 km/s channels).

The exception is the 14A D-config data. These will be regridded to match
the 20A data.
'''


import os
from glob import glob

# from tasks import split, concat, uvcontsub, mstransform

basepath = "/mnt/space/ekoch/VLA_tracks/"

fourteenA_path = os.path.join(basepath, '14A-235/products/')
fifteenA_path = os.path.join(basepath, '15A-175/products/HI/')
# eighteenA_path = os.path.join(basepath, '18A-467/calibrated/')

output_path = os.path.join(basepath, '20A-346/HI_ms')

a_tracks = glob(os.path.join(output_path, "M31_A_*.regrid2kms"))
b_tracks = glob(os.path.join(output_path, "M31_B_*.regrid2kms"))
c_tracks = glob(os.path.join(output_path, "M31_C_*.regrid2kms"))

bc_tracks = b_tracks + c_tracks

outconcatvis =os.path.join(output_path, 'M31_20A-346_BC_HI.ms.contsub.regrid2kms_LSRK.withflagging')

if not os.path.exists(outconcatvis):

    outconcatvis_temp =os.path.join(output_path, 'M31_20A-346_BC_HI.ms.contsub.regrid2kms.withflagging')

    concat(concatvis=outconcatvis,
           vis=bc_tracks,
           timesort=False)

    mstransform(vis=outconcatvis_temp,
                outputvis=outconcatvis,
                regridms=True, outframe='LSRK',
                datacolumn='data')

    rmtables(outconcatvis_temp)

# Make a separate directory for all of the 7-pt splits
hexsplit_dir = os.path.join(output_path, 'hexsplit_ms')

if not os.path.exists(hexsplit_dir):
    os.mkdir(hexsplit_dir)

# Next, split out the 7-pt A pointing coverage from the B and C tracks:
for track in bc_tracks:

    outvis = "{0}/{1}_7pthex".format(hexsplit_dir,
                                     os.path.split(track)[1])
    if os.path.exists(outvis):
        casalog.post("{} exists. Skipping split".format(outvis))

    split(vis=track,
          outputvis=outvis,
          datacolumn='data',
          field='M31LARGE_5,M31LARGE_16,M31LARGE_17,M31LARGE_18,M31LARGE_30,M31LARGE_31,M31LARGE_32')

bctrack_splits = glob(os.path.join(hexsplit_dir, "*_7pthex"))

# Concat all of the 20A 7-pt hex data together.
outconcatvis_hex =os.path.join(output_path, 'M31_20A-346_ABC_hex_HI.ms.contsub.regrid2kms_LSRK.withflagging')

if not os.path.exists(outconcatvis_hex):
    outconcatvis_hex_temp =os.path.join(output_path, 'M31_20A-346_ABC_hex_HI.ms.contsub.regrid2kms.withflagging')

    concat(concatvis=outconcatvis_hex,
           vis=bc_tracks,
           timesort=False)

    mstransform(vis=outconcatvis_hex_temp,
                outputvis=outconcatvis_hex,
                regridms=True, outframe='LSRK',
                datacolumn='data')

    rmtables(outconcatvis_hex_temp)

# Now include the 14A and 15A data.

fourteenA_path = os.path.join(basepath, '14A-235/products/')
fifteenA_path = os.path.join(basepath, '15A-175/products/HI/')
eighteenA_path = os.path.join(basepath, '18A-467/calibrated/')


# First, regrid to match the 2 km/s channels with the rest of the 20A data

regrid_14A_ms = os.path.join(output_path,
                             'M31_14A-235_HI_spw_0_LSRK.ms.contsub.regrid2kms')

if not os.path.exists(regrid_14A_ms):

    mstransform(vis=os.path.join(fourteenA_path, 'M31_14A-235_HI_spw_0_LSRK.ms.contsub'),
                outputvis=regrid_14A_ms,
                regridms=True,
                mode='velocity', start='-700km/s', width='2.0km/s', nchan=366,
                restfreq='1.42040575177GHz', veltype='radio', timebin='20s',
                datacolumn='data')

    statwt(vis=regrid_14A_ms, datacolumn='data')

# Make the full mosaic BCD concat MS:

outconcatvis_BCD_full =os.path.join(output_path, 'M31_20A_14A_BCD_HI.ms.contsub.regrid2kms')

if not os.path.exists(outconcatvis_BCD_full):

    concat(concatvis=outconcatvis_BCD_full,
           vis=[outconcatvis, regrid_14A_ms],
           timesort=False)


# We already have a 14A split version in the 15A track folder. Regrid this one, too.
regrid_14A_hex_ms = os.path.join(output_path,
                                 'M31_14A-235_15Afields_HI_spw_0_LSRK.ms.contsub.regrid2kms')

if not os.path.exists(regrid_14A_hex_ms):

    mstransform(vis=os.path.join(fifteenA_path, 'M31_14A-235_15Afields_HI_spw_0_LSRK.ms.contsub'),
                outputvis=regrid_14A_hex_ms,
                regridms=True,
                mode='velocity', start='-700km/s', width='2.0km/s', nchan=366,
                restfreq='1.42040575177GHz', veltype='radio', timebin='20s',
                datacolumn='data')

    statwt(vis=regrid_14A_hex_ms, datacolumn='data')


regrid_15A_B_ms = os.path.join(output_path,
                               '15A-175_Btracks_HI_spw_0_LSRK.ms.contsub.regrid2kms')

if not os.path.exists(regrid_15A_B_ms):

    mstransform(vis=os.path.join(fifteenA_path, '15A-175_Btracks_HI_spw_0_LSRK.ms.contsub'),
                outputvis=regrid_15A_B_ms,
                regridms=True,
                mode='velocity', start='-700km/s', width='2.0km/s', nchan=366,
                restfreq='1.42040575177GHz', veltype='radio', timebin='20s',
                datacolumn='data')

    statwt(vis=regrid_15A_B_ms, datacolumn='data')

regrid_15A_C_ms = os.path.join(output_path,
                               '15A-175_Ctracks_HI_spw_0_LSRK.ms.contsub.regrid2kms')

if not os.path.exists(regrid_15A_C_ms):

    mstransform(vis=os.path.join(fifteenA_path, '15A-175_Ctracks_HI_spw_0_LSRK.ms.contsub'),
                outputvis=regrid_15A_C_ms,
                regridms=True,
                mode='velocity', start='-700km/s', width='2.0km/s', nchan=366,
                restfreq='1.42040575177GHz', veltype='radio', timebin='20s',
                datacolumn='data')

    statwt(vis=regrid_15A_C_ms, datacolumn='data')

# Make concatenated 7-pt hex MSs with all data.

outconcatvis_hex_all =os.path.join(output_path, 'M31_20A_15A_14A_ABCD_hex_HI.ms.contsub.regrid2kms')

if not os.path.exists(outconcatvis_hex):
    concat(concatvis=outconcatvis_hex,
        vis=[outconcatvis_hex, regrid_14A_hex_ms, regrid_15A_B_ms, regrid_15A_C_ms],
        timesort=False)
