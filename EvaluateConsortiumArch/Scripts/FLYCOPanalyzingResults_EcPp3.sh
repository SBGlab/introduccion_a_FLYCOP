#!/bin/bash

# FLYCOP 
# Author: Beatriz García-Jiménez, Iván Martín Martín
# April 2018 // Modification: April 2021

# call: FLYCOPanalyzingResults_EcPp3.sh 0 V0 'MaxNaringenin' 100
# sh FLYCOP.sh 'EcPp3' 0 V0 'MaxNaringenin' 5
# sh FLYCOP.sh 'EcPp3' 0 V0 'MaxNaringenin' 100

domainName='EcPp3'

id=$1 # '20', '21', ...
templateID=$2 # 'V1' 'V2' 'V5' ...
fitness=$3
nRuns=$4  # Nº de ejecuciones SMAC (aleatorización real)

echo "Initializing FLYCOPanalizingResults"
pwd
currDir=`pwd`  # Debería ser FLYCOP/MicrobialCommunities (folder)
dataAnalysisDir=${currDir}/${domainName}_scenario${id}_FLYCOPdataAnalysis  # FLYCOP folder
mkdir $dataAnalysisDir

seed=123
cd smac-output/${domainName}_confFLYCOP_scenario_v${id}/state-run${seed}  # FLYCOP folder


# 1.- Get summary statistics file $nRuns SMAC configurations
# ----------------------------------------------------------

tail -n${nRuns} runs_and_results-it*.csv | awk -F, '{print NR","1-$4}' > $dataAnalysisDir/fitness.csv
paste -d, paramstrings-it*.txt $dataAnalysisDir/fitness.csv > $dataAnalysisDir/paramstrings_withFitness.csv	# Archivos generados por SMAC

echo "sucr1\tEcbiomass\tEcbiomass_glyc\tfrc2\tKTbiomass\tNH4Ec\tNH4KT\tCons_Arch\tfitFunc" > $dataAnalysisDir/tableParamWithFitness.csv
cut -d, -f1-8,10 $dataAnalysisDir/paramstrings_withFitness.csv | awk 'BEGIN{FS="[=,]"} {print $2"\t"$4"\t"$6"\t"$8"\t"$10"\t"$12"\t"$14"\t"$16"\t"$17}' | sed "s/'//g" | sed "s/-999999999/0/">> $dataAnalysisDir/tableParamWithFitness.csv

egrep "WARN.*Result of algorithm run|ERROR.*The following algorithm call failed" ../log-warn${seed}.txt | awk -F'Result of algorithm run: ' '{if($2==""){print "X,X,X,1,X,X,1"}else{print $2}}' | cut -d, -f4,7 | awk -F, '{print 1-$1","$2}' > $dataAnalysisDir/avgfitnessAndStdev.txt

# Retrieve configuration

cd ..
param1=`tail log-run${seed}.txt | egrep "p1_sucr1" | awk -F'p1_sucr1' '{print $2}' | cut -d' ' -f2 | sed "s/'//g"`
param2=`tail log-run${seed}.txt | egrep "p1_sucr1" | awk -F'p1_sucr1' '{print $2}' | cut -d' ' -f4 | sed "s/'//g"`
param3=`tail log-run${seed}.txt | egrep "p1_sucr1" | awk -F'p1_sucr1' '{print $2}' | cut -d' ' -f6 | sed "s/'//g"`
param4=`tail log-run${seed}.txt | egrep "p1_sucr1" | awk -F'p1_sucr1' '{print $2}' | cut -d' ' -f8 | sed "s/'//g"`
param5=`tail log-run${seed}.txt | egrep "p1_sucr1" | awk -F'p1_sucr1' '{print $2}' | cut -d' ' -f10 | sed "s/'//g"`
param6=`tail log-run${seed}.txt | egrep "p1_sucr1" | awk -F'p1_sucr1' '{print $2}' | cut -d' ' -f12 | sed "s/'//g"`
param7=`tail log-run${seed}.txt | egrep "p1_sucr1" | awk -F'p1_sucr1' '{print $2}' | cut -d' ' -f14 | sed "s/'//g"`
param8=`tail log-run${seed}.txt | egrep "p1_sucr1" | awk -F'p1_sucr1' '{print $2}' | cut -d' ' -f16 | sed "s/'//g"`
echo "Optimal consortium configuration found: " $param1 $param2 $param3 $param4 $param5 $param6 $param7 $param8
cd ../..


# 2.- Move configurations collection file to data analysis folder
# ---------------------------------------------------------------

mv smac-output/${domainName}_PlotsScenario${id}/ $dataAnalysisDir/
# rm -Rf smac-output/
cd $dataAnalysisDir
mv ${domainName}_PlotsScenario${id}/configurationsResults* configurationsResults_Scenario${id}.txt
cd ..

# 3.- R script to build scatterplot and correlations files
# --------------------------------------------------------

echo "Initializing dataAnalysisPlotsAndTables_generic_single = Rscript"
Rscript --vanilla ../Scripts/dataAnalysisPlotsAndTables_EcPp3.r $domainName $id $fitness
echo "Finished dataAnalysisPlotsAndTables_generic_single = Rscript"


# 4.- Individual Test for the optimal configuration
# -------------------------------------------------

cp -p -R EcPp3_TemplateOptimizeConsortium${templateID} EcPp3_scenario${id}_optimalConfiguration
cd EcPp3_scenario${id}_optimalConfiguration
python3 -W ignore ../../Scripts/EcPp3_individualTestFLYCOP_v0.py $param1 $param2 $param3 $param4 $param5 $param6 $param7 $param8 $fitness
cd $currDir  # MicrobialCommunities


# 5.- Preliminary analysis of the configurationsResults.txt file
# ---------------------------------------------------------------

mkdir -p $dataAnalysisDir/PreliminaryAnalysis
cp -r FLYCOP_${domainName}_${id}_log.txt $dataAnalysisDir/PreliminaryAnalysis
cp -r $dataAnalysisDir/configurationsResults_Scenario${id}.txt $dataAnalysisDir/PreliminaryAnalysis

cd $dataAnalysisDir/PreliminaryAnalysis
python3 -W ignore ../../../Scripts/EcPp3_preliminaryAnalysis_v0.py $domainName $id

rm -r FLYCOP_${domainName}_${id}_log.txt
cp -r configurationsResults_Scenario${id}.txt ..  # This would be the updated version of configurationsResults_Scenario${id}.txt, since it has the "ConfigKey" column
# Thus we overwrite the original file!
cd ../../..
# ---------------------------------------------------------------

echo "Finished FLYCOPanalizingResults"





















