from __future__ import division, print_function
import numpy as np
import scipy as sp
import scipy.io as sio
import matplotlib.pyplot as plt
import pickle
import csv
import glob
import pandas as pd

# import functions
import FuncParcel

# vector of cortical ROI index
Cortical_ROIs = np.loadtxt('/home/despoB/kaihwang/bin/FuncParcel/Data/Cortical_ROI_index')

# list of subjects
Control_Subj = ['1103', '1220', '1306', '1223', '1314', '1311', '1318', '1313', '1326', '1325', '1328', '1329', '1333', '1331', '1335', '1338', '1336', '1339', '1337', '1344', '1340']
thalamic_patients = ['128', '162', '163', '168', '176']
striatal_patients = ['b117', 'b122', 'b138', 'b143', 'b153']


# create control's dataframe
OlderControlGlobalData = pd.DataFrame()
OlderControlNodalData = pd.DataFrame()
for s in Control_Subj:
	fn = '/home/despoB/kaihwang/Rest/Graph/gsetCI_%s.mat' %s
	GlobalData, NodalData = FuncParcel.convert_matlab_graph_str(fn, s, Cortical_ROIs)
	OlderControlGlobalData = OlderControlGlobalData.append(GlobalData)
	OlderControlNodalData = OlderControlNodalData.append(NodalData)
OlderControlNodalData['Group'] = 'Control'
OlderControlGlobalData['Group'] = 'Control'

# convert patients' global graph metrics into z-score
PatientsGlobalData = pd.DataFrame()
PatientsNodalData = pd.DataFrame()
for p in thalamic_patients:
	fn = '/home/despoB/kaihwang/Rest/Graph/gsetCI_%s.mat' %p
	GlobalData, NodalData = FuncParcel.convert_matlab_graph_str(fn, p, Cortical_ROIs)
	GlobalData['Q_zscore'] = FuncParcel.cal_graph_z_score(p, fn, Cortical_ROIs, OlderControlGlobalData, 1, 'Q')
	GlobalData['CC_zscore'] = FuncParcel.cal_graph_z_score(p, fn, Cortical_ROIs, OlderControlGlobalData, 1, 'CC')
	GlobalData['Group'] = 'Thalamic_patients'
	NodalData['PC_zscore'] = FuncParcel.cal_graph_z_score(p, fn, Cortical_ROIs, OlderControlNodalData, 0, 'PC')
	NodalData['localE_zscore'] = FuncParcel.cal_graph_z_score(p, fn, Cortical_ROIs, OlderControlNodalData, 0, 'localE')
	NodalData['Between_Module_Weight_zscore'] = FuncParcel.cal_graph_z_score(p, fn, Cortical_ROIs, OlderControlNodalData, 0, 'Between_Module_Weight')
	NodalData['Within_Module_Weight_zscore'] = FuncParcel.cal_graph_z_score(p, fn, Cortical_ROIs, OlderControlNodalData, 0, 'Within_Module_Weight')
	NodalData['Between_Module_Degree_zscore'] = FuncParcel.cal_graph_z_score(p, fn, Cortical_ROIs, OlderControlNodalData, 0, 'Between_Module_Degree')
	NodalData['Within_Module_Degree_zscore'] = FuncParcel.cal_graph_z_score(p, fn, Cortical_ROIs, OlderControlNodalData, 0, 'Within_Module_Degree')
	NodalData['Group'] = 'Thalamic_patients'
	PatientsGlobalData = PatientsGlobalData.append(GlobalData)
	PatientsNodalData = PatientsNodalData.append(NodalData)

for p in striatal_patients:
	fn = '/home/despoB/kaihwang/Rest/Graph/gsetCI_%s.mat' %p
	GlobalData, NodalData = FuncParcel.convert_matlab_graph_str(fn, p, Cortical_ROIs)
	GlobalData['Q_zscore'] = FuncParcel.cal_graph_z_score(p, fn, Cortical_ROIs, OlderControlGlobalData, 1, 'Q')
	GlobalData['CC_zscore'] = FuncParcel.cal_graph_z_score(p, fn, Cortical_ROIs, OlderControlGlobalData, 1, 'CC')
	GlobalData['Group'] = 'Striatal_patients'
	NodalData['PC_zscore'] = FuncParcel.cal_graph_z_score(p, fn, Cortical_ROIs, OlderControlNodalData, 0, 'PC')
	NodalData['localE_zscore'] = FuncParcel.cal_graph_z_score(p, fn, Cortical_ROIs, OlderControlNodalData, 0, 'localE')
	NodalData['Between_Module_Weight_zscore'] = FuncParcel.cal_graph_z_score(p, fn, Cortical_ROIs, OlderControlNodalData, 0, 'Between_Module_Weight')
	NodalData['Within_Module_Weight_zscore'] = FuncParcel.cal_graph_z_score(p, fn, Cortical_ROIs, OlderControlNodalData, 0, 'Within_Module_Weight')
	NodalData['Between_Module_Degree_zscore'] = FuncParcel.cal_graph_z_score(p, fn, Cortical_ROIs, OlderControlNodalData, 0, 'Between_Module_Degree')
	NodalData['Within_Module_Degree_zscore'] = FuncParcel.cal_graph_z_score(p, fn, Cortical_ROIs, OlderControlNodalData, 0, 'Within_Module_Degree')
	NodalData['Group'] = 'Striatal_patients'
	PatientsGlobalData = PatientsGlobalData.append(GlobalData)
	PatientsNodalData = PatientsNodalData.append(NodalData)

#combine dataframes
GraphGlobalData = pd.DataFrame()
GraphNodalData = pd.DataFrame()

GraphGlobalData = PatientsGlobalData.append(OlderControlGlobalData)
GraphNodalData = PatientsNodalData.append(OlderControlNodalData)

GraphGlobalData.to_csv('Data/GraphGlobalData.csv')
GraphNodalData.to_csv('Data/GraphNodalData.csv')
#cleanup
#reset_selective GlobalData
#reset_selective NodalData
#reset_selective OlderControlGlobalData
#reset_selective OlderControlNodalData


