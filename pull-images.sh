singularity cache clean

mkdir -p ./images

# fsl:6.0.5
singularity pull --dir ./images docker://mcin/fsl:6.0.5

# ants:2.5.3
singularity pull --dir ./images docker://antsx/ants:v2.5.3

# afni:AFNI_24.2.06
singularity pull --dir ./images docker://afni/afni_make_build:AFNI_24.2.06


# pull the test images
mkdir -p ./data
wget -P ./data https://fcp-indi.s3.amazonaws.com/data/Projects/INDI/umf_pd/neurocon.tar.gz

#untar the test images
tar -xvzf ./data/neurocon.tar.gz -C ./data
rm ./data/neurocon.tar.gz

# pull oasis images
mkdir -p ./oasis_data
wget  -P ./oasis_data https://figshare.com/ndownloader/files/3133832
# unzip
unzip ./oasis_data/3133832 -d ./oasis_data
rm ./oasis_data/3133832

singularity cache clean