###Channel 
CH00=Channel('CH00','MEM01[C]','OCV0[V]')
CH01=Channel('CH01','MEM02[C]','OCV1[V]')
CH02=Channel('CH02','MEM03[C]','OCV2[V]')
CH03=Channel('CH03','MEM04[C]','OCV4[V]')
CH04=Channel('CH04','MEM05[C]','OCV4[V]')
CH05=Channel('CH05','MEM06[C]','OCV5[V]')
CH06=Channel('CH06','MEM07[C]','OCV6[V]')
CH07=Channel('CH07','MEM08[C]','OCV7[V]')

CH00_workstation= Channel('CH00','MEM02[C]','OCV01[mV]')
CH01_workstation= Channel('CH01','MEM02[C]','OCV02[mV]')
CH02_workstation= Channel('CH02','MEM02[C]','OCV03[mV]')
CH03_workstation= Channel('CH03','MEM02[C]','OCV04[mV]')
CH04_workstation= Channel('CH04','MEM04[C]','OCV05[mV]')
CH05_workstation= Channel('CH05','MEM04[C]','OCV06[mV]')
CH06_workstation= Channel('CH06','MEM04[C]','OCV07[mV]')
CH07_workstation= Channel('CH07','MEM04[C]','OCV08[mV]')

CH00_workstation_old= Channel('CH00','MEM02[oC]','OCV01[mV]')
CH01_workstation_old= Channel('CH01','MEM02[oC]','OCV02[mV]')
CH02_workstation_old= Channel('CH02','MEM02[oC]','OCV03[mV]')
CH03_workstation_old= Channel('CH03','MEM02[oC]','OCV04[mV]')
CH04_workstation_old= Channel('CH04','MEM04[oC]','OCV05[mV]')
CH05_workstation_old= Channel('CH05','MEM04[oC]','OCV06[mV]')
CH06_workstation_old= Channel('CH06','MEM04[oC]','OCV07[mV]')
CH07_workstation_old= Channel('CH07','MEM04[oC]','OCV08[mV]')

###Battery
LFP01=Battery('LFP01',1500,39.598,29.10,'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/RPT/RPT_Data/LFP_cell01.mpt','')
LFP02=Battery('LFP02',1500,39.726,28.44,'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/RPT/RPT_Data/LFP_cell02.mpt','C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/RPT/Impedance/LFP_cell02_GEIS_CA2.mpt')
LFP03=Battery('LFP03',1500,39.391,29.28,'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/RPT/RPT_Data/LFP_cell03.mpt','C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/RPT/Impedance/LFP_cell03_GEIS_CA3.mpt')
LFP04=Battery('LFP04',1500,39.801,28.11,'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/RPT/RPT_Data/LFP_cell04.mpt','C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/RPT/Impedance/LFP_cell04_GEIS_CA4.mpt')
LFP05=Battery('LFP05',1500,40.072,27.98,'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/RPT/RPT_Data/LFP_cell05.mpt','C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/RPT/Impedance/LFP_cell05_GEIS_CA5.mpt')
LFP06=Battery('LFP06',1500,39.522,28.60,'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/RPT/RPT_Data/LFP_cell06.mpt','C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/RPT/Impedance/LFP_cell06_CA6.mpt')
LFP07=Battery('LFP07',1500,40.036,28.07,'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/RPT/RPT_Data/LFP_cell07.mpt','C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/RPT/Impedance/LFP_cell07_GEIS_CA7.mpt')
LFP08=Battery('LFP08',1500,39.505,29.32,'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/RPT/RPT_Data/LFP_cell08.mpt','C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/RPT/Impedance/LFP_cell08_GEIS_CA8.mpt')
LFP09=Battery('LFP09',1500,39.457,29.55,'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/RPT/RPT_Data/LFP_cell09.csv','')
LFP10=Battery('LFP10',1500,40.050,28.84,'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/RPT/RPT_Data/LFP_cell10.csv','')

graphite=Battery('Graphite',1,1,1,'','')


##Battery group
batteryLFP=Battery_group([LFP01,LFP02,LFP03,LFP04,LFP05,LFP06,LFP07,LFP08,LFP09,LFP10])

battery_impedance=Battery_group([LFP02,LFP03,LFP04,LFP05,LFP07])

### graphite
graph_exp_dis=Experiment('Entropy',2,1,graphite,CH00_workstation,20,3,28,[28,28,25,22,28],'C:/Users/Aurore/Desktop/20um_no9_disentropy.txt')
#graph_exp_dis.method_entropy_matlab_plot('C:/Users/Aurore/Desktop/20um_no9_disentropyentropy.csv')
graph_exp_ch=Experiment('Entropy',2,1,graphite,CH01_workstation,20,3,48,[48,48,45,42,48],'C:/Users/Aurore/Desktop/20um_no15_chentropy_47deg.txt')
#graph_exp_ch.method_entropy_matlab_plot('C:/Users/Aurore/Desktop/20um_no15_chentropy_47degentropy.csv')
graph_dis_28=Experiment('Entropy',2,1,graphite,CH00_workstation,20,3,28,[28,28,25,22,28],'C:/Users/Aurore/Desktop/20um_no9_disentropy.txt')
graph_dis_38=Experiment('Entropy',2,1,graphite,CH04_workstation2,20,3,38,[38,38,35,32,38],'C:/Users/Aurore/Desktop/20um_dischargeentropy38_no21.txt')
graph_ch_28=Experiment('Entropy',1,1,graphite,CH04_workstation,20,3,28,[28,28,25,22,28],'C:/Users/Aurore/Desktop/20um_no13_chentropy.txt')
graph_ch_38=Experiment('Entropy',1,1,graphite,CH00_workstation2,20,3,38,[38,38,35,32,38],'C:/Users/Aurore/Desktop/20um_chargeentropy38_no25.txt')

graph_ch_group=Experiment_group(1,[graph_ch_28,graph_ch_38])
graph_dis_group=Experiment_group(2,[graph_dis_28,graph_dis_38])


###Discharge 20min 28C
exp1=Experiment('Entropy',2,2,LFP01,CH00,20,3,28,[28,28,25,22,28],'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Discharge_20min_28C/Discharge_entropy20mins-CH00.txt')
exp2=Experiment('Entropy',2,2,LFP02,CH01,20,3,28,[28,28,25,22,28],'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Discharge_20min_28C/Discharge_entropy20mins-CH01.txt')
exp3=Experiment('Entropy',2,2,LFP03,CH02,20,3,28,[28,28,25,22,28],'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Discharge_20min_28C/Discharge_entropy20mins-CH02.txt')
exp4=Experiment('Entropy',2,2,LFP04,CH03,20,3,28,[28,28,25,22,28],'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Discharge_20min_28C/Discharge_entropy20mins-CH03.txt')
#exp4.entropy_OCV_plot('C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment//Discharge_20min_28C/Discharge_entropy20mins-CH03/Discharge_entropy20mins-CH03entropy.csv')
exp5=Experiment('Entropy',2,2,LFP05,CH04,20,3,28,[28,28,25,22,28],'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Discharge_20min_28C/Discharge_entropy20mins-CH04.txt')
#exp5.entropy_matlab_plot('C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Discharge_20min_28C/Discharge_entropy20mins-CH04/Discharge_entropy20mins-CH04entropy.csv')
exp6=Experiment('Entropy',2,2,LFP06,CH05,20,3,28,[28,28,25,22,28],'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Discharge_20min_28C/Discharge_entropy20mins-CH05.txt')
exp7=Experiment('Entropy',2,2,LFP07,CH06,20,3,28,[28,28,25,22,28],'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Discharge_20min_28C/Discharge_entropy20mins-CH06.txt')
exp8=Experiment('Entropy ',2,2,LFP08,CH07,20,3,28,[28,28,25,22,28],'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Discharge_20min_28C/Discharge_entropy20mins-CH07.txt')

exp_list_discharge_20min_28=Experiment_group('Discharge 20 min',[exp1,exp3,exp4,exp5,exp6,exp7,exp8])

###Charge 20min 28C
exp_charge_20min_28_CH00=Experiment('Entropy',1,2,LFP01,CH00,20,3,28,[28,28,25,22,28],'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Charge_20min_28C/Entropy_charge_20min_CH00.txt')
exp_charge_20min_28_CH02=Experiment('Entropy',1,2,LFP03,CH02,20,3,28,[28,28,25,22,28],'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Charge_20min_28C/Entropy_charge_20min_CH02.txt')
exp_charge_20min_28_CH03=Experiment('Entropy',1,2,LFP04,CH03,20,3,28,[28,28,25,22,28],'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Charge_20min_28C/Entropy_charge_20min_CH03.txt')
exp_charge_20min_28_CH04=Experiment('Entropy',1,2,LFP05,CH04,20,3,28,[28,28,25,22,28],'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Charge_20min_28C/Entropy_charge_20min_CH04.txt')
exp_charge_20min_28_CH05=Experiment('Entropy',1,2,LFP06,CH05,20,3,28,[28,28,25,22,28],'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Charge_20min_28C/Entropy_charge_20min_CH05.txt')
exp_charge_20min_28_CH06=Experiment('Entropy',1,2,LFP07,CH06,20,3,28,[28,28,25,22,28],'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Charge_20min_28C/Entropy_charge_20min_CH06.txt')
exp_charge_20min_28_CH07=Experiment('Entropy',1,2,LFP08,CH07,20,3,28,[28,28,25,22,28],'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Charge_20min_28C/Entropy_charge_20min_CH07.txt')

exp_list_charge_20min_28=Experiment_group('Charge 20 min',[exp_charge_20min_28_CH00,exp_charge_20min_28_CH02,exp_charge_20min_28_CH03,exp_charge_20min_28_CH04, exp_charge_20min_28_CH05, exp_charge_20min_28_CH06, exp_charge_20min_28_CH07])

### Discharge 15min 28C

exp_discharge_15min_28_CH00=Experiment('Entropy ',2,2,LFP01,CH00,15,3,28,[28,28,25,22,28],'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Discharge_15min_28C/Discharge_entropy_15min_CH00.txt')
exp_discharge_15min_28_CH02=Experiment('Entropy ',2,2,LFP03,CH02,15,3,28,[28,28,25,22,28],'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Discharge_15min_28C/Discharge_entropy_15min_CH02.txt')
exp_discharge_15min_28_CH03=Experiment('Entropy ',2,2,LFP04,CH03,15,3,28,[28,28,25,22,28],'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Discharge_15min_28C/Discharge_entropy_15min_CH03.txt')
exp_discharge_15min_28_CH04=Experiment('Entropy ',2,2,LFP05,CH04,15,3,28,[28,28,25,22,28],'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Discharge_15min_28C/Discharge_entropy_15min_CH04.txt')
#exp_discharge_15min_28_CH04.entropy_OCV_plot('C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Discharge_15min_28C/Discharge_entropy_15min_CH04/Discharge_entropy_15min_CH04entropy.csv')
exp_discharge_15min_28_CH05=Experiment('Entropy ',2,2,LFP06,CH05,15,3,28,[28,28,25,22,28],'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Discharge_15min_28C/Discharge_entropy_15min_CH05.txt')
exp_discharge_15min_28_CH06=Experiment('Entropy ',2,2,LFP07,CH06,15,3,28,[28,28,25,22,28],'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Discharge_15min_28C/Discharge_entropy_15min_CH06.txt')
exp_discharge_15min_28_CH07=Experiment('Entropy ',2,2,LFP08,CH07,15,3,28,[28,28,25,22,28],'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Discharge_15min_28C/Discharge_entropy_15min_CH07.txt')

exp_group_15min=Experiment_group('Discharge 15 min' ,[exp_discharge_15min_28_CH00, exp_discharge_15min_28_CH02, exp_discharge_15min_28_CH03, exp_discharge_15min_28_CH04, exp_discharge_15min_28_CH05, exp_discharge_15min_28_CH06, exp_discharge_15min_28_CH07])

###Charge 15min 28C
exp_charge_15min_28_CH00=Experiment('Entropy ',1,2,LFP01,CH00,15,3,28,[28,28,25,22,28],'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Charge_15min_28C/Entropy_charge_15min_CH00.txt')
exp_charge_15min_28_CH02=Experiment('Entropy ',1,2,LFP03,CH02,15,3,28,[28,28,25,22,28],'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Charge_15min_28C/Entropy_charge_15min_CH02.txt')
exp_charge_15min_28_CH03=Experiment('Entropy ',1,2,LFP04,CH03,15,3,28,[28,28,25,22,28],'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Charge_15min_28C/Entropy_charge_15min_CH03.txt')
exp_charge_15min_28_CH04=Experiment('Entropy ',1,2,LFP05,CH04,15,3,28,[28,28,25,22,28],'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Charge_15min_28C/Entropy_charge_15min_CH04.txt')
exp_charge_15min_28_CH05=Experiment('Entropy ',1,2,LFP06,CH05,15,3,28,[28,28,25,22,28],'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Charge_15min_28C/Entropy_charge_15min_CH05.txt')
exp_charge_15min_28_CH06=Experiment('Entropy ',1,2,LFP07,CH06,15,3,28,[28,28,25,22,28],'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Charge_15min_28C/Entropy_charge_15min_CH06.txt')
exp_charge_15min_28_CH07=Experiment('Entropy ',1,2,LFP08,CH07,15,3,28,[28,28,25,22,28],'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Charge_15min_28C/Entropy_charge_15min_CH07.txt')

exp_group_15min_charge=Experiment_group('Charge 15 min',[exp_charge_15min_28_CH00,exp_charge_15min_28_CH02,exp_charge_15min_28_CH03, exp_charge_15min_28_CH04, exp_charge_15min_28_CH05, exp_charge_15min_28_CH06, exp_charge_15min_28_CH07])




### Discharge 20min 38C
exp_discharge_20min_38_CH00=Experiment('Entropy',2,2,LFP01,CH00,20,3,38,[38,38,35,32,38],'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Discharge_20min_38C/Discharge_entropy_20min_38C_CH00.txt')
exp_discharge_20min_38_CH02=Experiment('Entropy',2,2,LFP03,CH02,20,3,38,[38,38,35,32,38],'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Discharge_20min_38C/Discharge_entropy_20min_38C_CH02.txt')
exp_discharge_20min_38_CH03=Experiment('Entropy',2,2,LFP04,CH03,20,3,38,[38,38,35,32,38],'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Discharge_20min_38C/Discharge_entropy_20min_38C_CH03.txt')
exp_discharge_20min_38_CH04=Experiment('Entropy',2,2,LFP05,CH04,20,3,38,[38,38,35,32,38],'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Discharge_20min_38C/Discharge_entropy_20min_38C_CH04.txt')
exp_discharge_20min_38_CH05=Experiment('Entropy',2,2,LFP06,CH05,20,3,38,[38,38,35,32,38],'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Discharge_20min_38C/Discharge_entropy_20min_38C_CH05.txt')
exp_discharge_20min_38_CH06=Experiment('Entropy',2,2,LFP07,CH06,20,3,38,[38,38,35,32,38],'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Discharge_20min_38C/Discharge_entropy_20min_38C_CH06.txt')
exp_discharge_20min_38_CH07=Experiment('Entropy',2,2,LFP08,CH07,20,3,38,[38,38,35,32,38],'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Discharge_20min_38C/Discharge_entropy_20min_38C_CH07.txt')


exp_group_20min_discharge_38=Experiment_group('Discharge 20min 38C',[exp_discharge_20min_38_CH00,exp_discharge_20min_38_CH02,exp_discharge_20min_38_CH03,exp_discharge_20min_38_CH04, exp_discharge_20min_38_CH05,exp_discharge_20min_38_CH05,exp_discharge_20min_38_CH06])


###Charge 20min 38C
exp_charge_20min_38_CH00=Experiment('Entropy',1,2,LFP01,CH00,20,3,38,[38,38,35,32,38],'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Charge_20min_38C/Charge_entropy_20min_38C_CH00.txt')
exp_charge_20min_38_CH02=Experiment('Entropy',1,2,LFP03,CH02,20,3,38,[38,38,35,32,38],'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Charge_20min_38C/Charge_entropy_20min_38C_CH02.txt')
exp_charge_20min_38_CH03=Experiment('Entropy',1,2,LFP04,CH03,20,3,38,[38,38,35,32,38],'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Charge_20min_38C/Charge_entropy_20min_38C_CH03.txt')
exp_charge_20min_38_CH04=Experiment('Entropy',1,2,LFP05,CH04,20,3,38,[38,38,35,32,38],'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Charge_20min_38C/Charge_entropy_20min_38C_CH04.txt')
exp_charge_20min_38_CH05=Experiment('Entropy',1,2,LFP06,CH05,20,3,38,[38,38,35,32,38],'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Charge_20min_38C/Charge_entropy_20min_38C_CH05.txt')
exp_charge_20min_38_CH06=Experiment('Entropy',1,2,LFP07,CH06,20,3,38,[38,38,35,32,38],'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Charge_20min_38C/Charge_entropy_20min_38C_CH06.txt')
exp_charge_20min_38_CH07=Experiment('Entropy',1,2,LFP08,CH07,20,3,38,[38,38,35,32,38],'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Charge_20min_38C/Charge_entropy_20min_38C_CH07.txt')


###Discharge 15min 38C
exp_discharge_15min_38_CH00=Experiment('Entropy',2,2,LFP01,CH00,15,3,38,[38,38,35,32,38],'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Discharge_15min_38C/Entropy_discharge_15min_38C_CH00.txt')
exp_discharge_15min_38_CH02=Experiment('Entropy ',2,2,LFP03,CH02,15,3,38,[38,38,35,32,38],'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Discharge_15min_38C/Entropy_discharge_15min_38C_CH02.txt')
exp_discharge_15min_38_CH03=Experiment('Entropy ',2,2,LFP04,CH03,15,3,38,[38,38,35,32,38],'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Discharge_15min_38C/Entropy_discharge_15min_38C_CH03.txt')
exp_discharge_15min_38_CH04=Experiment('Entropy ',2,2,LFP05,CH04,15,3,38,[38,38,35,32,38],'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Discharge_15min_38C/Entropy_discharge_15min_38C_CH04.txt')
exp_discharge_15min_38_CH05=Experiment('Entropy ',2,2,LFP06,CH05,15,3,38,[38,38,35,32,38],'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Discharge_15min_38C/Entropy_discharge_15min_38C_CH05.txt')
exp_discharge_15min_38_CH06=Experiment('Entropy ',2,2,LFP07,CH06,15,3,38,[38,38,35,32,38],'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Discharge_15min_38C/Entropy_discharge_15min_38C_CH06.txt')
exp_discharge_15min_38_CH07=Experiment('Entropy ',2,2,LFP08,CH07,15,3,38,[38,38,35,32,38],'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Discharge_15min_38C/Entropy_discharge_15min_38C_CH07.txt')


###Charge 15min 38C
exp_charge_15min_38_CH00=Experiment('Entropy',1,2,LFP01,CH00,15,3,38,[38,38,35,32,38],'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Charge_15min_38C/entropy_charge_15min_38C_CH00.txt')
exp_charge_15min_38_CH02=Experiment('Entropy',1,2,LFP03,CH02,15,3,38,[38,38,35,32,38],'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Charge_15min_38C/entropy_charge_15min_38C_CH02.txt')
exp_charge_15min_38_CH03=Experiment('Entropy',1,2,LFP04,CH03,15,3,38,[38,38,35,32,38],'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Charge_15min_38C/entropy_charge_15min_38C_CH03.txt')
exp_charge_15min_38_CH04=Experiment('Entropy',1,2,LFP05,CH04,15,3,38,[38,38,35,32,38],'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Charge_15min_38C/entropy_charge_15min_38C_CH04.txt')
exp_charge_15min_38_CH05=Experiment('Entropy',1,2,LFP06,CH05,15,3,38,[38,38,35,32,38],'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Charge_15min_38C/entropy_charge_15min_38C_CH05.txt')
exp_charge_15min_38_CH06=Experiment('Entropy',1,2,LFP07,CH06,15,3,38,[38,38,35,32,38],'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Charge_15min_38C/entropy_charge_15min_38C_CH06.txt')
exp_charge_15min_38_CH07=Experiment('Entropy',1,2,LFP08,CH07,15,3,38,[38,38,35,32,38],'C:/Users/Aurore/Documents/Mines de Nantes/Stage international/Lancaster University/Entropy_experiment/Charge_15min_38C/entropy_charge_15min_38C_CH07.txt')









