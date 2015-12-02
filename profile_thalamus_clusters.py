### script to profile the distribution of cortical components each thalamus cluster is connected to, "pooled" across subjects
import sys
from brain_graphs import *
from FuncParcel import *
import glob

### setup paths and variables needed
corrmat_path = '/home/despoB/connectome-thalamus/Partial_CorrMats/'
path_to_ROIs = '/home/despoB/connectome-thalamus/ROIs'
output_path = '/home/despoB/connectome-thalamus/Thalamic_parcel/Indiv_consensus/'
Parcel_path = '/home/despoB/connectome-thalamus/Thalamic_parcel'

### load data needed
Thalamus_clusters = np.loadtxt(Parcel_path + '/Thalamus_clusters')
Cortical_ROIs_CI = np.loadtxt(path_to_ROIs + '/Gordon_consensus_CI')
Cortical_ROI_positions = np.array(range(0, len(Cortical_ROIs_CI)))
Thalamocortical_aveMat = np.loadtxt(Parcel_path + '/MGH_Gordon_333_thalamocortical_pcorr_avemat')
Thalamus_voxels = np.loadtxt(path_to_ROIs+'/thalamus_voxel_indices', dtype = int)
Thalamus_voxel_positions = np.array(range(len(Cortical_ROIs_CI),len(Thalamocortical_aveMat)))

#Cortical_Network_CIs = np.loadtxt(path_to_ROIs + '/Gordon_Network_CIs')
#Cortical_Network_CIs_plus_thalamus = np.loadtxt(path_to_ROIs +'/Gordon_CI_plus_thalamus_ROIs')
# Thalamus_voxel_coordinate = np.loadtxt(path_to_ROIs +'/thalamus_voxels_ijk_indices', dtype = int)

#### load the subject's partial corr matrix (bertween the thalamus and the cortex)
# the file pattern, MGH subjects (303 of them), and then with this ROI template: MGH_Gordon_333_consensus_CI*
# MGH*MGH_Gordon_333_consensus_CI*

# file_pattern = 'NKI*Gordon*consensus*'
# pcorrMat_Files = glob.glob(corrmat_path + file_pattern)

# Indiv_Subject_Thalamus_Winner_CIs = np.empty((len(Thalamus_voxels), len(pcorrMat_Files)))

# for i, fn in enumerate(pcorrMat_Files):
# 	M = pickle.load(open(fn, "rb"))

#### step 2:, do the winner take all of thalamus voxel mapping for each subject. 
# 	_, Thalamo_rankCIs, _, = parcel_subcortical_network(M, Cortical_Network_CIs_plus_thalamus, Thalamus_voxels, Cortical_Network_CIs, Cortical_Network_CIs)
# 	# then sourt through the ranking output, and keep the "winner"
# 	Indiv_Subject_Thalamus_Winner_CIs[:,i] = sort_CIs(Thalamo_rankCIs)


#### Get a histogram  for each thalamus cluster
Cluster_profile = {}
for i in np.unique(Thalamus_clusters):
	tmp = np.zeros(len(np.unique(Cortical_ROIs_CI)))
	for j, n in enumerate(np.unique(Cortical_ROIs_CI)):
		tmp[j] = Thalamocortical_aveMat[Thalamus_voxel_positions[Thalamus_clusters==i],:][:,Cortical_ROI_positions[Cortical_ROIs_CI==n]].mean()

	Cluster_profile[i] = tmp	
	#print(Counter(Indiv_Subject_Thalamus_Winner_CIs[Thalamus_clusters ==i].flatten()))
	#print(Counter(stats.mode(Indiv_Subject_Thalamus_Winner_CIs[Thalamus_clusters ==i])[0][0]))
save_object(Cluster_profile, Parcel_path + '/31Cluster_profiles')


Thalamus_parcel_CI = np.zeros(len(Thalamus_voxels))
for i in np.unique(Thalamus_clusters):
	Thalamus_parcel_CI[Thalamus_clusters==i] = np.argmax(zscore(Cluster_profile[i]))

np.savetxt(Parcel_path + '/Thalamus_clusters_corticalCI', Thalamus_parcel_CI)

atlas_path = path_to_ROIs+'/Thalamus_indices.nii.gz' 
ROI_list = path_to_ROIs + '/thalamus_voxel_indices' 
image_path = Parcel_path + '/MGH_gordon_consensus_based_thalamus_parcels_corticalCIs.nii.gz' 
make_image(atlas_path, image_path, ROI_list, Thalamus_parcel_CI)



#### new profile summary dictionary

Cluster_profile_summary = {}

Cluster_profile_summary[26] = np.array([6])
Cluster_profile_summary[6] = np.array([5, 6])
Cluster_profile_summary[22] = np.array([5])
Cluster_profile_summary[19] = np.array([5])
Cluster_profile_summary[4] = np.array([5, 9])
Cluster_profile_summary[8] = np.array([5, 6])
Cluster_profile_summary[27] = np.array([5, 7])
Cluster_profile_summary[7] = np.array([5, 7])
Cluster_profile_summary[15] = np.array([5, 8])

Cluster_profile_summary[10] = np.array([2, 7])
Cluster_profile_summary[5] = np.array([2, 7])
Cluster_profile_summary[24] = np.array([2, 7])
Cluster_profile_summary[11] = np.array([2, 7])
Cluster_profile_summary[25] = np.array([2, 7])

Cluster_profile_summary[12] = np.array([2])
Cluster_profile_summary[31] = np.array([2])

Cluster_profile_summary[1] = np.array([2, 9])
Cluster_profile_summary[2] = np.array([2, 3])

Cluster_profile_summary[18] = np.array([3])
Cluster_profile_summary[9] = np.array([3])

Cluster_profile_summary[13] = np.array([3, 5, 8])
Cluster_profile_summary[16] = np.array([3, 5, 8])

Cluster_profile_summary[20] = np.array([2, 3, 4, 5, 7])
Cluster_profile_summary[28] = np.array([9, 4, 1])
Cluster_profile_summary[14] = np.array([9, 4, 2, 1])
Cluster_profile_summary[21] = np.array([9, 1])
Cluster_profile_summary[29] = np.array([9, 2, 1])
Cluster_profile_summary[30] = np.array([9, 4, 1])
Cluster_profile_summary[3] = np.array([9, 1, 3])

Cluster_profile_summary[17] = np.array([8, 2])
Cluster_profile_summary[23] = np.array([8, 6])




#### look at segmentation confidence
os.chdir(corrmat_path)
#files = glob.glob('MGH*MGH_Gordon_333_consensus_CI_pcorr_mat')
#seg_confidence = np.zeros(3539)
#for fn in files:
#	M = pickle.load(open(fn, "rb"))
#	seg_confidence += np.sort(M[10:,0:10])[:,-2:][:,0] / np.sort(M[10:,0:10])[:,-2:][:,1]

M = average_corrmat('MGH*MGH_Gordon_333_consensus_CI_pcorr_mat')
seg_confidence = np.sort(M[10:,0:10])[:,-2:][:,0] / np.sort(M[10:,0:10])[:,-2:][:,1]
#seg_confidence = seg_confidence/ len(files)
Thalamus_parcel_CI = np.loadtxt(Parcel_path + '/Thalamus_clusters_corticalCI')