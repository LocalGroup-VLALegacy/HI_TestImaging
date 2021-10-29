

This folder contains example scripts for imaging individual HI channels in a cluster environment.

There will eventually be 3 steps for the imaging process:

1. Split the complete MS into individual channel MSs (no script here currently, but this is simple to do with CASA's mstransform task and a for loop).
2. Submit individual imaging jobs for each channel. (`HI_single_channel_clean.py`; params from `tclean_params_example.saved`).
3. Once images, concatenate the channels back into a cube (`concat_channels.py`).

These scripts are not a minimal example but can be used a starting point for further development.

Also note that we would eventually like to incorporate these steps into the [PHANGS imaging pipeline](https://github.com/akleroy/phangs_imaging_scripts) since it incorporates data handling and all steps needed to get to step 1 here.
