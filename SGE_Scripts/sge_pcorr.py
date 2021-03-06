# for calculating pcorr, and for sge.

import sys
from FuncParcel import *
from functools import partial
from multiprocessing import Pool
from itertools import product
import time

# script to do partial corr

def function_cal_pcorr_mat(subject, tharoi):
	ROIs = ['_Ses1_Gordon_333_cortical'] #'Craddock_300_cortical' 'Cortical_CI', 'Cortical_ROIs' 'Craddock_300_cortical' Gordon_333_cortical
	ts_path = '/home/despoB/connectome-thalamus/NotBackedUp/TS/MGH_'
	pcorr_path = '/home/despoB/kaihwang/Rest/NotBackedUp/ParMatrices/'
	fn = ts_path + subject + '_Ses1_%s_TS_000.netts' %tharoi
	thalamus_ts = np.loadtxt(fn)
	for roi in ROIs:

		fn = ts_path + subject + roi + '_TS_000.netts' 
		cortical_roi_ts = np.loadtxt(fn)

		#create output
		# pcorr_mat = np.zeros((thalamus_ts.shape[0],cortical_roi_ts.shape[0]),dtype=np.float)

		# #start parfor
		# pf = partial(par_pcorr_subcortico_cortical_connectivity, subcortical_ts=thalamus_ts, cortical_ts=cortical_roi_ts)
		
		# for idx, r in enumerate(pool.imap(pf, product(range(thalamus_ts.shape[0]), range(cortical_roi_ts.shape[0])),chunksize = 160)):
		# 	pcorr_mat.flat[idx] = r

		pcorr_mat = pcorr_subcortico_cortical_connectivity(thalamus_ts, cortical_roi_ts)
		
		fn = pcorr_path + 'MGH_' + subject + roi +'_' + tharoi + '_pcorr_mat'
		#np.savetxt(fn, pcorr_mat, fmt='%.4f')
		save_object(pcorr_mat, fn)

subject = sys.stdin.read().strip('\n')

trois = ['Thalamus_fslana', 'Thalamus_Morel_consolidated_mask']
for troi in trois:
	function_cal_pcorr_mat(subject, troi)







#this is for testing
# tha_ts = np.random.rand(3500, 900)
# cort_ts = np.random.rand(60, 900)

# #test non parallel
# start = time.time()
# pcorr_mat = pcorr_subcortico_cortical_connectivity(tha_ts, cort_ts)
# end = time.time()

# nonpar_time = end -start

# #test for parallel
# pcorr_mat = np.zeros((tha_ts.shape[0],cort_ts.shape[0]),dtype=np.float)
# pf = partial(par_pcorr_subcortico_cortical_connectivity, subcortical_ts=tha_ts, cortical_ts=cort_ts)

# start = time.time()
# for idx, r in enumerate(pool.imap(pf, product(range(3500), range(60)),chunksize = 1050)):
# 	pcorr_mat.flat[idx] = r
# end = time.time()

# par_time = end -start
