from styxdefs import set_global_runner
from styxsingularity import SingularityRunner

# Initialize the SingularityRunner with your container images
runner = SingularityRunner(
    images={
        "antsx/ants:v2.5.3" : "./images/ants_v2.5.3.sif",
        "afni/afni_make_build:AFNI_24.2.06" : "./images/afni_24.2.06.sif"
    }
)

# Set the global runner for Styx
set_global_runner(runner)

# Now you can use any Styx functions as usual, and they will run in Singularity containers

from niwrap import ants, afni, fsl
from nilearn.plotting import plot_anat
from nodeblocks.anat_preproc import anat_init

input_image = "./data/sub-PA001_ses-V1W1_acq-MPR_rec-Norm_T1w.nii.gz"
template_path = "./ants_template/oasis/T_template0.nii.gz"
mask_path= "./ants_template/oasis/T_template0_BrainCerebellumProbabilityMask.nii.gz"
# niworkflows-ants registration mask (can be optional)
regmask_path = "./ants_template/oasis/T_template0_BrainCerebellumRegistrationMask.nii.gz"

from nipype import Workflow, Node, Function
# out = anat_init(input_image, 1)
# afni.v_3dinfo(dataset=[out])

wf = Workflow("anat_init")
anat_init = Node(Function(input_names=["input_image", "pipe_num"], output_names=["out"], function=anat_init), name="anat_init")
anat_init.inputs.input_image = input_image
anat_init.inputs.pipe_num = 1
wf.add_nodes([anat_init])
wf.run()

