########################################################################################
# Required by styx
########################################################################################
from styxdefs import set_global_runner, DummyRunner
from styxsingularity import SingularityRunner

import os

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

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# input_bold = os.path.join(base,"data/neurocon/sub-control032014/func/sub-control032014_task-resting_run-1_bold.nii.gz")

# from nodeblocks.func_preproc import auto_mask
# skull_stripped = auto_mask(input_bold)

from nodeblocks.func_preproc import average_bold
# average = average_bold(skull_stripped.brain_file)

# from nodeblocks.func_preproc import motion_correction
# mc = motion_correction(skull_stripped.brain_file, average.out_file)

# mean = average_bold(mc.out_file)
from nilearn.plotting import plot_anat
# fig = plot_anat(mean.out_file, title="desc-brain_mask_bold", display_mode="ortho")
# fig.savefig('desc-brain_mask_bold.png')

# from nodeblocks.func_preproc import afni_3dcalc
# out = afni_3dcalc(
#     input_image="/ocean/projects/med220004p/bshresth/projects/rbc-runs/output2/working/pipeline_RBCv0/cpac_pipeline_RBCv0_sub-PA001_ses-V1W1/anat_reorient_0/sub-PA001_ses-V1W1_acq-MPR_rec-Norm_T1w_resample.nii.gz", 
#     reference_image="/ocean/projects/med220004p/bshresth/projects/rbc-runs/output2/working/pipeline_RBCv0/cpac_pipeline_RBCv0_sub-PA001_ses-V1W1/anat_skullstrip_ants/atropos_wf/copy_xform/09_relabel_wm_mask_xform.nii.gz"
#     )
# fig = plot_anat(out.out_file, title="desc-registered", display_mode="ortho")
# fig.savefig('desc-registered.png')

# from nodeblocks.func_preproc import mcflirt_registration
# out = mcflirt_registration(
#     input_image="/ocean/projects/med220004p/bshresth/projects/rbc-runs/output2/working/pipeline_RBCv0/cpac_pipeline_RBCv0_sub-PA001_ses-V1W1/edit_func_81/_scan_facesmatching_run-1/func_drop_trs/sub-PA001_ses-V1W1_task-facesmatching_run-1_bold_resample_calc.nii.gz", 
#     reference_image="/ocean/projects/med220004p/bshresth/projects/rbc-runs/output2/working/pipeline_RBCv0/cpac_pipeline_RBCv0_sub-PA001_ses-V1W1/_scan_facesmatching_run-1/func_get_fmriprep_ref_84/ref_bold.nii.gz"
#     )

# from nodeblocks.func_preproc import flirt_registration
# out = flirt_registration(
#     input_image="/ocean/projects/med220004p/bshresth/projects/rbc-runs/output2/working/pipeline_RBCv0/cpac_pipeline_RBCv0_sub-PA001_ses-V1W1/brain_extraction_36/sub-PA001_ses-V1W1_acq-MPR_rec-Norm_T1w_resample_calc.nii.gz", 
#     reference_image="/ocean/projects/med220004p/bshresth/projects/rbc-runs/output2/working/pipeline_RBCv0/cpac_pipeline_RBCv0_sub-PA001_ses-V1W1/anat_reorient_0/sub-PA001_ses-V1W1_acq-MPR_rec-Norm_T1w_resample.nii.gz"
#     )


# from nodeblocks.func_preproc import afni_3dTproject
# out = afni_3dTproject(input_image = "/ocean/projects/med220004p/bshresth/projects/rbc-runs/output2/working/pipeline_RBCv0/cpac_pipeline_RBCv0_sub-PA001_ses-V1W1/_scan_REST_run-1/func_despiked_template_212/vol0000_trans_merged_masked_despike.nii.gz", 
#                        mask_image = "/ocean/projects/med220004p/bshresth/projects/rbc-runs/output2/working/pipeline_RBCv0/cpac_pipeline_RBCv0_sub-PA001_ses-V1W1/_scan_REST_run-1/align_template_mask_to_template_data_space-template_reg-aCompCor_228/MNI152_T1_1mm_brain_mask_resample_resample.nii.gz",
#                        ort_file = "/ocean/projects/med220004p/bshresth/projects/rbc-runs/output2/working/pipeline_RBCv0/cpac_pipeline_RBCv0_sub-PA001_ses-V1W1/nuisance_regressors_aCompCor_158/_scan_REST_run-1/build_nuisance_regressors/nuisance_regressors.1D"
#                        )


from nodeblocks.func_preproc import afni_3dROIstats
out = afni_3dROIstats(
    input_image="/ocean/projects/med220004p/bshresth/projects/rbc-runs/output2/working/pipeline_RBCv0/cpac_pipeline_RBCv0_sub-PA001_ses-V1W1/func_slice_timing_correction_94/_scan_facesmatching_run-1/slice_timing/sub-PA001_ses-V1W1_task-facesmatching_run-1_bold_resample_calc_tshift.nii.gz",
    mask_image= "/ocean/projects/med220004p/bshresth/projects/rbc-runs/output2/working/pipeline_RBCv0/cpac_pipeline_RBCv0_sub-PA001_ses-V1W1/nuisance_regressors_36_parameter_158/_scan_facesmatching_run-1/GlobalSignal_union_masks/ref_bold_corrected_brain_mask_maths_mask.nii.gz"
)

fig = plot_anat(average_bold(out.out_file).out_file, title="desc-mcflirt", display_mode="ortho")
fig.savefig('desc-mcflirt.png')

