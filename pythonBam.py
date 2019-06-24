import csv
import sys

if len(sys.argv) < 3:
    sys.stderr.write('No Input CSV file and samtools\n')
    sys.exit(0)
    
inputFile = sys.argv[1]
minicondaBin = sys.argv[2]
outputFile = "bam.sh"
with open(outputFile,'w') as outFile:
    count=0
    with open(inputFile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if count !=0 :
               outFile.write(f'{minicondaBin}/samtools view -bt $WORK/ACM_reference_genome/Staphylococcus_aureus_NCTC_8325/NCBI/2006-02-13/Sequence/BWAIndex/genome.fa $WORK/ACM-outputs/samfiles/{row[0]}.sam >$WORK/ACM-outputs/bamfiles/{row[0]}.bam\n')
               outFile.write(f'{minicondaBin}/samtools flagstat $WORK/ACM-outputs/bamfiles/{row[0]}.bam > $WORK/ACM-outputs/flagsam/{row[0]}.flagstat.log\n')
               outFile.write(f'{minicondaBin}/samtools sort $WORK/ACM-outputs/bamfiles/{row[0]}.bam -O bam -o $WORK/ACM-outputs/sortsam/{row[0]}.sorted.bam\n')
               outFile.write(f'{minicondaBin}/samtools stats $WORK/ACM-outputs/sortsam/{row[0]}.sorted.bam >$WORK/ACM-outputs/stats/{row[0]}.txt \n')

            count =count +1
 
