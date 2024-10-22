########################################################################################
# Required by styx
########################################################################################
from styxdefs import set_global_runner
from styxsingularity import SingularityRunner

# Initialize the SingularityRunner with your container images
runner = SingularityRunner(
    images={
        "antsx/ants:v2.5.3" : "./images/ants_v2.5.3.sif",
        "afni/afni_make_build:AFNI_24.2.06" : "./images/afni_24.2.06.sif",
        "mcin/fsl:6.0.5": "./images/fsl_6.0.5.sif"
    }
)

# Set the global runner for Styx
set_global_runner(runner)


########################################################################################

import os
base = "/ocean/projects/med220004p/bshresth/projects/niwrap"
input_bold = os.path.join(base,"data/neurocon/sub-control032014/func/sub-control032014_task-resting_run-1_bold.nii.gz")


from nodeblocks.func_preproc import auto_mask
skull_stripped = auto_mask(input_bold)

from nodeblocks.func_preproc import average_bold
average = average_bold(skull_stripped.brain_file)

from nilearn.plotting import plot_anat
fig = plot_anat(average.out_file, title="desc-brain_mask_bold", display_mode="ortho")
fig.savefig('desc-brain_mask_bold.png')
