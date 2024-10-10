from styxdefs import set_global_runner
from styxsingularity import SingularityRunner

# Initialize the SingularityRunner with your container images
runner = SingularityRunner(
    images={
        "antsx/ants:v2.5.3" : "./images/ants_v2.5.3.sif"
    }
)

# Set the global runner for Styx
set_global_runner(runner)

# Now you can use any Styx functions as usual, and they will run in Singularity containers

from niwrap import ants
input_image = "./data/sub-PA001_ses-V1W1_acq-MPR_rec-Norm_T1w.nii.gz"
reference_image = "./data/sub-PA001_ses-V1W1_acq-MPR_rec-Norm_T1w.nii.gz"
output_image = "./output_image.nii.gz"
out = ants.brain_extraction_sh(anatomical_image=input_image, template=reference_image, probability_mask=output_image)
print(out)
