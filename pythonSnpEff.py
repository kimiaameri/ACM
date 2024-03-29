import csv
import sys

if len(sys.argv) < 4:
    sys.stderr.write('No Input CSV file and BCFTools and java\n')
    sys.exit(0)
    
inputFile = sys.argv[1]
BCFTools = sys.argv[2]
minicondaBin = sys.argv[3]
cpath = sys.argv[4]
outputFile = "snpEff.sh"

with open(inputFile) as csv_file:

    csv_reader = csv.reader(csv_file, delimiter=',')
    highSamples = []
    lowSamples = []
    for row in csv_reader:
        if row[3].lower() == 'E2_1': highSamples.append(row[0])
        if row[1].lower() == 'low': lowSamples.append(row[0])
    print(highSamples)
    print(lowSamples)
    high = len(highSamples)
    low = len(lowSamples)
    with open (cpath +"/High.txt",'w') as of:
        of.write(str(high))
    with open (cpath + "/Low.txt",'w') as of:
        of.write(str(low))
        
    length = high + low
    with open(outputFile,'w') as outFile:
        outFile.write(f'{BCFTools}bcftools isec $WORK/ACM-outputs/bcfoutput/*.gz -p $WORK/ACM-outputs/All -n={length};\n')
        prefix = "$WORK/ACM-outputs/bcfoutput/"
        allHigh = []
        for sample in highSamples :
            allHigh.append(prefix + sample + ".vcf.gz")
        allHighStr  = ' '.join(allHigh)         
        outFile.write(f'{BCFTools}bcftools isec {allHighStr} -p $WORK/ACM-outputs/high -n={high};\n')
        allLow = []
        for sample in lowSamples :
            allLow.append(prefix + sample + ".vcf.gz")
        
        allLowStr  = ' '.join(allLow)         

        outFile.write(f'{BCFTools}bcftools isec {allLowStr} -p $WORK/ACM-outputs/low -n={low};\n')
        outFile.write('sed -i \'s/^chr/Chromosome/\' $WORK/ACM-outputs/All/*.vcf;\n')
        outFile.write('sed -i \'s/^chr/Chromosome/\' $WORK/ACM-outputs/high/*.vcf;\n')
        outFile.write('sed -i \'s/^chr/Chromosome/\' $WORK/ACM-outputs/low/*.vcf;\n')
        outFile.write(f'{minicondaBin}java -Xmx4g -jar $WORK/ACM-softwares/snpEff/snpEff.jar -v Staphylococcus_aureus_subsp_aureus_nctc_8325 $WORK/ACM-outputs/all/0000.vcf > $WORK/ACM-outputs/snpEff-outputs/snpEff_intersection_All.ann.vcf \n')
        outFile.write('mv $WORK/ACM/snpEff_genes.txt $WORK/ACM-outputs/snpEff-outputs/snpEff-gene/snpEff_All_intersection_genes.txt \n')
        outFile.write('mv $WORK/ACM/snpEff_summary.html $WORK/ACM-outputs/snpEff-outputs/snpEff-summary/snpEff_All_intersection_summary.html \n')
        for i in highSamples:
             outFile.write(f'{minicondaBin}java -Xmx4g -jar $WORK/ACM-softwares/snpEff/snpEff.jar -v Staphylococcus_aureus_subsp_aureus_nctc_8325 $WORK/ACM-outputs/high/0000.vcf > $WORK/ACM-outputs/snpEff-outputs/snpEff_intersection_high.ann.vcf \n')
             outFile.write('mv $WORK/ACM/snpEff_genes.txt $WORK/ACM-outputs/snpEff-outputs/snpEff-gene/snpEff_high_intersection_genes.txt \n')
             outFile.write('mv $WORK/ACM/snpEff_summary.html $WORK/ACM-outputs/snpEff-outputs/snpEff-summary/snpEff_high_intersection_summary.html \n')
        for i in lowSamples:
             outFile.write(f'{minicondaBin}java -Xmx4g -jar $WORK/ACM-softwares/snpEff/snpEff.jar -v Staphylococcus_aureus_subsp_aureus_nctc_8325 $WORK/ACM-outputs/low/0000.vcf > $WORK/ACM-outputs/snpEff-outputs/snpEff_intersection_low.ann.vcf \n')
             outFile.write('mv $WORK/ACM/snpEff_genes.txt $WORK/ACM-outputs/snpEff-outputs/snpEff-gene/snpEff_low_intersection_genes.txt \n')
             outFile.write('mv $WORK/ACM/snpEff_summary.html $WORK/ACM-outputs/snpEff-outputs/snpEff-summary/snpEff_low_intersection_summary.html \n')




