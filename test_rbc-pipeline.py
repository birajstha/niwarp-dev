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

# Now you can use any Styx functions as usual, and they will run in Singularity containers

from niwrap import ants, afni, fsl
from nilearn.plotting import plot_anat
import os , sys
from nodeblocks.anat_preproc import anat_init, brain_mask_fsl, brain_mask_afni, brain_mask_ants
import pytest
import subprocess

base = "/ocean/projects/med220004p/bshresth/projects/niwrap"
input_image = os.path.join(base,"data/sub-PA001_ses-V1W1_acq-MPR_rec-Norm_T1w.nii.gz")
template_path = os.path.join(base,"ants_template/oasis/T_template0.nii.gz")
mask_path=os.path.join(base,"ants_template/oasis/T_template0_BrainCerebellumProbabilityMask.nii.gz")
regmask_path =os.path.join(base,"ants_template/oasis/T_template0_BrainCerebellumRegistrationMask.nii.gz")

# Test the anat_init function
def test_anat_init():
    out = anat_init(input_image)
    assert "desc-preproc_T1w.nii.gz" in str(out)
    assert afni.v_3dinfo(dataset=[out], orient=True)

# Test the brain_mask_fsl function
def test_brain_mask_fsl():
    out = brain_mask_fsl(input_image)
    assert "bet" in str(out)

# Test the brain_mask_anats function
def test_brain_mask_ants():
    out = brain_mask_ants(input_image, template_path, mask_path)
    assert "ants-brain" in str(out.brain_extracted_image)

# Test the brain_mask_afni function
# def test_brain_mask_afni():
#     out = brain_mask_afni(input_image)
#     assert "desc-brain_mask_T1w.nii.gz" in str(out)
#     assert afni.v_3dinfo(dataset=[out], orient=True)

