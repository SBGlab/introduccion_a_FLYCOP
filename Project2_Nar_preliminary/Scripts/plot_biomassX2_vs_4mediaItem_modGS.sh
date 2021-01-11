#!/bin/bash

# FLYCOP 
# Author: Beatriz García-Jiménez
# April 2018

# Call:
#sh ../../Scripts/plot_biomassX2_vs_4mediaItem.sh <suffix> <nutrientID1 (without [e])> <nutrientID2> <strain1> <strain2>

dirScripts="../../Scripts"

suffix=$1
met1=$2
met2=$3
met3=$4
met4=$5
endCycle=$6
title=$7
colorSubs1=$8
colorSubs2=$9
colorSubs3=${10}
colorSubs4=${11}
strain1=${12}
strain2=${13}

outFile="biomass_vs_${met1}_${met2}_${met3}_${met4}_${suffix}.txt"
plotFile="biomass_vs_${met1}_${met2}_${met3}_${met4}_${suffix}_plot.pdf"

numMet1=`head -n1 media_log_${suffix}.txt | sed "s/.*{ //" | sed "s/}.*//" | sed "s/'//g" | sed "s/, /\n/g" | egrep -w -n ${met1} | cut -d: -f1`
numMet2=`head -n1 media_log_${suffix}.txt | sed "s/.*{ //" | sed "s/}.*//" | sed "s/'//g" | sed "s/, /\n/g" | egrep -w -n ${met2} | cut -d: -f1`
numMet3=`head -n1 media_log_${suffix}.txt | sed "s/.*{ //" | sed "s/}.*//" | sed "s/'//g" | sed "s/, /\n/g" | egrep -w -n ${met3} | cut -d: -f1`
numMet4=`head -n1 media_log_${suffix}.txt | sed "s/.*{ //" | sed "s/}.*//" | sed "s/'//g" | sed "s/, /\n/g" | egrep -w -n ${met4} | cut -d: -f1`

met1File="media_log_substrate_${met1}.txt"
egrep '\{'$numMet1'\}' media_log_${suffix}.txt | sed "s/media_//" | sed "s/{$numMet1}//" | sed "s/(\([[:digit:]]\|10\), \([[:digit:]]\|10\))//g" | sed "s/sparse.*/0.0/" | sed "s/;$//" | sed "s/\ =\ /\t/" | awk -F"\t" 'BEGIN{oldCycle=0;value=-1}{if($1!=oldCycle){print value; oldCycle=$1; value=$2}else{value=$2}}END{print value}' > $met1File

met2File="media_log_substrate_${met2}.txt"
egrep '\{'$numMet2'\}' media_log_${suffix}.txt | sed "s/media_//" | sed "s/{$numMet2}//" | sed "s/(\([[:digit:]]\|10\), \([[:digit:]]\|10\))//g" | sed "s/sparse.*/0.0/" | sed "s/;$//" | sed "s/\ =\ /\t/" | awk -F"\t" 'BEGIN{oldCycle=0;value=-1}{if($1!=oldCycle){print value; oldCycle=$1; value=$2}else{value=$2}}END{print value}' > $met2File

met3File="media_log_substrate_${met3}.txt"
egrep '\{'$numMet3'\}' media_log_${suffix}.txt | sed "s/media_//" | sed "s/{$numMet3}//" | sed "s/(\([[:digit:]]\|10\), \([[:digit:]]\|10\))//g" | sed "s/sparse.*/0.0/" | sed "s/;$//" | sed "s/\ =\ /\t/" | awk -F"\t" 'BEGIN{oldCycle=0;value=-1}{if($1!=oldCycle){print value; oldCycle=$1; value=$2}else{value=$2}}END{print value}' > $met3File

met4File="media_log_substrate_${met4}.txt"
egrep '\{'$numMet4'\}' media_log_${suffix}.txt | sed "s/media_//" | sed "s/{$numMet4}//" | sed "s/(\([[:digit:]]\|10\), \([[:digit:]]\|10\))//g" | sed "s/sparse.*/0.0/" | sed "s/;$//" | sed "s/\ =\ /\t/" | awk -F"\t" 'BEGIN{oldCycle=0;value=-1}{if($1!=oldCycle){print value; oldCycle=$1; value=$2}else{value=$2}}END{print value}' > $met4File

paste -d'\t' total_biomass_log_${suffix}.txt ${met1File} ${met2File} ${met3File} ${met4File} > $outFile
# rm ${met1File} ${met2File} ${met3File} ${met4File}

Rscript --vanilla ${dirScripts}/plot.biomassX2.vs.4substrate.r $outFile $plotFile $met1 $met2 $met3 $met4 $endCycle $title $colorSubs1 $colorSubs2 $colorSubs3 $colorSubs4 $strain1 $strain2



