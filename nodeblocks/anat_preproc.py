


"""
@nodeblock(
    name="anatomical_init",
    config=["anatomical_preproc"],
    switch=["run"],
    inputs=["T1w"],
    outputs=["desc-preproc_T1w", "desc-reorient_T1w", "desc-head_T1w"],
)
def anatomical_init(wf, cfg, strat_pool, pipe_num, opt=None):

    anat_deoblique = pe.Node(interface=afni.Refit(), name=f"anat_deoblique_{pipe_num}")
    anat_deoblique.inputs.deoblique = True

    node, out = strat_pool.get_data("T1w")
    wf.connect(node, out, anat_deoblique, "in_file")

    anat_reorient = pe.Node(
        interface=afni.Resample(),
        name=f"anat_reorient_{pipe_num}",
        mem_gb=0,
        mem_x=(0.0115, "in_file", "t"),
    )
    anat_reorient.inputs.orientation = "RPI"
    anat_reorient.inputs.outputtype = "NIFTI_GZ"

    wf.connect(anat_deoblique, "out_file", anat_reorient, "in_file")

    outputs = {
        "desc-preproc_T1w": (anat_reorient, "out_file"),
        "desc-reorient_T1w": (anat_reorient, "out_file"),
        "desc-head_T1w": (anat_reorient, "out_file"),
    }

    return (wf, outputs)

"""

from niwrap import afni

def anat_init(input_image, pipe_num):
    afni.v_3drefit(in_file=input_image, deoblique=True)
    out = afni.v_3dresample(in_file=input_image, orientation="RPI", prefix="desc-preproc_T1w.nii.gz")
    return out.out_file



