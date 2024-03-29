import csv
import sys

if len(sys.argv) < 4:
    sys.stderr.write('No Input CSV file and genomebed\n')
    sys.exit(0)
    
inputFile = sys.argv[1]
genomeBedpath = sys.argv[2]
minicondaBin = sys.argv[3]

outputFile = "mapVCF-to-Bed.sh"
with open(outputFile,'w') as outFile:
    outFile.write(f'sed -i \'s/^cpdna/chr/\' {genomeBedpath}nctc8325.bed;\n')  
    count=0
    with open(inputFile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if count !=0:                          
                outFile.write(f'{minicondaBin}bedtools intersect -a $WORK/ACM-outputs/vcfbed/{row[0]}.bed -b {genomeBedpath}nctc8325.bed > $WORK/ACM-outputs/intersection/{row[0]}.bed \n')
            count =count + 1

