
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

a_tracks = glob(os.path.join(output_path, "M31_A_*"))
b_tracks = glob(os.path.join(output_path, "M31_B_*"))
c_tracks = glob(os.path.join(output_path, "M31_C_*"))

bc_tracks = b_tracks + c_tracks

concat(concatvis=os.path.join(output_path, 'M31_20A-346_BC_HI.ms.contsub.regrid2kms'),
       vis=bc_tracks,
       timesort=False)