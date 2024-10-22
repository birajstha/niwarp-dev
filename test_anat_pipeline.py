########################################################################################
# Required by styx
########################################################################################
from styxdefs import set_global_runner
from styxsingularity import SingularityRunner

# Initialize the SingularityRunner with your container images
runner = SingularityRunner(
    images={
        "antsx/ants:v2.5.3" : "./images/ants_v2.5.3.sif",
        "afni/afni_make_build:AFNI_24.2.06" : "./images/afni_24.2.06.sif",
        "mcin/fsl:6.0.5": "./images/fsl_6.0.5.sif"
    }
)

# Set the global runner for Styx
set_global_runner(runner)


########################################################################################


import os
base = "/ocean/projects/med220004p/bshresth/projects/niwrap"
input_image = os.path.join(base,"data/neurocon/sub-control032014/anat/sub-control032014_T1w.nii.gz")

### Anat Init Block ###
from nodeblocks.anat_preproc import anat_init
resampled = anat_init(input_image)

### Skull Stripping Block ###
from nodeblocks.anat_preproc import brain_mask_fsl
skull_stripped = brain_mask_fsl(resampled.out_file)
skull_stripped_image = skull_stripped.outfile

# from nodeblocks.anat_preproc import brain_mask_ants
# template_path = os.path.join(base,"oasis_data/MICCAI2012-Multi-Atlas-Challenge-Data/T_template0.nii.gz")
# mask_path=os.path.join(base,"oasis_data/MICCAI2012-Multi-Atlas-Challenge-Data/T_template0_BrainCerebellumProbabilityMask.nii.gz")
# regmask_path =os.path.join(base,"oasis_data/MICCAI2012-Multi-Atlas-Challenge-Data/T_template0_BrainCerebellumRegistrationMask.nii.gz")
# skull_stripped = brain_mask_ants(input_image, template_path, mask_path)
# skull_stripped_image = skull_stripped.brain_extracted_image

### N4 Bias Field Correction Block ###
from nodeblocks.anat_preproc import n4biasfieldcorrection
out = n4biasfieldcorrection(skull_stripped_image)



### Plotting the results ###
from nilearn.plotting import plot_anat
fig = plot_anat(out.corrected_image, title="Preproc_T1w_bet", display_mode="ortho")
fig.savefig('preproc_T1w_bet.png')
fig.close()