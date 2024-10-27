# Description: This file contains the functions for the anatomical preprocessing of the input image.
from niwrap import afni, fsl, ants
import subprocess

def auto_mask(input_bold):
    out = afni.v_3d_automask(in_file=input_bold, apply_prefix="desc-brain_bold.nii.gz", prefix="desc-brain_mask_bold.nii.gz")
    return out

def average_bold(input_bold):
    out = afni.v_3d_tstat(mean=True, in_file=input_bold, prefix="desc-mean_sbref.nii.gz")
    return out

def motion_correction(input_bold, base_file):
    out = afni.v_3dvolreg(in_file=input_bold, 
                          twopass=True,
                          fourier=True,
                          zpad=4,
                          basefile=base_file,
                          prefix="desc-mc_bold.nii.gz",
                          maxdisp1d="desc-mc_maxdisp_bold.1D")
    return out