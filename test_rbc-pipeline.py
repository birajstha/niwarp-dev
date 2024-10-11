from styxdefs import set_global_runner
from styxsingularity import SingularityRunner

# Initialize the SingularityRunner with your container images
runner = SingularityRunner(
    images={
        "antsx/ants:v2.5.3" : "./images/ants_v2.5.3.sif",
        "afni/afni_make_build:AFNI_24.2.06" : "./images/afni_24.2.06.sif"
    }
)

# Set the global runner for Styx
set_global_runner(runner)

# Now you can use any Styx functions as usual, and they will run in Singularity containers

from niwrap import ants, afni
from nilearn.plotting import plot_anat
import joblib

cache_dir = './cache'
memory = joblib.Memory(cache_dir, verbose=0)

input_image = "./data/sub-PA001_ses-V1W1_acq-MPR_rec-Norm_T1w.nii.gz"
template_path = "./ants_template/oasis/T_template0.nii.gz"
mask_path= "./ants_template/oasis/T_template0_BrainCerebellumProbabilityMask.nii.gz"
# niworkflows-ants registration mask (can be optional)
regmask_path = "./ants_template/oasis/T_template0_BrainCerebellumRegistrationMask.nii.gz"

out = ants.brain_extraction_sh(anatomical_image=input_image, 
                               template=template_path, 
                               probability_mask=mask_path, 
                               output_prefix="ants-brain",
                               runner=runner)

orientation = afni.v_3dinfo(dataset=[out.brain_extracted_image])

print(orientation)
# fig = plot_anat(out.brain_extracted_image, title="ants-brain-extraction", display_mode="ortho")
# fig.savefig('ants_extracted-brain.png')
# fig.close()

