# Description: This file contains the functions for the anatomical preprocessing of the input image.
from niwrap import afni, fsl, ants
import subprocess

def anat_init(input_image, orientation="RPI"):
    #make a copy of input image and deoblique it
    subprocess.run(["cp", input_image, "T1w.nii.gz"])
    afni.v_3drefit(in_file="T1w.nii.gz", deoblique=True)
    out = afni.v_3dresample(in_file=input_image, orientation=orientation, prefix="desc-preproc_T1w.nii.gz")
    return out

def brain_mask_fsl(input_image):
    out = fsl.bet(infile=input_image, binary_mask=True, )
    return out

def brain_mask_ants(input_image, template_path, mask_path):
    out = ants.brain_extraction_sh(anatomical_image=input_image,
                                   template= template_path,
                                   probability_mask=mask_path,
                                   output_prefix="ants-brain")
    return out

# This is not complete yet...
# def brain_mask_afni(input_image):
#     out = afni.v_3d_skull_strip(in_file=input_image)
#     return out

"""N4BiasFieldCorrection -d 3 
    --input-image sub-PA001_ses-V1W1_acq-MPR_rec-Norm_T1w_resample.nii.gz 
    --output sub-PA001_ses-V1W1_acq-MPR_rec-Norm_T1w_resample_corrected.nii.gz 
    --shrink-factor 2
"""
def n4biasfieldcorrection(input_image):
    out = ants.n4_bias_field_correction(input_image=input_image, 
                                        corrected_image_path="corrected.nii.gz",
                                        image_dimensionality=3, 
                                        shrink_factor=2,
                                        bias_field_path="bias.nii.gz",
                                     )
    return out

"""
fast -t 1 -o segment -p -g -S 1 sub-PA001_ses-V1W1_acq-MPR_rec-Norm_T1w_resample_calc.nii.gz
"""
def fast(input_image):
    out = fsl.fast(in_files=[input_image], 
                   out_basename="segment",
                   channels=1,
                   segments=True,
                   img_type=1
                   )
    return out

"""
antsRegistration \
    --collapse-output-transforms 0 \
    --dimensionality 3 \
    --initial-moving-transform [MNI152_T1_2mm_brain.nii.gz,sub-colornest073_ses-1_rec-refaced_desc-brain_T1w.nii.gz,0] \
    --transform Rigid[0.1] \
    --metric MI[MNI152_T1_2mm_brain.nii.gz,sub-colornest073_ses-1_rec-refaced_desc-brain_T1w.nii.gz,1,32,Regular,0.25] \
    --convergence [1000x500x250x100,1e-08,10] \
    --smoothing-sigmas 3.0x2.0x1.0x0.0 \
    --shrink-factors 8x4x2x1 \
    --use-histogram-matching 1 \
    --transform Affine[0.1] \
    --metric MI[MNI152_T1_2mm_brain.nii.gz,sub-colornest073_ses-1_rec-refaced_desc-brain_T1w.nii.gz,1,32,Regular,0.25] \
    --convergence [1000x500x250x100,1e-08,10] \
    --smoothing-sigmas 3.0x2.0x1.0x0.0 \
    --shrink-factors 8x4x2x1 \
    --use-histogram-matching 1 \
    --transform SyN[0.1,3.0,0.0] \
    --metric CC[MNI152_T1_2mm.nii.gz,sub-colornest073_ses-1_rec-refaced_T1w.nii.gz,1,4] \
    --convergence [100x100x70x20,1e-09,15] \
    --smoothing-sigmas 3.0x2.0x1.0x0.0 \
    --shrink-factors 6x4x2x1 \
    --use-histogram-matching 1 \
    --winsorize-image-intensities [0.01,0.99] \
    --interpolation LanczosWindowedSinc \
    --output [transform,transform_Warped.nii.gz]
"""
def ants_registration(input_image, template_path):
    out = ants.registration(collapse_output_transforms=0,
                            dimensionality=3,
                            initial_moving_transform=[template_path, input_image, 0],
                            transform=["Rigid[0.1]", "Affine[0.1]", "SyN[0.1,3.0,0.0]"],
                            metric=["MI", "MI", "CC"],
                            convergence=[[1000,500,250,100,1e-08,10], [1000,500,250,100,1e-08,10], [100,100,70,20,1e-09,15]],
                            smoothing_sigmas=["3.0x2.0x1.0x0.0", "3.0x2.0x1.0x0.0", "3.0x2.0x1.0x0.0"],
                            shrink_factors=["8x4x2x1", "8x4x2x1", "6x4x2x1"],
                            use_histogram_matching=1,
                            winsorize_image_intensities=[0.01,0.99],
                            interpolation="LanczosWindowedSinc",
                            output=["transform", "transform_Warped.nii.gz"]
                            )
    return out