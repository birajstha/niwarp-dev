#!/bin/bash
#SBATCH --mem=30G
#SBATCH -N 1
#SBATCH -p RM-shared
#SBATCH -t 60:00:00
#SBATCH --ntasks-per-node=20

MED="/ocean/projects/med220004p"
HOME="/ocean/projects/med220004p/bshresth"
DATA="/ocean/projects/med220004p/jclucas/data/vannucci/bids_raw"
OUTPUT="/ocean/projects/med220004p/bshresth/vannucci/all_runs/scripts/outputs/ANTS_FSL_noBBR_strict"
IMAGE="/ocean/projects/med220004p/bshresth/projects/niwrap/images/cpac_nightly.sif"
PIPELINE="/ocean/projects/med220004p/bshresth/vannucci/all_runs/configs/ANTS_FSL_noBBR_strict.yml"
PARTICIPANT="sub-PA001"

apptainer exec \
    -B /ocean/projects/med220004p/bshresth/code/C-PAC/CPAC:/code/CPAC \
    --bind /ocean/projects/med220004p/bshresth:/ocean/projects/med220004p/bshresth \
    $IMAGE \
    /bin/bash