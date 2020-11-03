
'''
Split out this field from the B, C, D tracks, which are already HI splits.

Split out science and HI SPW for A tracks.

'''

import os
from glob import glob

from tasks import split, concat, uvcontsub

fieldname = 'M31LARGE_17'
fieldname_18A = 'M31_Field17'

basepath = "/mnt/space/ekoch/VLA_tracks/"

fourteenA_path = os.path.join(basepath, '14A-235/products/')
fifteenA_path = os.path.join(basepath, '15A-175/products/HI/')
eighteenA_path = os.path.join(basepath, '18A-467/calibrated/')

output_path = os.path.join(basepath, '18A-467/HI_allconfig_imagingtests/')

# Split out field M31_Field17

# D
split(vis=os.path.join(fourteenA_path, 'M31_14A-235_HI_spw_0_LSRK.ms.contsub'),
      outputvis=os.path.join(output_path, 'M31_14A-235_HI_spw_0_LSRK.ms.contsub_M31_Field17'),
      field=fieldname,
      datacolumn='DATA')

split(vis=os.path.join(fourteenA_path, 'M31_14A-235_HI_spw_0_LSRK.ms'),
      outputvis=os.path.join(output_path, 'M31_14A-235_HI_spw_0_LSRK.ms_M31_Field17'),
      field=fieldname,
      datacolumn='DATA')

# C
split(vis=os.path.join(fifteenA_path, '15A-175_Ctracks_HI_spw_0_LSRK.ms'),
      outputvis=os.path.join(output_path, '15A-175_Ctracks_HI_spw_0_LSRK.ms_M31_Field17'),
      field=fieldname,
      datacolumn='DATA')

uvcontsub(vis=os.path.join(output_path, '15A-175_Ctracks_HI_spw_0_LSRK.ms_M31_Field17'),
          fitorder=0,
          fitspw="0:205~1075;2805~3750")


# B
split(vis=os.path.join(fifteenA_path, '15A-175_Btracks_HI_spw_0_LSRK.ms'),
      outputvis=os.path.join(output_path, '15A-175_Btracks_HI_spw_0_LSRK.ms_M31_Field17'),
      field=fieldname,
      datacolumn='DATA')

uvcontsub(vis=os.path.join(output_path, '15A-175_Btracks_HI_spw_0_LSRK.ms_M31_Field17'),
          fitorder=0,
          fitspw="0:205~1075;2805~3750")

# A

# Split out HI.

if not os.path.exists(os.path.join(basepath, '18A-467/products/')):
    os.mkdir(os.path.join(basepath, '18A-467/products/'))
if not os.path.exists(os.path.join(basepath, '18A-467/products/HI/')):
    os.mkdir(os.path.join(basepath, '18A-467/products/HI/'))

output_names = []

for i, track in enumerate(glob(os.path.join(eighteenA_path, '*.ms'))):

    print("On {0} {1}".format(i, track))

    output_msname = os.path.join(basepath, '18A-467/products/HI/',
                                 track.split("/")[-1] + "_HI")

    split(vis=track,
          outputvis=output_msname,
          spw='0',
          field=fieldname_18A,
          datacolumn='CORRECTED',
          keepflags=False)

    output_names.append(output_msname)


concat(concatvis=os.path.join(basepath, '18A-467/products/HI/', '18A-467_HI_spw_0.ms'),
       vis=output_names,
       timesort=True)

# Continuum subtraction
# Doing this for now without masking out channels that should have signal
# This is because the time interval is `int` and the HI is not bright enough to really matter
uvcontsub(vis=os.path.join(basepath, '18A-467/products/HI/', '18A-467_HI_spw_0.ms'),
          fitorder=0)

os.system("cp -r {0} {1}".format(os.path.join(basepath, '18A-467/products/HI/', '18A-467_HI_spw_0.ms')),
                                 os.path.join(output_path, '18A-467_HI_spw_0.ms'))
os.system("cp -r {0} {1}".format(os.path.join(basepath, '18A-467/products/HI/', '18A-467_HI_spw_0.ms.contsub')),
                                 os.path.join(output_path, '18A-467_HI_spw_0.ms.contsub'))
