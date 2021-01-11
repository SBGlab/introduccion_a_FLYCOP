#!/bin/bash

# FLYCOP 
# Author: Beatriz García-Jiménez
# April 2018 // Modification: November 2020

# call: FLYCOPanalyzingResults_EcPp2.sh 0 V0 'MaxT4hcinnm_MaxMalon' 5
# sh FLYCOP.sh 'EcPp2' 0 V0 'MaxNaringenin' 5
# sh FLYCOP.sh 'EcPp2' 0 V0 'MaxNaringenin' 100

domainName='EcPp2'

id=$1 # '20', '21', ...
templateID=$2 # 'V1' 'V2' 'V5' ...
fitness=$3
nRuns=$4  # Nº de ejecuciones SMAC (aleatorización real)

echo "Initializing FLYCOPanalizingResults"
pwd
currDir=`pwd`  # Debería ser FLYCOP (folder)
dataAnalysisDir=${currDir}/${domainName}_scenario${id}_FLYCOPdataAnalysis  # FLYCOP folder
mkdir $dataAnalysisDir

seed=123
cd smac-output/${domainName}_confFLYCOP_scenario_v${id}/state-run${seed}  # FLYCOP folder

# 1.- Get summary statistics file $nRuns SMAC configurations
tail -n${nRuns} runs_and_results-it*.csv | awk -F, '{print NR","1-$4}' > $dataAnalysisDir/fitness.csv
paste -d, paramstrings-it*.txt $dataAnalysisDir/fitness.csv > $dataAnalysisDir/paramstrings_withFitness.csv	# Archivos generados por SMAC

echo "sucr1\tEcbiomass\tfrc2\tKTbiomass\tfitFunc" > $dataAnalysisDir/tableParamWithFitness.csv
cut -d, -f1-4,6 $dataAnalysisDir/paramstrings_withFitness.csv | awk 'BEGIN{FS="[=,]"} {print $2"\t"$4"\t"$6"\t"$8"\t"$9}' | sed "s/'//g" | sed "s/-999999999/0/">> $dataAnalysisDir/tableParamWithFitness.csv

egrep "WARN.*Result of algorithm run|ERROR.*The following algorithm call failed" ../log-warn${seed}.txt | awk -F'Result of algorithm run: ' '{if($2==""){print "X,X,X,1,X,X,1"}else{print $2}}' | cut -d, -f4,7 | awk -F, '{print 1-$1","$2}' > $dataAnalysisDir/avgfitnessAndStdev.txt

# Retrieve configuration
cd ..
param1=`tail log-run${seed}.txt | egrep "p1_sucr1" | awk -F'p1_sucr1' '{print $2}' | cut -d' ' -f2 | sed "s/'//g"`
param2=`tail log-run${seed}.txt | egrep "p1_sucr1" | awk -F'p1_sucr1' '{print $2}' | cut -d' ' -f4 | sed "s/'//g"`
param3=`tail log-run${seed}.txt | egrep "p1_sucr1" | awk -F'p1_sucr1' '{print $2}' | cut -d' ' -f6 | sed "s/'//g"`
param4=`tail log-run${seed}.txt | egrep "p1_sucr1" | awk -F'p1_sucr1' '{print $2}' | cut -d' ' -f8 | sed "s/'//g"`
echo "Optimal consortium configuration found: " $param1 $param2 $param3 $param4
cd ../..

# 2.- Move configurations collection file to data analysis folder
mv smac-output/${domainName}_PlotsScenario${id}/ $dataAnalysisDir/
# rm -Rf smac-output/
cd $dataAnalysisDir
mv ${domainName}_PlotsScenario${id}/configurationsResults* configurationsResults_Scenario${id}.txt
sort -k3 -r configurationsResults_Scenario${id}.txt | uniq > configurationsResults_Scenario${id}_sorted.txt 
rm configurationsResults_Scenario${id}.txt
cd ..

# 3.- R script to build scatterplot and correlations files
echo "Initializing dataAnalysisPlotsAndTables_generic_single = Rscript"
Rscript --vanilla ../Scripts/dataAnalysisPlotsAndTables_EcPp2_single.r $domainName $id $fitness
echo "Finished dataAnalysisPlotsAndTables_generic_single = Rscript"

# 4.- Generar un test individual, con el mismo nº de scenario (tengo que hacer trozo script python)
cp -p -R EcPp2_TemplateOptimizeConsortium${templateID} EcPp2_scenario${id}_optimalConfiguration
cd EcPp2_scenario${id}_optimalConfiguration
python3 -W ignore ../../Scripts/EcPp2_individualTestFLYCOP.py $param1 $param2 $param3 $param4 $fitness
cd $currDir

echo "Finished FLYCOPanalizingResults"

