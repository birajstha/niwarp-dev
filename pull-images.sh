singularity cache clean

mkdir -p ./images

# fsl:6.0.5
singularity pull --dir ./images docker://mcin/fsl:6.0.5

# ants:2.5.3
singularity pull --dir ./images docker://antsx/ants:v2.5.3

# afni:AFNI_24.2.06
singularity pull --dir ./images/ docker://afni/afni_make_build:AFNI_24.2.06