if [ -z $WORK ]; then WORK=`pwd`; fi



#######   Download softwares    #######
cd $WORK
mkdir ACM-softwares
cd ACM-softwares/
####      Bioconda          ####
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
sh Miniconda3-latest-Linux-x86_64.sh
cd $WORK/ACM
conda env create -f sanva.environment.yaml
conda activate
conda activate sanva
