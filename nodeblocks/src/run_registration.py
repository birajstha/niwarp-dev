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


from niwrap import afni, fsl, ants

def antsRegistration():
    """
    antsRegistration    --random-seed 77742777 
                        --collapse-output-transforms 1 
                        --dimensionality 3 
                        --initial-moving-transform [/ocean/projects/med220004p/bshresth/projects/rbc-runs/output2/working/pipeline_RBCv0/cpac_pipeline_RBCv0_sub-PA001_ses-V1W1/resampled_T1w-brain-template/T1w-brain-template/MNI152_T1_1mm_brain_resample.nii.gz,/ocean/projects/med220004p/bshresth/projects/rbc-runs/output2/working/pipeline_RBCv0/cpac_pipeline_RBCv0_sub-PA001_ses-V1W1/brain_extraction_36/sub-PA001_ses-V1W1_acq-MPR_rec-Norm_T1w_resample_calc.nii.gz,0] 
                        --transform Rigid[0.05] 
                        --metric MI[/ocean/projects/med220004p/bshresth/projects/rbc-runs/output2/working/pipeline_RBCv0/cpac_pipeline_RBCv0_sub-PA001_ses-V1W1/resampled_T1w-brain-template/T1w-brain-template/MNI152_T1_1mm_brain_resample.nii.gz,/ocean/projects/med220004p/bshresth/projects/rbc-runs/output2/working/pipeline_RBCv0/cpac_pipeline_RBCv0_sub-PA001_ses-V1W1/brain_extraction_36/sub-PA001_ses-V1W1_acq-MPR_rec-Norm_T1w_resample_calc.nii.gz,1,32,Regular,0.25] 
                        --convergence [100x100,1e-06,20] 
                        --smoothing-sigmas 2.0x1.0vox 
                        --shrink-factors 2x1 
                        --use-histogram-matching 1 
                        --transform Affine[0.08] 
                        --metric MI[/ocean/projects/med220004p/bshresth/projects/rbc-runs/output2/working/pipeline_RBCv0/cpac_pipeline_RBCv0_sub-PA001_ses-V1W1/resampled_T1w-brain-template/T1w-brain-template/MNI152_T1_1mm_brain_resample.nii.gz,/ocean/projects/med220004p/bshresth/projects/rbc-runs/output2/working/pipeline_RBCv0/cpac_pipeline_RBCv0_sub-PA001_ses-V1W1/brain_extraction_36/sub-PA001_ses-V1W1_acq-MPR_rec-Norm_T1w_resample_calc.nii.gz,1,32,Regular,0.25] 
                        --convergence [100x100,1e-06,20] 
                        --smoothing-sigmas 1.0x0.0vox 
                        --shrink-factors 2x1 
                        --use-histogram-matching 1 
                        --transform SyN[0.1,3.0,0.0] 
                        --metric CC[/ocean/projects/med220004p/bshresth/projects/rbc-runs/output2/working/pipeline_RBCv0/cpac_pipeline_RBCv0_sub-PA001_ses-V1W1/resampled_T1w-brain-template/T1w-brain-template/MNI152_T1_1mm_brain_resample.nii.gz,/ocean/projects/med220004p/bshresth/projects/rbc-runs/output2/working/pipeline_RBCv0/cpac_pipeline_RBCv0_sub-PA001_ses-V1W1/brain_extraction_36/sub-PA001_ses-V1W1_acq-MPR_rec-Norm_T1w_resample_calc.nii.gz,1,4] 
                        --convergence [100x70x50x20,1e-06,10] 
                        --smoothing-sigmas 3.0x2.0x1.0x0.0vox 
                        --shrink-factors 8x4x2x1 
                        --use-histogram-matching 1 
                        --winsorize-image-intensities [0.005,0.995] 
                        --interpolation LanczosWindowedSinc 
                        --output [transform,transform_Warped.nii.gz]
    """
    out = ants.antsRegistration(random_seed=77742777,
                                collapse_output_transforms=1,
                                dimensionality=3,
                                initial_moving_transform=["/ocean/projects/med220004p/bshresth/projects/rbc-runs/output2/working/pipeline_RBCv0/cpac_pipeline_RBCv0_sub-PA001_ses-V1W1/resampled_T1w-brain-template/T1w-brain-template/MNI152_T1_1mm_brain_resample.nii.gz", "/ocean/projects/med220004p/bshresth/projects/rbc-runs/output2/working/pipeline_RBCv0/cpac_pipeline_RBCv0_sub-PA001_ses-V1W1/brain_extraction_36/sub-PA001_ses-V1W1_acq-MPR_rec-Norm_T1w_resample_calc.nii.gz", "0"],
                                transform="Rigid[0.05]",
                                metric="MIMI[/ocean/projects/med220004p/bshresth/projects/rbc-runs/output2/working/pipeline_RBCv0/cpac_pipeline_RBCv0_sub-PA001_ses-V1W1/resampled_T1w-brain-template/T1w-brain-template/MNI152_T1_1mm_brain_resample.nii.gz,/ocean/projects/med220004p/bshresth/projects/rbc-runs/output2/working/pipeline_RBCv0/cpac_pipeline_RBCv0_sub-PA001_ses-V1W1/brain_extraction_36/sub-PA001_ses-V1W1_acq-MPR_rec-Norm_T1w_resample_calc.nii.gz,1,32,Regular,0.25] ",
                                convergence="[100x100,1e-06,20]",
                                smoothing_sigmas="2.0x1.0vox",
                                shrink_factors="2x1",
                                use_histogram_matching=1,
                                transform="Affine[0.08]",
                                metric="CC/ocean/projects/med220004p/bshresth/projects/rbc-runs/output2/working/pipeline_RBCv0/cpac_pipeline_RBCv0_sub-PA001_ses-V1W1/resampled_T1w-brain-template/T1w-brain-template/MNI152_T1_1mm_brain_resample.nii.gz,/ocean/projects/med220004p/bshresth/projects/rbc-runs/output2/working/pipeline_RBCv0/cpac_pipeline_RBCv0_sub-PA001_ses-V1W1/brain_extraction_36/sub-PA001_ses-V1W1_acq-MPR_rec-Norm_T1w_resample_calc.nii.gz,1,4] ",