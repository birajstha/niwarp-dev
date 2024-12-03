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

def flirt_registration(input_image, reference_image):
    """
    flirt -in /ocean/projects/med220004p/bshresth/projects/rbc-runs/output2/working/pipeline_RBCv0/cpac_pipeline_RBCv0_sub-PA001_ses-V1W1/_scan_facesmatching_run-1/extract_ref_brain_bold_104/uni_masked.nii.gz 
    -ref /ocean/projects/med220004p/bshresth/projects/rbc-runs/output2/working/pipeline_RBCv0/cpac_pipeline_RBCv0_sub-PA001_ses-V1W1/brain_extraction_36/sub-PA001_ses-V1W1_acq-MPR_rec-Norm_T1w_resample_calc.nii.gz 
    -out uni_masked_flirt.nii.gz 
    -omat uni_masked_flirt.mat 
    -cost corratio 
    -dof 6 
    -interp trilinear
    """
    out = fsl.flirt(in_file=input_image, 
                    reference=reference_image, 
                    out_file="desc-flirt.nii.gz",
                    out_matrix_file="desc-flirt.mat",
                    cost="corratio",
                    dof=6,
                    interp="trilinear")
    return out

def mcflirt_registration(input_image, reference_image):
    """
    mcflirt -in /ocean/projects/med220004p/bshresth/projects/rbc-runs/output2/working/pipeline_RBCv0/cpac_pipeline_RBCv0_sub-PA001_ses-V1W1/edit_func_81/_scan_facesmatching_run-1/func_drop_trs/sub-PA001_ses-V1W1_task-facesmatching_run-1_bold_resample_calc.nii.gz 
    -out /ocean/projects/med220004p/bshresth/projects/rbc-runs/output2/working/pipeline_RBCv0/cpac_pipeline_RBCv0_sub-PA001_ses-V1W1/_scan_facesmatching_run-1/func_motion_correct_mcflirt_87/sub-PA001_ses-V1W1_task-facesmatching_run-1_bold_resample_calc_mcf.nii.gz 
    -reffile /ocean/projects/med220004p/bshresth/projects/rbc-runs/output2/working/pipeline_RBCv0/cpac_pipeline_RBCv0_sub-PA001_ses-V1W1/_scan_facesmatching_run-1/func_get_fmriprep_ref_84/ref_bold.nii.gz 
    -mats 
    -plots 
    -rmsabs 
    -rmsrel
    """
    out = fsl.mcflirt(in_file=input_image, 
                      out_file="desc-mcflirt.nii.gz", 
                      ref_file=reference_image, 
                      save_mats=True, 
                      save_plots=True, 
                      save_rmsabs=True,
                      save_rmsrel=True)
    return out


def afni_3dcalc(input_image, reference_image):
    """
    3dcalc -a /ocean/projects/med220004p/bshresth/projects/rbc-runs/output2/working/pipeline_RBCv0/cpac_pipeline_RBCv0_sub-PA001_ses-V1W1/anat_reorient_0/sub-PA001_ses-V1W1_acq-MPR_rec-Norm_T1w_resample.nii.gz 
    -b /ocean/projects/med220004p/bshresth/projects/rbc-runs/output2/working/pipeline_RBCv0/cpac_pipeline_RBCv0_sub-PA001_ses-V1W1/anat_skullstrip_ants/atropos_wf/copy_xform/09_relabel_wm_mask_xform.nii.gz 
    -expr "a*step(b)" 
    -prefix sub-PA001_ses-V1W1_acq-MPR_rec-Norm_T1w_resample_calc.nii.gz
    """
    out = afni.v_3dcalc(in_file_a=input_image,  
                        in_file_b=reference_image,
                        expr=f"a*step(b)", 
                        prefix="desc-registered.nii.gz")
    return out

def afni_3dTproject(input_image, mask_image, ort_file, polort=0):
    """
    3dTproject  -input /ocean/projects/med220004p/bshresth/projects/rbc-runs/output2/working/pipeline_RBCv0/cpac_pipeline_RBCv0_sub-PA001_ses-V1W1/_scan_REST_run-1/func_despiked_template_212/vol0000_trans_merged_masked_despike.nii.gz 
                -mask /ocean/projects/med220004p/bshresth/projects/rbc-runs/output2/working/pipeline_RBCv0/cpac_pipeline_RBCv0_sub-PA001_ses-V1W1/_scan_REST_run-1/align_template_mask_to_template_data_space-template_reg-aCompCor_228/MNI152_T1_1mm_brain_mask_resample_resample.nii.gz 
                -ort /ocean/projects/med220004p/bshresth/projects/rbc-runs/output2/working/pipeline_RBCv0/cpac_pipeline_RBCv0_sub-PA001_ses-V1W1/nuisance_regressors_aCompCor_158/_scan_REST_run-1/build_nuisance_regressors/nuisance_regressors.1D 
                -polort 0 
                -prefix residuals.nii.gz
    """
    out = afni.v_3d_tproject(in_file= input_image,
                            mask= mask_image,
                            ort= ort_file,
                            polort= polort,
                            prefix="desc-residuals.nii.gz")
    return out

def afni_3dROIstats(input_image, mask_image):
    """
    3dROIstats -1Dformat 
    -mask /ocean/projects/med220004p/bshresth/projects/rbc-runs/output2/working/pipeline_RBCv0/cpac_pipeline_RBCv0_sub-PA001_ses-V1W1/nuisance_regressors_36_parameter_158/_scan_facesmatching_run-1/GlobalSignal_union_masks/ref_bold_corrected_brain_mask_maths_mask.nii.gz 
    /ocean/projects/med220004p/bshresth/projects/rbc-runs/output2/working/pipeline_RBCv0/cpac_pipeline_RBCv0_sub-PA001_ses-V1W1/func_slice_timing_correction_94/_scan_facesmatching_run-1/slice_timing/sub-PA001_ses-V1W1_task-facesmatching_run-1_bold_resample_calc_tshift.nii.gz 
    > sub-PA001_ses-V1W1_task-facesmatching_run-1_bold_resample_calc_tshift_roistat.1D
    """
    out = afni.v_3d_roistats(format1_d=True,
                            mask=mask_image,
                            in_file=input_image,
                            out_file="desc-roi_stats.1D")
    return out

def afni_3dTshift(input_image, tpattern, tr):
    """
    3dTshift -prefix sub-PA001_ses-V1W1_task-facesmatching_run-1_bold_resample_calc_tshift.nii.gz 
    -tpattern 
    @/ocean/projects/med220004p/bshresth/projects/rbc-runs/output2/working/pipeline_RBCv0/cpac_pipeline_RBCv0_sub-PA001_ses-V1W1/_scan_facesmatching_run-1/bold_scan_params_sub-PA001_ses-V1W1/tpattern.txt 
    -TR 0.8s 
    /ocean/projects/med220004p/bshresth/projects/rbc-runs/output2/working/pipeline_RBCv0/cpac_pipeline_RBCv0_sub-PA001_ses-V1W1/func_slice_timing_correction_94/_scan_facesmatching_run-1/slice_timing/sub-PA001_ses-V1W1_task-facesmatching_run-1_bold_resample_calc.nii.gz
    """
    out = afni.v_3d_tshift(in_file=input_image,
                            tpattern=tpattern,
                            tr=tr,
                            prefix="desc-tshift.nii.gz")
    return out

def fsl_fslmaths(inputs, operation):
    """
    fslmaths /ocean/projects/med220004p/bshresth/projects/rbc-runs/output2/working/pipeline_RBCv0/cpac_pipeline_RBCv0_sub-PA001_ses-V1W1/_scan_REST_run-1/skullstrip_first_pass_104/ref_bold_corrected_brain_mask.nii.gz 
    -mul /ocean/projects/med220004p/bshresth/projects/rbc-runs/output2/working/pipeline_RBCv0/cpac_pipeline_RBCv0_sub-PA001_ses-V1W1/_scan_REST_run-1/skullstrip_second_pass_104/uni_mask.nii.gz 
    -seed 77742777 
    /ocean/projects/med220004p/bshresth/projects/rbc-runs/output2/working/pipeline_RBCv0/cpac_pipeline_RBCv0_sub-PA001_ses-V1W1/_scan_REST_run-1/combine_masks_104/ref_bold_corrected_brain_mask_maths.nii.gz
    """
    out = fsl.fslmaths(input_files=inputs,
                        operations=operation,
                        output="desc-maths.nii.gz")
    return out

def afni_3dBlurToFWHM(input_image, mask_image, fwhm):
    """
    3dBlurToFWHM -FWHM 6.000000 
    -input /ocean/projects/med220004p/bshresth/projects/rbc-runs/output2/working/pipeline_RBCv0/cpac_pipeline_RBCv0_sub-PA001_ses-V1W1/reho_290/_scan_REST_run-1/reho_map/ReHo.nii.gz 
    -mask /ocean/projects/med220004p/bshresth/projects/rbc-runs/output2/working/pipeline_RBCv0/cpac_pipeline_RBCv0_sub-PA001_ses-V1W1/_scan_REST_run-1/applyxfm_deriv_mask_to_standard_190/ref_bold_corrected_brain_mask_maths_trans.nii.gz 
    -prefix ReHo_afni.nii.gz

    another one
    3dBlurToFWHM -FWHM 6.000000 
    -input /ocean/projects/med220004p/rupprech/ecpac_runs/base_rbc-2/rbc-options/sub-NDARINV2VY7YYNW/wd/pipeline_RBCv0/cpac_sub-NDARINV2VY7YYNW_ses-baselineYear1Arm1/reho_289/_scan_rest_run-01/reho_map/ReHo.nii.gz 
    -mask /ocean/projects/med220004p/rupprech/ecpac_runs/base_rbc-2/rbc-options/sub-NDARINV2VY7YYNW/wd/pipeline_RBCv0/cpac_sub-NDARINV2VY7YYNW_ses-baselineYear1Arm1/_scan_rest_run-01/applyxfm_deriv_mask_to_standard_189/ref_bold_corrected_brain_mask_maths_trans.nii.gz 
    -prefix ReHo_afni.nii.gz
    """
    out = afni.v_3d_blur_to_fwhm(fwhm=fwhm,
                            in_file=input_image,
                            mask=mask_image,
                            prefix="desc-ReHo.nii.gz")
    return out


def fsl_fslstats(input_image, mask_image):
    """
    fslstats /ocean/projects/med220004p/bshresth/projects/rbc-runs/output2/working/pipeline_RBCv0/cpac_pipeline_RBCv0_sub-PA001_ses-V1W1/reho_290/_scan_REST_run-1/reho_map/ReHo.nii.gz 
    -k /ocean/projects/med220004p/bshresth/projects/rbc-runs/output2/working/pipeline_RBCv0/cpac_pipeline_RBCv0_sub-PA001_ses-V1W1/_scan_REST_run-1/applyxfm_deriv_mask_to_standard_190/ref_bold_corrected_brain_mask_maths_trans.nii.gz 
    -m 

    another one
    fslstats /ocean/projects/med220004p/rupprech/ecpac_runs/base_rbc-2/rbc-options/sub-NDARINV2VY7YYNW/wd/pipeline_RBCv0/cpac_sub-NDARINV2VY7YYNW_ses-baselineYear1Arm1/space-template_lfcdw_smooth_AFNI_303/_scan_rest_run-01/_fwhm_6/smooth/local_functional_connectivity_density_Weighted_afni.nii.gz 
    -k /ocean/projects/med220004p/bshresth/projects/niwrap-dev/cpac_templates/Mask_ABIDE_85Percent_GM.nii.gz 
    -s 
    """
    out = fsl.fslstats(input_file=input_image,
                        index_mask=mask_image,
                        std_dev_flag=True)
    return out

def afni_3dDespike(input_image):
    """
    3dDespike -prefix vol0000_trans_merged_masked_despike.nii.gz 
    /ocean/projects/med220004p/rupprech/ecpac_runs/base_rbc-2/rbc-options/sub-NDARINV2VY7YYNW/wd/pipeline_RBCv0/cpac_sub-NDARINV2VY7YYNW_ses-baselineYear1Arm1/_scan_rest_run-01/func_despiked_template_211/vol0000_trans_merged_masked.nii.gz
    """
    out = afni.v_3d_despike(prefix="desc-despike.nii.gz", in_file=input_image)
    return out

def fsl_convert_xfm(input_file):
    """
    convert_xfm -omat /ocean/projects/med220004p/bshresth/projects/rbc-runs/output2/working/pipeline_RBCv0/cpac_pipeline_RBCv0_sub-PA001_ses-V1W1/_scan_REST_run-1/anat_to_func_linear_xfm_aCompCor_158/uni_masked_flirt_inv.mat 
    -inverse 
    /ocean/projects/med220004p/bshresth/projects/rbc-runs/output2/working/pipeline_RBCv0/cpac_pipeline_RBCv0_sub-PA001_ses-V1W1/func_to_anat_bbreg_132/_scan_REST_run-1/bbreg_func_to_anat/uni_masked_flirt.mat
    """
    out = fsl.convert_xfm(out_file="desc-flirt_inv.mat", invert_xfm=True, in_file=input_file)
    return out

def afni_3dBandpass(highpass, lowpass, input_image):
    """
    3dBandpass -prefix residual_filtered.nii.gz 
    0.010000 
    0.100000 
    /ocean/projects/med220004p/bshresth/projects/rbc-runs/output2/working/pipeline_RBCv0/cpac_pipeline_RBCv0_sub-PA001_ses-V1W1/alff_falff_264/_scan_REST_run-1/_hp_0.01/_lp_0.1/bandpass_filtering/residuals.nii.gz
    """
    out = afni.v_3d_bandpass(prefix="desc-residual_filtered.nii.gz", lowpass=lowpass, highpass=highpass, in_file=input_image)
    return out

def fsl_fslmerge(input_files: list):
    """
    fslmerge -t vol0000_trans_merged.nii.gz 
    ../applyxfm_derivfunc_to_standard_189_/mapflow/_applyxfm_derivfunc_to_standard_189_1/vol0001_trans.nii.gz 
    ../applyxfm_derivfunc_to_standard_189_/mapflow/_applyxfm_derivfunc_to_standard_189_2/vol0002_trans.nii.gz
    """
    out = fsl.fslmerge(merge_time = True, output_file="desc-merged.nii.gz", input_files=input_files)
    return out    

def afni_3dUnifize(cl_frac, rbt, input_image):
    """
    3dUnifize -clfrac 0.2 
    -rbt 18.3 65.0 90.0 
    -prefix uni.nii.gz 
    -T2 
    -input /ocean/projects/med220004p/bshresth/projects/rbc-runs/output2/working/pipeline_RBCv0/cpac_pipeline_RBCv0_sub-PA001_ses-V1W1/_scan_REST_run-1/unifize_104/ref_bold_corrected_brain_masked.nii.gz
    """
    out = afni.v_3d_unifize(cl_frac=cl_frac, rbt=rbt, prefix="desc-uni.nii.gz", t2=True, in_file=input_image)
    return out