#!/usr/bin/python

# Example: >>%run EcoliPputida1
#          >>avgfitness,sdfitness=EcoliPputidaFLYCOP_oneConf(...) 
# Goal: individual test to improve consortium {E.coli-P.putida}, depending on initial sucrose, fructose concentration that E. coli secretes and initial E.coli & KT biomasses 
# Run through the function EcoliPputidaFLYCOP_oneConf


import cobra
import os, stat
import pandas as pd
import tabulate
import re
import sys
import getopt
import os.path
import copy
import csv
import math
import cobra.flux_analysis.variability
import massedit
import subprocess
import shutil, errno
import statistics
import optlang
from cobra import Reaction
from cobra import Metabolite

# import gurobipy
# import spec

################################################################
### FUNCTION initialize_models #################################    
def initialize_models():
 # Only to run 1st time, to build the models!!
 if not(os.path.exists('ModelsInput/iEC1364_W_p_coumarate.xml')) or not(os.path.exists('ModelsInput/P.put_malonate.xml')):
     print('ERROR! Not iEC1364_W_p_coumarate.xml or P.put_malonate.xml files with GEM of consortium strains in ModelsInput!')
 else:
  path=os.getcwd()  # original path == "MicrobialCommunities"
  os.chdir('ModelsInput')
  
  # ---------------------------------------------------------------------------
  # E. coli WT for taking sucrose and excreting fructose
  # ---------------------------------------------------------------------------
  model=cobra.io.read_sbml_model("iEC1364_W_p_coumarate.xml")
  
  # Replace brackets with compartment location (e.g. "[c]") in metabolite ids by '_' (e.g. "_c") 
  for metabolite in model.metabolites:
    metabolite.id = re.sub('__91__c__93__',r'[c]',metabolite.id)
    metabolite.id = re.sub('__91__p__93__$',r'[p]',metabolite.id)
    metabolite.id = re.sub('__91__e__93__',r'[e]',metabolite.id)
    # metabolite.id = re.sub('__',r'_',metabolite.id)
    metabolite.compartment = ''
  # To solve possible problems in changing names     
  model.repair()
  
  # Replace brackets with compartment location (e.g. "[c]") in rxn ids by '_' (e.g. "_c") 
  for rxn in model.reactions:
    rxn.id = re.sub('__40__p__41__',r'(p)',rxn.id)
    rxn.id = re.sub('__40__c__41__',r'(c)',rxn.id)
    rxn.id = re.sub('__40__e__41__',r'(e)',rxn.id)    
  # To solve possible problems in changing names     
  model.repair()
  
  cobra.io.save_matlab_model(model,"iEC1364_W_p_coumaratemod.mat")
  del(model)
  model = cobra.io.load_matlab_model("iEC1364_W_p_coumaratemod.mat")
  
  # Put sucrose as carbon source and maximize uptake 
  model.reactions.get_by_id("EX_sucr(e)").bounds=(-15,0) # Maximize uptake, maximum upper bound
  
  # MAKE SURE FRUCTOSE METABOLISM IS SHUTTED DOWN
  model.reactions.get_by_id("XYLI2").bounds = (0, 0)
  model.reactions.get_by_id("HEX7").bounds = (0, 0)  # (0, 0) --> Model infeasible
  model.reactions.get_by_id("FRUpts2pp").bounds = (0, 0)  #
  model.reactions.get_by_id("FRUptspp").bounds = (0, 0)  # 
  
  # ACTIVATED REACTION: FFSD: h2o[c] + suc6p[c] --> fru[c] + g6p[c]
  model.reactions.get_by_id("FFSD").bounds = (0, 1000)
  
  cobra.io.save_matlab_model(model,"iEC1364_W_p_coumaratemod_tmp.mat")
  del(model)
  # ---------------------------------------------------------------------------
  
  
  # ---------------------------------------------------------------------------
  # P.putida KT 2440 model for taking fructose and secreting B12 // PENDIENTE: excreción B12
  model=cobra.io.read_sbml_model('P.put_malonate.xml') 

  # Replace brackets with compartment location (e.g. "[c]") in metabolite ids by '_' (e.g. "_c") 
  for metabolite in model.metabolites:
    metabolite.id = re.sub('__91__c__93__',r'[c]',metabolite.id)
    metabolite.id = re.sub('__91__p__93__$',r'[p]',metabolite.id)
    metabolite.id = re.sub('__91__e__93__',r'[e]',metabolite.id)
    # metabolite.id = re.sub('__',r'_',metabolite.id)
    metabolite.compartment = ''
  # To solve possible problems in changing names     
  model.repair()
  
  # Replace brackets with compartment location (e.g. "[c]") in rxn ids by '_' (e.g. "_c") 
  for rxn in model.reactions:
    rxn.id = re.sub('__40__p__41__',r'(p)',rxn.id)
    rxn.id = re.sub('__40__c__41__',r'(c)',rxn.id)
    rxn.id = re.sub('__40__e__41__',r'(e)',rxn.id)    
  # To solve possible problems in changing names     
  model.repair()
  
  cobra.io.save_matlab_model(model,"P.put_malonatemod.mat")
  del(model)
  model=cobra.io.load_matlab_model('P.put_malonatemod.mat') 
  
  # Maximize fructose uptake 
  model.reactions.get_by_id("EX_fru(e)").bounds=(-15,0)  # Maximize uptake, maximum upper bound
  
  # PREVENT P.putidaKT FROM TAKING glc[e] from the media
  model.reactions.get_by_id("EX_glc__D(e)").bounds = (0, 0)
  # ADJUST REACTION DIRECTION FOR SECRETING MALONATE: MALONpp  h[p] + malon[p] <-- h[c] + malon[c]
  model.reactions.get_by_id("MALONpp").bounds = (-1000, 0)
  
  cobra.io.save_matlab_model(model,"P.put_malonatemod_tmp.mat")
  del(model)
  # ---------------------------------------------------------------------------

  os.chdir(path)
# end-def initialize_models
################################################################    


################################################################    
### FUNCTION mat_to_comets #####################################    
# mat_to_comets(modelPath)
def mat_to_comets(matInputFile):
    model=cobra.io.load_matlab_model(matInputFile)
    # Open output file:
    with open(matInputFile+'.txt', mode='w') as f:
        # Print the S matrix
        f.write("SMATRIX  "+str(len(model.metabolites))+"  "+str(len(model.reactions))+"\n")
        for x in range(len(model.metabolites)):
            for y in range(len(model.reactions)):
                if (model.metabolites[x] in model.reactions[y].metabolites):
                    coeff=model.reactions[y].get_coefficient(model.metabolites[x])
                    f.write("    "+str(x+1)+"   "+str(y+1)+"   "+str(coeff)+"\n")
        f.write("//\n")
        
        # Print the bounds
        f.write("BOUNDS  -1000  1000\n");
        for y in range(len(model.reactions)):
            lb=model.reactions[y].lower_bound
            up=model.reactions[y].upper_bound
            f.write("    "+str(y+1)+"   "+str(lb)+"   "+str(up)+"\n")
        f.write("//\n")
        
        # Print the objective reaction
        f.write('OBJECTIVE\n')
        for y in range(len(model.reactions)):
            if (model.reactions[y] in model.objective):   # Cambio línea ejecución Docker
            # if (str(model.reactions[y].id) in str(model.objective.expression)):  # Cambio línea ejecución MiOrdenador
                indexObj=y+1
        f.write("    "+str(indexObj)+"\n")
        f.write("//\n")
        
        # Print metabolite names
        f.write("METABOLITE_NAMES\n")
        for x in range(len(model.metabolites)):
            f.write("    "+model.metabolites[x].id+"\n")
        f.write("//\n")

        # Print reaction names
        f.write("REACTION_NAMES\n")
        for y in range(len(model.reactions)):
            f.write("    "+model.reactions[y].id+"\n")
        f.write("//\n")

        # Print exchange reactions
        f.write("EXCHANGE_REACTIONS\n")
        for y in range(len(model.reactions)):
            if (model.reactions[y].id.find('EX_')==0):
                f.write(" "+str(y+1))
        f.write("\n//\n")            
    del(model)
### end-function-mat_to_comets    
################################################################


################################################################
### FUNCTION EcoliPputidaOneConf ############################
# maxCycles2=1000,500 or -1 meaning sucrose is exhausted
def EcoliPputidaFLYCOP_oneConf(sucr1, Ecbiomass, frc2, KTbiomass, fitFunc='MaxT4hcinnm_MaxMalon', maxCycles=500, dirPlot='', repeat=5):  
  '''
  Call: avgFitness, sdFitness = EcoliPputidaFLYCOP_oneConf(sucr1, Ecbiomass, frc2, KTbiomass)
  Start with no more than 5 repeats (1st trial)

  INPUTS: sucr1: lower bound of sucrose uptake in model 1 (E.coli) (mM)
          Ecbiomass: initial E. coli biomass (gL-1)
          frc2: lower bound of fructose uptake in model 2 (P.putida) (mM)
          KTbiomass: initial P. putida KT biomass (gL-1)
          
          fitFunc: fitness function to optimize. Either "MaxT4hcinnm" (E.coli) OR "MaxMalon" (P.putida) OR both 'MaxT4hcinnm_MaxMalon'
          maxCycles: cycles in COMETS run.
          dirPlot: copy of the graphs with several run results.
          repeat: number of runs with the same configuration.
          
  OUTPUT: avgFitness: average fitness of 'repeat' COMETS runs with the same configuration (due to it is not deterministic)
          sdFitness: standard deviation of fitness during 'repeat' COMETS runs (see above)
  '''

  if not(os.path.exists('ModelsInput/iEC1364_W_p_coumaratemod_tmp.mat')): # or os.path.exists('ModelsInput/P.put_malonatemod_tmp.mat')): 
      initialize_models()
      print("Inicializamos modelos\n")

  if(maxCycles > -1):
      maxCycles=int(maxCycles)
  else:
      maxCycles=500
  
  print("Fitness function:"+fitFunc)
  # print(os.getcwd())

  # Single GEMs parameter modifications
  # ===================================  
  if not(os.path.exists('iEC1364_W_p_coumaratemod_tmp.mat.txt')) or not (os.path.exists('P.put_malonatemod_tmp.mat.txt')):
    
    # ========================================================================= 
    # MODEL ADAPTATION TO THE PARAMETERS PASSED TO THE 'EcoliPputidaFLYCOP_oneConf' function
    # E. coli
    
    model=cobra.io.load_matlab_model('ModelsInput/iEC1364_W_p_coumaratemod_tmp.mat')
    model.objective = "BIOMASS_Ec_iJO1366_core_53p95M"  # Cambiar el objetivo del modelo para optimizar biomasa (core), un objetivo realista
    # model.objective = "BIOMASS_Ec_iJO1366_WT_53p95M"  # WT, en lugar de 'core'
    model.optimize()
    
    # -------------------------------------------------------------------------
    # FLUX VARIABILITY ANALYSIS: optimizar producción de FRUCTOSA / pCUMARATO al tiempo que crece E. coli (objective: BIOMASS_core)
    # Excretar fructosa / pCA aunque se pierda una parte de la capacidad de crecimiento máximo (obj.: BIOMASS) == 20% sobre objetivo global
    model.reactions.get_by_id('FFSD').bounds=(-1000,1000)  # To un-limit the fructose production, for the flux variability analysis
    model.reactions.get_by_id('FRUtpp').bounds=(-1000,1000)  # To un-limit the fructose production, for the flux variability analysis
    model.reactions.get_by_id('FRUtex').bounds=(-1000,1000)  # To un-limit the fructose production, for the flux variability analysis
    model.reactions.get_by_id('EX_fru(e)').bounds=(-1000,1000)  # To un-limit the fructose production, for the flux variability analysis
    dictOptValueFru = cobra.flux_analysis.flux_variability_analysis(model, {'EX_fru(e)'}, fraction_of_optimum=(1-0.20))
    dictOptValuepCA = cobra.flux_analysis.flux_variability_analysis(model, {'EX_T4hcinnm(e)'}, fraction_of_optimum=((1-0.20)))
   
    # FRUCTOSA
    FruExLimit=dictOptValueFru['EX_fru(e)']['maximum']
    model.reactions.get_by_id("FRUtpp").bounds=(0, FruExLimit)  # FRUtpp: fru[c] --> fru[p] // Bounds: (0, 3.973750000000021)
    model.reactions.get_by_id("FRUtex").bounds=(-FruExLimit, 0)  # FRUtex: fru[e] <-- fru[p] // Bounds: (-3.973750000000021, 0)
    model.reactions.get_by_id("EX_fru(e)").bounds=(FruExLimit, FruExLimit)  # valor único, óptimo encontrado  //  PONER SIEMPRE EL MISMO NÚMERO
    cobra.io.save_matlab_model(model,'iEC1364_W_p_coumaratemod_tmp.mat')
    
    # pCUMARATO
    pCALimit=dictOptValuepCA['EX_T4hcinnm(e)']['maximum']
    model.reactions.get_by_id('T4HCINNMtex').bounds=(pCALimit,1000)  # Reacción para exportar, transportador ajustado --> EXCRECIÓN con valores positivos
    model.reactions.get_by_id('EX_T4hcinnm(e)').bounds=(pCALimit,pCALimit)  # valor único, óptimo encontrado  //  PONER SIEMPRE EL MISMO NÚMERO
    cobra.io.save_matlab_model(model,'iEC1364_W_p_coumaratemod_tmp.mat')
    # -------------------------------------------------------------------------
    
    model.optimize()
    cobra.io.save_matlab_model(model,'iEC1364_W_p_coumaratemod_tmp.mat')
    del(model)                                    
    
    
    # =========================================================================
    # MODEL ADAPTATION TO THE PARAMETERS PASSED TO THE 'EcoliPputidaFLYCOP_oneConf' function
    # P. putida
    
    model=cobra.io.load_matlab_model('ModelsInput/P.put_malonatemod_tmp.mat')
    # model.objective = "BIOMASS_KT2440_Core2"  # Cambiar el objetivo del modelo para optimizar biomasa (core), un objetivo realista
    model.objective = "BIOMASS_KT2440_WT3"  # WT, en lugar de 'core'
    model.optimize()
    
    # Fórmula MALON
    model.metabolites.get_by_id("malon[c]").formula = "C3H2O4"  # CH2(COO)2²⁻
    model.metabolites.get_by_id("malon[p]").formula = "C3H2O4"
    model.metabolites.get_by_id("malon[e]").formula = "C3H2O4"
    
    # -------------------------------------------------------------------------
    # FLUX VARIABILITY ANALYSIS: optimizar producción de MALONATO al tiempo que crece P. putida Kt (objective: BIOMASS_WT)
    # Excretar malonato aunque se pierda una parte de la capacidad de crecimiento máximo (obj.: BIOMASS) == 20% sobre objetivo global
    dictMalonValue=cobra.flux_analysis.variability.flux_variability_analysis(model,{'EX_malon(e)'},fraction_of_optimum=(1 - 0.20))  # EXCRECIÓN MALONATO
    
    MalonLimit=dictMalonValue['EX_malon(e)']['maximum']
    model.reactions.get_by_id('MALONtex').bounds=(MalonLimit,1000)  # Reacción para exportar, transportador ajustado --> EXCRECIÓN con valores positivos
    model.reactions.get_by_id('EX_malon(e)').bounds=(MalonLimit,MalonLimit)  # valor único, óptimo encontrado  //  PONER SIEMPRE EL MISMO NÚMERO
    # -------------------------------------------------------------------------
    
    model.optimize()
    cobra.io.save_matlab_model(model,'P.put_malonatemod_tmp.mat')
    del(model)
    
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
    # MAT to COMETS
    mat_to_comets('iEC1364_W_p_coumaratemod_tmp.mat')
    mat_to_comets('P.put_malonatemod_tmp.mat')
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
    # Community parameter modifications
    # =================================            
    # 4.- [shell script] Write automatically the COMETS parameter about initial biomass of strains // Initial biomass --> parameter subject to optimization (.pcs)
    massedit.edit_files(['EcPp1_layout_template1.txt'],["re.sub(r'XXX','"+str(Ecbiomass)+"',line)"], dry_run=False)  # dry_run = False --> guardar archivo modificado // True, mostrar diferencias. En ese caso, ¿guarda?
    massedit.edit_files(['EcPp1_layout_template1.txt'],["re.sub(r'YYY','"+str(KTbiomass)+"',line)"], dry_run=False)
  # end-if building models
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# QUICK FRUCTOSE SUMMARY
    
  # model=cobra.io.load_matlab_model('ModelsInput/iEC1364_W_p_coumaratemod_tmp.mat')
  # model.optimize()
    
  # print("\n\nFINAL SUMMARY")
  # print(model.summary())
    
  # print("\n\nFRUCTOSE SUMMARY")
  # print("\n\n-----------------", model.metabolites.get_by_id("fru[c]").summary())
  # print("\n\n-----------------", model.metabolites.get_by_id("fru[p]").summary())
  # print("\n\n-----------------", model.metabolites.get_by_id("fru[e]").summary())
    
  # del(model)

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# QUICK MALON SUMMARY
    
  # model=cobra.io.load_matlab_model('ModelsInput/P.put_malonatemod_tmp.mat')
  # model.optimize()
    
  # print("\n\MALON SUMMARY")
  # print("\n\n-----------------", model.metabolites.get_by_id("malon[c]").summary())
  # print("\n\n-----------------", model.metabolites.get_by_id("malon[p]").summary())
  # print("\n\n-----------------", model.metabolites.get_by_id("malon[e]").summary())
    
  # del(model)
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

  # [COMETS by command line] Run COMETS
  if not(os.path.exists('IndividualRunsResults')):
    os.makedirs('IndividualRunsResults')
  totfitness=0
  sumpCA=0  # pCA quantity variable (production by E. coli)
  sumMalon=0  # Malon quantity variable (production by P.putida KT)
  fitnessList=[]  # List with the different values for 'totfitness' in every execution ('n' repeats)
  
  # path=os.getcwd()
  # print(path)
  print("\n---------------------------")
  for i in range(repeat):
        with open("output.txt", "w") as f:
            subprocess.run(args=['./comets_scr', 'comets_script_template'], stdout=f, stderr=subprocess.STDOUT)  # ejecutar COMETS con layout --> media_log_template1 / total_biomass_log_template1/ flux_log_template1
            
        # [R call] Run script to generate one graph:subprocess.call
        title=str(sucr1)+'_'+str(Ecbiomass)+'_'+str(frc2)+'_'+str(KTbiomass)  
        # print(title)
        subprocess.run(['../../Scripts/plot_biomassX2_vs_4mediaItem.sh template1 sucr T4hcinnm fru malon '+str(maxCycles)+' '+title+' blue black darkmagenta yellow EcoliWT KT2440'], shell=True)

        
        # Compute fitness (measure to optimize):
        # (A) DETERMINE ENDCYCLE: when sucrose is exhausted {}
        with open("biomass_vs_sucr_T4hcinnm_fru_malon_template1.txt", "r") as sources: # Creado en ejecución COMETS 'subprocess.run()'
            lines = sources.readlines()                                                            
            iniPointV=lines[0].split()  # Initial line, initial values                                                          
            iniBiomass=float(iniPointV[1])+float(iniPointV[2])  # Asumo suma de las dos biomasas
            endCycle=0
            
            # (Definir fin de ciclo por producción). Hasta entonces, el ciclo final es aquel en que se agota la sacarosa. Si este sustrato no se agota, 'endcycle' = último ciclo
            for line in lines:
                sucrConc=float(line.split()[3])
                endCycle=int(line.split()[0])
                if sucrConc == float(0.0):
                    break;
            
        # (B) FINAL BIOMASS // FINAL CONCENTRATIONS: pCA, Malon
        finalLineV=lines[endCycle].split()  # Line where the 'endcycle' is reached // Either sucrConc = 0.0, either encycle = last_cycle
        final_Ecbiomass = float(finalLineV[1])
        final_KTbiomass = float(finalLineV[2])
        
        totpCA=float(finalLineV[4])  
        totMalon=float(finalLineV[6])
        print("Execution: "+str(i)+" of "+str(repeat)+". CYCLE: "+str(endCycle))
        print("T4hcinnm: "+str(totpCA)+"\t\t"+"Malon: "+str(totMalon))
        finalBiomass = final_Ecbiomass + final_KTbiomass
        
        # (C) COMPUTE FITNESS: maximize pCA AND/OR Malon
        fitTime=1-(float(endCycle)/float(maxCycles))  # maxCycles == Number of total cycles
        fitpCA=float(totpCA/final_Ecbiomass)  # Normalized with respect to the final E. coli biomass
        fitMalon=float(totMalon/final_KTbiomass)  # Normalized with respect to the final P. putida KT biomass
        
        if(fitFunc=='MaxT4hcinnm'):
            fitness=fitpCA
        elif(fitFunc=='MaxMalon'):
            fitness=fitMalon
        elif(fitFunc=='MaxT4hcinnm_MaxMalon'):
            fitness=float(0.5*fitpCA+0.5*fitMalon)

        print(" Fitness: "+str(round(fitness,6))+" in cycle "+str(endCycle), "\n")

        totfitness += fitness  # 'n' repeats
        fitnessList.append(fitness)  # List with fitness values in 'n' repeats
        sumpCA += totpCA  # Total pCA for 'n' repeats
        sumMalon += totMalon  # Total Malon for 'n' repeats

        # ---------------------------------------------------------------------
        # Copy individual solution
        file='IndividualRunsResults/'+'biomass_vs_sucr_T4hcinnm_fru_malon_run'+str(i)+'_'+str(fitness)+'_'+str(endCycle)+'.pdf'
        shutil.move('biomass_vs_sucr_T4hcinnm_fru_malon_template1_plot.pdf',file)        
        if(dirPlot != ''):
            file2=dirPlot+'biomass_vs_sucr_T4hcinnm_fru_malon'+str(sucr1)+'_'+str(Ecbiomass)+'_'+str(frc2)+'_'+str(KTbiomass)+'_run'+str(i)+'_'+str(fitness)+'_'+str(endCycle)+'.pdf'
            shutil.move(file,file2)
            
        file='IndividualRunsResults/'+'total_biomass_log_run'+str(i)+'.txt'
        shutil.move('total_biomass_log_template1.txt',file)
        file='IndividualRunsResults/'+'media_log_run'+str(i)+'.txt'
        shutil.move('media_log_template1.txt',file)
        file='IndividualRunsResults/'+'flux_log_run'+str(i)+'.txt'
        shutil.move('flux_log_template1.txt',file)   

  avgfitness=totfitness/repeat  # 'totfitness' average in 'n' repeats
  if(repeat>1):
      sdfitness=statistics.stdev(fitnessList)  # standard deviations for 'n' values
  else:
      sdfitness=0.0
      
  avgpCA = sumpCA/repeat
  avgMalon = sumMalon/repeat
  # --------------------------------------------------------------------------- 
  # Display results in terminal
  print("Fitness_function \t configuration \t\t fitness \t sd \t\t pCA(mM) \t Malon(mM) \t endCycle")  # UNITS: mM (metabolites)  //  gL-1 (biomass)
  print(fitFunc+"\t"+str(sucr1)+','+str(Ecbiomass)+','+str(frc2)+','+str(KTbiomass)+"\t"+str(round(avgfitness,6))+"\t"+str(sdfitness)+"\t"+str(round(avgpCA,6))+"\t"+str(round(avgMalon,6))+"\t"+str(endCycle))
  with open(dirPlot+"configurationsResults"+fitFunc+".txt", "a") as myfile:
      myfile.write("Fitness_function\tconfiguration\tfitness\tsd\tpCA(mM)\tMalon(mM)\tendCycle")
      myfile.write(fitFunc+"\t"+str(sucr1)+','+str(Ecbiomass)+','+str(frc2)+','+str(KTbiomass)+"\t"+str(round(avgfitness,6))+"\t"+str(sdfitness)+"\t"+str(round(avgpCA,6))+"\t"+str(round(avgMalon,6))+"\t"+str(endCycle))
  
  print("Avg.fitness(sd):\t"+str(avgfitness)+"\t(+/-"+str(sdfitness)+")\n")
  if(sdfitness>0.1):  # Correction if SD is too high
      avgfitness=0.0
  
  return avgfitness,sdfitness
# end-def EcoliPputidaOneConf
################################################################




