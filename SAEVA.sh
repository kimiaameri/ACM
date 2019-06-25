#!/bin/sh
#SBATCH --time=100:00:00   # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64gb     # Maximum memory required per CPU (in megabytes)
#SBATCH --job-name=SAVEA
#SBATCH --error=ACM.%J.err
#SBATCH --output=ACM.%J.out
####  Download reference genome    ####

export MINICONDA_HOME="~/miniconda3/envs/sanva/bin/"
export GITHUB_DIR=`pwd`

cd $WORK/
mkdir ACM_reference_genome
cd ACM_reference_genome
wget ftp://igenome:G3nom3s4u@ussd-ftp.illumina.com/Staphylococcus_aureus_NCTC_8325/NCBI/2006-02-13/Staphylococcus_aureus_NCTC_8325_NCBI_2006-02-13.tar.gz
tar -xzf Staphylococcus_aureus_NCTC_8325_NCBI_2006-02-13.tar.gz
rm Staphylococcus_aureus_NCTC_8325_NCBI_2006-02-13.tar.gz

module load R
cd $WORK
mkdir ACM-outputs
cd ACM-outputs
######## Input file #########
cd $WORK/ACM
Rscript inputFile.R $GITHUB_DIR/ACM-data $GITHUB_DIR/InputFiles.csv
######## Trimmomatic #########
## make trimmomatic directory
cd $WORK/ACM-outputs
mkdir trimmomatic
cd trimmomatic
mkdir trimlog
cd $WORK/ACM
#### for SANVA if there is no adapter
python3 pythonTrimmomaticNoadapter.py ./InputFiles.csv $MINICONDA_HOME $GITHUB_DIR
##### For SANVA if there is adapter
#python3 pythonTrimmomatic.py ../InputFiles.csv $MINICONDA_HOME $GITHUB_DIR

sh trimmomatic.sh > $WORK/SANVA-outputs/trimmomatic.log
########### BWA  ###############
cd $WORK/ACM-outputs
mkdir samfiles
cd $WORK/ACM
python3 pythonBwa.py ./InputFiles.csv $MINICONDA_HOME
sh bwa.sh
###########  BAM ##################
cd $WORK/ACM-outputs
mkdir bamfiles
mkdir flagsam
mkdir sortsam
mkdir depth
mkdir stats

cd $WORK/ACM/

#python3 pythonBam.py ./InputFiles.csv $SAMTools
python3 pythonBam.py ./InputFiles.csv $MINICONDA_HOME
sh bam.sh

###########  Picard ##################
cd $WORK/ACM-outputs
mkdir picard
cd picard
mkdir picardlog
cd $WORK/ACM/
#python3 pythonPicard.py ./InputFiles.csv $PICARD
python3 pythonPicard.py ./InputFiles.csv $MINICONDA_HOME

sh picard.sh
###########  Freebayes ##################
cd $WORK/ACM-outputs
mkdir freebayesoutput

cd $WORK/ACM/
#python3 pythonFreebayes.py ./InputFiles.csv $FREEBAYES
python3 pythonFreebayes.py ./InputFiles.csv $MINICONDA_HOME

sh freebayes.sh

########### Getting depth and qual for filtering ######
#python3 pythonFinddepth.py ./InputFiles.csv $SAMTools 
python3 pythonFinddepth.py ./InputFiles.csv $MINICONDA_HOME
sh findDepth.sh

Rscript depth.R $WORK/ACM-outputs/depth/ $WORK/ACM-outputs/freebayesoutput/ depth.txt quality.txt 
export DEPTH=$(( `cat depth.txt` * 1 ))
export QUALITY=$((`cat quality.txt` * 1 ))

###########  VCF-BCF ##################
cd $WORK/ACM-outputs
mkdir vcffilter-q
mkdir bcfoutput
mkdir vcffilter-q-dp
cd $WORK/ACM/
#python3 pythonBCF_VCF.py ./InputFiles.csv $BCFTools $QUALITY $DEPTH
python3 pythonBCF_VCF.py ./InputFiles.csv $MINICONDA_HOME $QUALITY $DEPTH

sh BCF-VCF.sh
###########  snpEFF Merge All Files ##################
cd $WORK/ACM/
#python3 pythonSnpEffMerge.py ./InputFiles.csv $BCFTools $MINICONDA_HOME $WORK/SANVA-outputs
python3 pythonSnpEffMerge.py ./InputFiles.csv $MINICONDA_HOME $WORK/ACM-outputs

sh snpEffMerge.sh


