########################################################################################
# Required by styx
########################################################################################
from styxdefs import set_global_runner
from styxsingularity import SingularityRunner

# Initialize the SingularityRunner with your container images
base = "/ocean/projects/med220004p/bshresth/projects/niwrap-dev"
runner = SingularityRunner(
    images={
        "antsx/ants:v2.5.3" : f"{base}/images/ants_v2.5.3.sif",
        "afni/afni_make_build:AFNI_24.2.06" : f"{base}/images/afni_make_build_AFNI_24.2.06.sif",
        "brainlife/fsl:6.0.4-patched2": f"{base}/images/fsl_6.0.4-patched2.sif"
    }
)


# Set the global runner for Styx
set_global_runner(runner)


########################################################################################


import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


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
anat_preproc = n4biasfieldcorrection(skull_stripped_image)


input_bold = os.path.join(base,"data/neurocon/sub-control032014/func/sub-control032014_task-resting_run-1_bold.nii.gz")

from nodeblocks.func_preproc import auto_mask
skull_stripped = auto_mask(input_bold)

from nodeblocks.func_preproc import average_bold
average = average_bold(skull_stripped.brain_file)

from nodeblocks.func_preproc import motion_correction
mc = motion_correction(skull_stripped.brain_file, average.out_file)

mean = average_bold(mc.out_file)

from nilearn.plotting import plot_anat
fig = plot_anat(mean.out_file, title="desc-brain_mask_bold", display_mode="ortho")
fig.savefig('desc-brain_mask_bold.png')