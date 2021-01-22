# HI_TestImaging
Imaging tests with the XL configuration setup

All configurations test: M31_Field17 or M31LARGE_17

* Combines 14A-235 (D), 15A-175 (B, C), 18A-467 (A)


`split_HI_allconfigs.py`: Split out HI, the single A-config pointing, and do contsub where needed.
`check_config_weighting.py`: TODO
`HI_allconfigs_timeonsource.py`: Calculate time on source for all configs and make scan lists to reach equal times.
`manual_imaging_HI_allconfigs.py`: Imaging test with all configs with all integration time we have
`manual_imaging_HI_allconfigs_matchintime.py`: Imaging test with all configs with equal integration time per config

Imaging tests to do at the final 2:2:2:1 time per configuration:

* [ ] ABCD vs. ABC
* [ ] ABC-taper vs. BC for high-res HI
* [ ] ?
