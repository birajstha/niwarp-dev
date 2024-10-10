from styxdefs import set_global_runner
from styxsingularity import SingularityRunner

# Initialize the SingularityRunner with your container images
runner = SingularityRunner(
    images={
        "afni/afni_make_build:AFNI_24.2.06" : "./images/afni_24.2.06.sif"
    }
)

# Set the global runner for Styx
set_global_runner(runner)

# Now you can use any Styx functions as usual, and they will run in Singularity containers

from niwrap import afni

output = afni.v_3dinfo(dataset=["./data/sub-PA001_ses-V1W1_acq-MPR_rec-Norm_T1w.nii.gz"])

print(output)