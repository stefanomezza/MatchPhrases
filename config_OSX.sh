curl -O https://repo.continuum.io/miniconda/Miniconda3-latest-MacOSX-x86_64.sh && bash Miniconda3-latest-MacOSX-x86_64.sh && rm -rf Miniconda3-latest-MacOSX-x86_64.sh
conda create -n YourMD_task
source activate YourMD_task
while read -r line
do
	pip install $line
done < requirements.txt
