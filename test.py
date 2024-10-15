from styxdefs import set_global_runner
from styxsingularity import SingularityRunner

# Initialize the SingularityRunner with your container images
runner = SingularityRunner(
    images={
        "mcin/fsl:6.0.5": "./images/fsl_6.0.5.sif"
    }
)

# Set the global runner for Styx
set_global_runner(runner)

# Now you can use any Styx functions as usual, and they will run in Singularity containers

from niwrap import fsl
from nilearn.plotting import plot_anat

# bet_output = fsl.bet(
#     infile="./data/sub-PA001_ses-V1W1_acq-MPR_rec-Norm_T1w.nii.gz",
#     binary_mask=True,
#     runner=runner
# )


# fig = plot_anat(bet_output.outfile, title="BET output", display_mode="ortho")
# fig.savefig('bet_output.png')
# fig.close()

# fig = plot_anat("./data/sub-PA001_ses-V1W1_acq-MPR_rec-Norm_T1w.nii.gz", title="Original", display_mode="ortho")
# fig.savefig('original.png')
# fig.close()

# Test another function
out = fsl.fslinfo(filename="./data/sub-PA001_ses-V1W1_acq-MPR_rec-Norm_T1w.nii.gz")
print(out)
