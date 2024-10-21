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

import os 
base = "/ocean/projects/med220004p/bshresth/projects/niwrap"
input_image = os.path.join(base,"data/neurocon/sub-control032014/anat/sub-control032014_T1w.nii.gz")

template_path = os.path.join(base,"oasis_data/MICCAI2012-Multi-Atlas-Challenge-Data/T_template0.nii.gz")
mask_path=os.path.join(base,"oasis_data/MICCAI2012-Multi-Atlas-Challenge-Data/T_template0_BrainCerebellumProbabilityMask.nii.gz")
regmask_path =os.path.join(base,"oasis_data/MICCAI2012-Multi-Atlas-Challenge-Data/T_template0_BrainCerebellumRegistrationMask.nii.gz")

# Test the anat_init function
def test_anat_init():
    from nodeblocks.anat_preproc import anat_init
    from niwrap import afni
    out = anat_init(input_image)
    assert "desc-preproc_T1w.nii.gz" in str(out.out_file)
    assert afni.v_3dinfo(dataset=[out.out_file], orient=True)

# Test the brain_mask_fsl function
def test_brain_mask_fsl():
    from nodeblocks.anat_preproc import brain_mask_fsl
    out = brain_mask_fsl(input_image)
    assert "bet" in str(out.outfile)

# Test the brain_mask_anats function
def test_brain_mask_ants():
    from nodeblocks.anat_preproc import brain_mask_ants
    out = brain_mask_ants(input_image, template_path, mask_path)
    assert "ants-brain" in str(out.brain_extracted_image)

# Test the brain_mask_afni function
# def test_brain_mask_afni():
#     out = brain_mask_afni(input_image)
#     assert "desc-brain_mask_T1w.nii.gz" in str(out)
#     assert afni.v_3dinfo(dataset=[out], orient=True)

# Test N4BiasFieldCorrection
def test_n4biasfieldcorrection():
    from nodeblocks.anat_preproc import n4biasfieldcorrection
    out = n4biasfieldcorrection(input_image)
    assert ".nii.gz" in str(out.corrected_image)

# Test fast
def test_fast():
    from nodeblocks.anat_preproc import fast
    out = fast(input_image)
    assert "segment" in str(out.restored_image)

# Test antsRegistration
def test_ants_registration():
    from nodeblocks.anat_preproc import ants_registration
    out = ants_registration(input_image, template_path, regmask_path)
    assert "Warped" in str(out.warped_image)

