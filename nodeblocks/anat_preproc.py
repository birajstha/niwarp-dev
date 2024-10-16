# Description: This file contains the functions for the anatomical preprocessing of the input image.
from niwrap import afni, fsl, ants

def anat_init(input_image):
    afni.v_3drefit(in_file=input_image, deoblique=True)
    out = afni.v_3dresample(in_file=input_image, orientation="RPI", prefix="desc-preproc_T1w.nii.gz")
    return out.out_file


def brain_mask_afni(input_image):
    out = afni.v_3d_skull_strip(in_file=input_image)
    return out.out_file

def brain_mask_fsl(input_image):
    out = fsl.bet(infile=input_image, binary_mask=True)
    return out.outfile

def brain_mask_ants(input_image, template_path, mask_path):
    out = ants.brain_extraction_sh(anatomical_image=input_image,
                                   template= template_path,
                                   probability_mask=mask_path,
                                   output_prefix="ants-brain")
    return out