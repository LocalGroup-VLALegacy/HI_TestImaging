
'''
This script applies manual source flagging only for the HI line.

'''


myvis = 'M31_B_20A-346.sb38492195.eb38516348.59050.30097761574.speclines_HI.ms.contsub.regrid2kms'
# None for HI

myvis = 'M31_B_20A-346.sb38707953.eb38714315.59132.04043678241.speclines_HI.ms.contsub.regrid2kms'
# None for HI

myvis = 'M31_B_20A-346.sb38491509.eb38714905.59133.19162402778.speclines_HI.ms.contsub.regrid2kms'
flagdata(vis=myvis, mode='manual',
         field='M31LARGE_29',
         scan='44',
         timerange='2020/10/11/07:33:13.5~2020/10/11/07:33:20',
         reason='[MANUAL] Issue: Amp spike. Flagged by Eric',
         flagbackup=False)
flagdata(vis=myvis, mode='manual',
         field='M31LARGE_27',
         scan='42',
         timerange='<2020/10/11/07:21:28.5',
         reason='[MANUAL] Issue: Amp spike. Flagged by Eric',
         flagbackup=False)
flagdata(vis=myvis, mode='manual',
         field='M31LARGE_15',
         scan='26',
         timerange='<2020/10/11/06:15:13.5',
         reason='[MANUAL] Issue: Amp spike. Flagged by Eric',
         flagbackup=False)
flagdata(vis=myvis, mode='manual',
         field='M31LARGE_21',
         scan='34',
         timerange='<2020/10/11/06:48:46.5',
         reason='[MANUAL] Issue: Amp spike. Flagged by Eric',
         flagbackup=False)
flagdata(vis=myvis, mode='manual',
         field='M31LARGE_24',
         scan='38',
         timerange='<2020/10/11/07:05:07.5',
         reason='[MANUAL] Issue: Amp spike. Flagged by Eric',
         flagbackup=False)
flagmanager(vis=myvis, mode='save', versionname='manual_flagging')

myvis = 'M31_B_20A-346.sb38491509.eb38715699.59134.11144230324.speclines_HI.ms.contsub.regrid2kms'
flagdata(vis=myvis, mode='manual',
        field='M31LARGE_39',
        scan='58',
        timerange='<2020/10/12/06:32:43.5',
        reason='[MANUAL] Issue: Amp spike. Flagged by Eric',
        flagbackup=False)
flagdata(vis=myvis, mode='manual',
        field='M31LARGE_42',
        scan='62',
        timerange='<2020/10/12/06:48:58.5',
        reason='[MANUAL] Issue: Amp spike. Flagged by Eric',
        flagbackup=False)
flagdata(vis=myvis, mode='manual',
        field='M31LARGE_45',
        scan='66',
        timerange='<2020/10/12/07:05:16.5',
        reason='[MANUAL] Issue: Amp spike. Flagged by Eric',
        flagbackup=False)
flagdata(vis=myvis, mode='manual',
        field='M31LARGE_47',
        scan='68',
        timerange='<2020/10/12/07:15:00' ,
        reason='[MANUAL] Issue: RFI. Flagged by Eric',
        flagbackup=False)
flagmanager(vis=myvis, mode='save', versionname='manual_flagging')


myvis = 'M31_B_20A-346.sb38491509.eb38715699.59134.11144230324.speclines_HI.ms.contsub.regrid2kms'
flagdata(vis=myvis, mode='manual',
         field='M31LARGE_12',
         scan='22',
         timerange='<2020/10/15/06:53:25.5',
         reason='[MANUAL] Issue: Not on source. Flagged by Eric',
         flagbackup=False)
flagdata(vis=myvis, mode='manual',
         field='M31LARGE_18',
         scan='30',
         timerange='<2020/10/15/07:26:19.5',
         reason='[MANUAL] Issue: Not on source. Flagged by Eric',
         flagbackup=False)
flagdata(vis=myvis, mode='manual',
         field='M31LARGE_6',
         scan='14',
         timerange='<2020/10/15/06:21:19.5',
         reason='[MANUAL] Issue: Not on source. Flagged by Eric',
         flagbackup=False)
flagmanager(vis=myvis, mode='save', versionname='manual_flagging')


myvis = 'M31_C_20A-346.sb38095502.eb38174408.58988.69745849537.speclines_HI.ms.contsub.regrid2kms'
# None for HI

myvis = 'M31_C_20A-346.sb38096442.eb38209668.58991.5012732176.speclines_HI.ms.contsub.regrid2kms'
flagdata(vis=myvis, mode='manual',
         field='M31LARGE_14',
         scan='54',
         timerange='<2020/05/22/16:09:37.5',
         reason='[MANUAL] Issue: Not on source. Flagged by Eric',
         flagbackup=False)
flagdata(vis=myvis, mode='manual',
         field='M31LARGE_43',
         scan='31',
         antenna='ea08&&ea22',
         reason='[MANUAL] Issue: Amp outlier. Flagged by Eric',
         flagbackup=False)
flagdata(vis=myvis, mode='manual',
         field='M31LARGE_44',
         scan='32',
         antenna='ea08&&ea22',
         reason='[MANUAL] Issue: Amp outlier. Flagged by Eric',
         flagbackup=False)
flagmanager(vis=myvis, mode='save', versionname='manual_flagging')


myvis = 'M31_C_20A-346.sb38096442.eb38216745.58992.52579186343.speclines_HI.ms.contsub.regrid2kms'
flagdata(vis=myvis, mode='manual',
         field='M31LARGE_0',
         scan='38',
         timerange='<2020/05/23/15:27:37.5',
         reason='[MANUAL] Issue: Not on source. Flagged by Eric',
         flagbackup=False)
flagdata(vis=myvis, mode='manual',
         field='M31LARGE_26',
         scan='11',
         antenna='ea08&&ea22',
         reason='[MANUAL] Issue: Amp spike. Flagged by Eric',
         flagbackup=False)
flagdata(vis=myvis, mode='manual',
         field='M31LARGE_29',
         scan='15',
         timerange='>2020/05/23/13:41:07.5',
         reason='[MANUAL] Issue: RFI  . Flagged by Eric',
         flagbackup=False)
flagdata(vis=myvis, mode='manual',
         field='M31LARGE_30',
         scan='16',
         antenna='ea08&&ea22',
         reason='[MANUAL] Issue: Amp spike. Flagged by Eric',
         flagbackup=False)
flagmanager(vis=myvis, mode='save', versionname='manual_flagging')

myvis = 'M31_C_20A-346.sb38097770.eb38161238.58986.707791782406.speclines_HI.ms.contsub.regrid2kms'
# None for HI

myvis = 'M31_C_20A-346.sb38098105.eb38158028.58985.68987263889.speclines_HI.ms.contsub.regrid2kms'
flagdata(vis=myvis, mode='manual',
         field='',
         antenna='ea20&&ea22',
         reason='[MANUAL] Issue: Consistent low amp in 1 baseline. Flagged by Eric',
         flagbackup=False)
flagdata(vis=myvis, mode='manual',
         field='M31LARGE_0',
         scan='22',
         timerange='<2020/05/16/18:08:12.5',
         reason='[MANUAL] Issue: Not on source. Flagged by Eric',
         flagbackup=False)
flagdata(vis=myvis, mode='manual',
         field='M31LARGE_28',
         scan='54',
         timerange='<2020/05/16/20:41:42.5',
         reason='[MANUAL] Issue: Not on source. Flagged by Eric',
         flagbackup=False)
flagdata(vis=myvis, mode='manual',
         field='M31LARGE_42',
         scan='14',
         timerange='<2020/05/16/17:29:52.5',
         reason='[MANUAL] Issue: Not on source. Flagged by Eric',
         flagbackup=False)
flagmanager(vis=myvis, mode='save', versionname='manual_flagging')


myvis = 'M31_C_20A-346.sb38098534.eb38272581.59009.385237395836.speclines_HI.ms.contsub.regrid2kms'
# None for HI

myvis = 'M31_A_20A-346.sb38951534.eb39180381.59198.11168030092.speclines_HI.ms.contsub.regrid2kms'
flagdata(vis=myvis, mode='manual',
         field='',
         scan='68~79',
         antenna='ea01,ea03,ea04,ea05,ea06,ea07,ea08,ea11,ea14,ea15,ea20,ea21,ea24',
         reason='[MANUAL] Issue: Consistent spike in gain cal phases towards track end. Flagged by Eric',
         flagbackup=False)
flagdata(vis=myvis, mode='manual',
         field='',
         scan='59~79',
         antenna='ea17',
         reason='[MANUAL] Issue: Consistent spike in gain cal phases towards track ,end. Flagged by Eric',
         flagbackup=False)
flagdata(vis=myvis, mode='manual',
         field='M31LARGE_17', scan='17',
         timerange='>2020/12/15/03:44:33.0',
         reason='[MANUAL] Issue: RFI . Flagged by Eric',
         flagbackup=False)
flagdata(vis=myvis, mode='manual',
         field='M31LARGE_18', scan='10',
         timerange='<2020/12/15/03:16:07',
         reason='[MANUAL] Issue: Not on source. Flagged by Eric',
         flagbackup=False)
flagdata(vis=myvis, mode='manual',
         field='M31LARGE_18', scan='19',
         timerange='<2020/12/15/03:49:13',
         reason='[MANUAL] Issue: Not on source. Flagged by Eric',
         flagbackup=False)
flagdata(vis=myvis, mode='manual',
         field='M31LARGE_31', scan='66',
         timerange='>2020/12/15/06:44:29.0',
         reason='[MANUAL] Issue: RFI spike. Flagged by Eric',
         flagbackup=False)
flagdata(vis=myvis, mode='manual',
         field='M31LARGE_5', scan='60',
         timerange='<2020/12/15/06:21:13',
         reason='[MANUAL] Issue: Not on source. Flagged by Eric',
         flagbackup=False)
flagdata(vis=myvis, mode='manual',
         field='M31LARGE_5', scan='15',
         timerange='<2020/12/15/03:34:43',
         reason='[MANUAL] Issue: Not on source. Flagged by Eric',
         flagbackup=False)
flagmanager(vis=myvis, mode='save', versionname='manual_flagging')

myvis = 'M31_A_20A-346.sb38951534.eb39181553.59199.09210221065.speclines_HI.ms.contsub.regrid2kms'
flagdata(vis=myvis, mode='manual',
         field='',
         antenna='ea06',
         reason='[MANUAL] Issue: Consistent amp scatter in targets. Flagged by Eric',
         flagbackup=False)
flagdata(vis=myvis, mode='manual',
         field='M31LARGE_18',
         scan='10',
         timerange='<2020/12/16/02:46:03',
         reason='[MANUAL] Issue: Not on source. Flagged by Eric',
         flagbackup=False)
flagdata(vis=myvis, mode='manual',
         field='M31LARGE_18',
         scan='19',
         timerange='<2020/12/16/03:18:55',
         reason='[MANUAL] Issue: Not on source. Flagged by Eric',
         flagbackup=False)
flagdata(vis=myvis, mode='manual',
         field='M31LARGE_18',
         scan='28',
         timerange='<2020/12/16/03:52:07',
         reason='[MANUAL] Issue: Not on source. Flagged by Eric',
         flagbackup=False)
flagdata(vis=myvis, mode='manual',
         field='M31LARGE_18',
         scan='46',
         timerange='<2020/12/16/04:58:35',
         reason='[MANUAL] Issue: Not on source. Flagged by Eric',
         flagbackup=False)
flagdata(vis=myvis, mode='manual',
         field='M31LARGE_18',
         scan='73',
         timerange='<2020/12/16/06:38:25',
         reason='[MANUAL] Issue: Not on source. Flagged by Eric',
         flagbackup=False)
flagdata(vis=myvis, mode='manual',
         field='M31LARGE_32',
         scan='76',
         timerange='<2020/12/16/06:50:27',
         reason='[MANUAL] Issue: RFI  . Flagged by Eric',
         flagbackup=False)
flagdata(vis=myvis, mode='manual',
         field='M31LARGE_5',
         scan='76',
         timerange='>2020/12/16/02:34:25',
         reason='[MANUAL] Issue: RFI  . Flagged by Eric',
         flagbackup=False)
flagdata(vis=myvis, mode='manual',
         field='M31LARGE_5',
         scan='15',
         timerange='<2020/12/16/03:04:27',
         reason='[MANUAL] Issue: Not on source. Flagged by Eric',
         flagbackup=False)