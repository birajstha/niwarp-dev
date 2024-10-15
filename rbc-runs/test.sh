#!/usr/bin/bash
#SBATCH -N 1
#SBATCH -p RM-shared
#SBATCH -t 50:00:00
#SBATCH --ntasks-per-node=40

MED=/ocean/projects/med220004p
HOME=${MED}/bshresth
DATA=/ocean/projects/med220004p/jclucas/data/vannucci/bids_raw
#/ocean/projects/med220004p/jclucas/data/vannucci/bids_raw
# /ocean/projects/med220004p/kenneall/mock_data/regtest_outs/default/output/pipeline_cpac-default-pipeline
# /ocean/projects/med220004p/kenneall/mock_data/HBN_CBIC
OUTPUT=${HOME}/projects/niwrap/rbc-runs/output
IMAGE=${HOME}/code/images/cpac_nightly.sif

PIPELINE=/ocean/projects/med220004p/bshresth/projects/check_orientations/pipeline_config.yml

repo=/ocean/projects/med220004p/bshresth/projects/niwrap/C-PAC

# singularity run \
#     -B ${repo}/CPAC:/code/CPAC \
#     -B $MED \
#     -B $DATA:$DATA \
#     -B $OUTPUT:$OUTPUT $IMAGE $DATA $OUTPUT participant \
#     --num_ants_threads 5 \
#     --n_cpus 2 \
#     --mem_gb 15 \
#     --skip_bids_validator \
#     --preconfig rbc-options \
#     --participant_label sub-PA001

### For testing pipeline

singularity run \
    -B ${repo}/CPAC:/code/CPAC \
    -B $MED \
    -B $DATA:$DATA \
    -B $OUTPUT:$OUTPUT $IMAGE $DATA $OUTPUT test_config \
    --num_ants_threads 5 \
    --n_cpus 2 \
    --mem_gb 50 \
    --skip_bids_validator \
    --preconfig rbc-options \
    --participant_label sub-PA001
