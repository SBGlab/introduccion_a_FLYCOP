#!/usr/bin/python

# Example: >>%run EcoliPputida2
#          >>avgfitness,sdfitness=EcoliPputidaFLYCOP_oneConf(...) 
# Goal: individual test to improve consortium {E.coli-P.putida}, depending on initial sucrose, fructose concentration that E. coli secretes and initial E.coli & KT biomasses 
# Run through the function EcoliPputidaFLYCOP_oneConf


# -----------------------------------------------------------------------------
# Project3_EcPp2_LimNut_M9
# -----------------------------------------------------------------------------


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
 if not(os.path.exists('ModelsInput/iEC1364_W_p_coumarate.xml')) or not(os.path.exists('ModelsInput/iJN1463_naringeninB12.xml')):
     print('ERROR! Not iEC1364_W_p_coumarate.xml or iJN1463_naringeninB12.xml files with GEM of consortium strains in ModelsInput!')
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
  cobra.io.save_matlab_model(model,"iEC1364_W_p_coumaratemod.mat")
  del(model)
  model = cobra.io.load_matlab_model("iEC1364_W_p_coumaratemod.mat")
  
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
  
  # Put sucrose as carbon source and maximize uptake, later changed by the parameter 'sucr1'
  model.reactions.get_by_id("EX_sucr(e)").bounds=(-15,0)
  # OXYGEN UPTAKE
  model.reactions.get_by_id("EX_o2(e)").bounds = (-20, 0)
  
  # MAKE SURE FRUCTOSE METABOLISM IS SHUTTED DOWN
  model.reactions.get_by_id("XYLI2").bounds = (0, 0)
  model.reactions.get_by_id("HEX7").bounds = (0, 0)  
  model.reactions.get_by_id("FRUpts2pp").bounds = (0, 0)
  model.reactions.get_by_id("FRUptspp").bounds = (0, 0)
  
  # ACTIVATED REACTION: FFSD: h2o[c] + suc6p[c] --> fru[c] + g6p[c]
  model.reactions.get_by_id("FFSD").bounds = (0, 1000)
  # To un-limit the fructose production, for the flux variability analysis
  model.reactions.get_by_id('FRUtpp').bounds=(-1000,1000)  
  model.reactions.get_by_id('FRUtex').bounds=(-1000,1000)  
  model.reactions.get_by_id('EX_fru(e)').bounds=(-1000,1000)
  
  # B12 auxotrophy: control / dependence with P.putida KT2440
  model.reactions.ADOCBLS.bounds=(0,0)
  
  cobra.io.save_matlab_model(model,"iEC1364_W_p_coumaratemod_tmp.mat")
  del(model)
  # ---------------------------------------------------------------------------
  
  
  # ---------------------------------------------------------------------------
  # P.putida KT 2440 model for taking fructose and secreting B12
  # model=cobra.io.read_sbml_model('iJN1463_naringenin_mod.xml')  # Model composed by Iván, based on "iJN1463 - P.put_malonate.xml"
  model=cobra.io.read_sbml_model('iJN1463_naringeninB12.xml')  # David's original model + B12 reactions

  # Replace brackets with compartment location (e.g. "[c]") in metabolite ids by '_' (e.g. "_c") 
  for metabolite in model.metabolites:
    metabolite.id = re.sub('__91__c__93__',r'[c]',metabolite.id)
    metabolite.id = re.sub('__91__p__93__$',r'[p]',metabolite.id)
    metabolite.id = re.sub('__91__e__93__',r'[e]',metabolite.id)
    # metabolite.id = re.sub('__',r'_',metabolite.id)
    metabolite.compartment = ''
  # To solve possible problems in changing names     
  model.repair()
  cobra.io.save_matlab_model(model,"iJN1463_naringeninB12.mat")
  del(model)
  model=cobra.io.load_matlab_model('iJN1463_naringeninB12.mat') 
  
  # Replace brackets with compartment location (e.g. "[c]") in rxn ids by '_' (e.g. "_c") 
  for rxn in model.reactions:
    rxn.id = re.sub('__40__p__41__',r'(p)',rxn.id)
    rxn.id = re.sub('__40__c__41__',r'(c)',rxn.id)
    rxn.id = re.sub('__40__e__41__',r'(e)',rxn.id)    
  # To solve possible problems in changing names     
  model.repair()
  cobra.io.save_matlab_model(model,"iJN1463_naringeninB12.mat")
  del(model)
  model=cobra.io.load_matlab_model('iJN1463_naringeninB12.mat') 
  
  
  # -------------------------------------------------------------------------
  # MODEL ADJUSTEMENTS
  # model.reactions.get_by_id("EX_sucr(e)").bounds = (0, 0)  # Este modelo no puede captar sacarosa
  
  # FRU reactions
  model.reactions.get_by_id("EX_fru(e)").bounds=(-15,0)  # Maximize uptake, maximum upper bound  //  DAVID: (-8, 0)  //  Later changed by the parameter 'frc2'
  model.reactions.get_by_id("FRUtex").bounds = (0, 1000)
  # model.reactions.FRUtex.bounds=(0,8)

  # PREVENT P.putidaKT FROM TAKING glc[e] from the media
  model.reactions.get_by_id("EX_glc__D(e)").bounds = (0, 0)
  # OXYGEN UPTAKE
  model.reactions.get_by_id("EX_o2(e)").bounds = (-20, 0)
  
  # pCOUMARATE UPTAKE  --> ¿Cambios sugeridos? Tomar todo el T4hcinnm posible (disponible en el medio)
  model.reactions.get_by_id("EX_T4hcinnm(e)").bounds = (-1000, 0)
  model.reactions.get_by_id("T4HCINNMtex").bounds = (0, 1000)
  model.reactions.get_by_id("T4HCINNMtpp").bounds = (0, 1000)
  model.reactions.get_by_id("4CMCOAS").bounds = (0, 0)  # T4hcinnm[c] + atp[c] + coa[c] --> amp[c] + coucoa[c] + ppi[c]
  
  # MALON reactions - no MALON secretion
  model.reactions.get_by_id("EX_malon(e)").bounds = (0, 0)
  model.reactions.get_by_id("MALONtex").bounds = (0, 0)
  model.reactions.get_by_id("MALONpp").bounds = (0, 0)
  model.reactions.get_by_id("MALONHY").bounds = (0, 0)  # Reacción de hidrólisis de malcoa[c] --> malon[c]
        
  # NARINGENIN reactions
  model.reactions.get_by_id("matB").bounds = (0, 1000)  # Ajuste posterior, de otro modo KT prioriza producción de naringenina, deja de crecer y se consume en el medio
  model.reactions.get_by_id("naringenintpp").bounds = (0, 1000)
  model.reactions.get_by_id("naringenintex").bounds = (0, 1000)
  # -------------------------------------------------------------------------
  
  cobra.io.save_matlab_model(model,"iJN1463_naringeninB12_tmp.mat")
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
def EcoliPputidaFLYCOP_oneConf(sucr1, Ecbiomass, frc2, KTbiomass, fitFunc='MaxNaringenin', maxCycles = 240, dirPlot='', repeat=5):  
  '''
  Call: avgFitness, sdFitness = EcoliPputidaFLYCOP_oneConf(sucr1, Ecbiomass, frc2, KTbiomass)
  Start with no more than 5 repeats (1st trial)

  INPUTS: sucr1: lower bound of sucrose uptake in model 1 (E.coli) (mM)
          Ecbiomass: initial E. coli biomass (gL-1)
          frc2: lower bound of fructose uptake in model 2 (P.putida) (mM)
          KTbiomass: initial P. putida KT biomass (gL-1)
          
          fitFunc: fitness function to optimize. 'MaxNaringenin', maximize Naringenin production by P. putida KT2440 (mM)
                                                 
          maxCycles: cycles in COMETS run, stated in file 'layout_template'. It is not used in the Python scripts (wrapper, individualTest). If desired to change, see 'layout_template'
          dirPlot: copy of the plots with several run results.
          repeat: number of runs with the same configuration (COMETS, not number of SMAC iterations)
          
          POTENTIAL LIMITATION OF NUTRIENTS: nh4 and/or pi
                  please, modify initial concentrations in layout_template
          
  OUTPUT: avgFitness: average fitness of 'repeat' COMETS runs with the same configuration (due to it is not deterministic)
          sdFitness: standard deviation of fitness during 'repeat' COMETS runs (see above)
  '''

  if not(os.path.exists('ModelsInput/iEC1364_W_p_coumaratemod_tmp.mat')): # or os.path.exists('ModelsInput/P.put_malonatemod_tmp.mat')): 
      initialize_models()
      print("Inicializamos modelos\n")

  print("Fitness function: ", fitFunc)
  # print(os.getcwd())

  # Single GEMs parameter modifications
  # ===================================  
  if not(os.path.exists('iEC1364_W_p_coumaratemod_tmp.mat.txt')) or not (os.path.exists('iJN1463_naringeninB12_tmp.mat.txt')):
    
    # ========================================================================= 
    # MODEL ADAPTATION TO THE PARAMETERS PASSED TO THE 'EcoliPputidaFLYCOP_oneConf' function
    # E. coli
    
    model=cobra.io.load_matlab_model('ModelsInput/iEC1364_W_p_coumaratemod_tmp.mat')
    # model.objective = "BIOMASS_Ec_iJO1366_core_53p95M"  # Cambiar el objetivo del modelo para optimizar biomasa (core), un objetivo realista
    model.objective = "BIOMASS_Ec_iJO1366_WT_53p95M"  # WT, en lugar de 'core'
    
    # This reaction ('EX_sucr(e)') controls the global sucr exchange flux for E. coli
    model.reactions.get_by_id("EX_sucr(e)").bounds=(sucr1, 0)
    # The rest of reactions depend on the sucr flux already specified
    model.reactions.get_by_id("SUCtpp").bounds=(0, 1000)  # sucr[p] --> sucr[c]  
    model.reactions.get_by_id("SUCRtpp").bounds=(0, 1000)  # sucr[p] --> sucr[c]
    model.reactions.get_by_id("SUCRtex").bounds=(0, 1000)  # sucr[e] --> sucr[p]
    model.optimize()
    
    # -------------------------------------------------------------------------
    # FLUX VARIABILITY ANALYSIS: optimizar producción de FRUCTOSA / pCUMARATO al tiempo que crece E. coli (objective: BIOMASS_core)
    # Excretar fructosa / pCA aunque se pierda una parte de la capacidad de crecimiento máximo (obj.: BIOMASS) == 20% sobre objetivo global
    dictOptValueFru = cobra.flux_analysis.flux_variability_analysis(model, {'EX_fru(e)'}, fraction_of_optimum=(1-0.20))
    dictOptValuepCA = cobra.flux_analysis.flux_variability_analysis(model, {'EX_T4hcinnm(e)'}, fraction_of_optimum=((1-0.20)))
   
    # FRUCTOSA
    # ======================
    FruExLimit=dictOptValueFru['EX_fru(e)']['maximum']
    model.reactions.get_by_id("FRUtpp").bounds=(0, FruExLimit)  # FRUtpp: fru[c] --> fru[p] // Bounds: (0, 3.973750000000021)
    model.reactions.get_by_id("FRUtex").bounds=(-FruExLimit, 0)  # FRUtex: fru[e] <-- fru[p] // Bounds: (-3.973750000000021, 0)
    model.reactions.get_by_id("EX_fru(e)").bounds=(FruExLimit, FruExLimit)  # valor único, óptimo encontrado  //  PONER SIEMPRE EL MISMO NÚMERO
    cobra.io.save_matlab_model(model,'iEC1364_W_p_coumaratemod_tmp.mat')
    
    # pCUMARATO
    # ======================
    model.reactions.get_by_id('TAL').bounds=(0,1000)
    pCALimit=dictOptValuepCA['EX_T4hcinnm(e)']['maximum']
    model.reactions.get_by_id('T4HCINNMtpp').bounds=(pCALimit,1000)
    model.reactions.get_by_id('T4HCINNMtex').bounds=(pCALimit,1000)
    model.reactions.get_by_id('EX_T4hcinnm(e)').bounds=(pCALimit,pCALimit)  # valor único, óptimo encontrado  //  PONER SIEMPRE EL MISMO NÚMERO
    cobra.io.save_matlab_model(model,'iEC1364_W_p_coumaratemod_tmp.mat')
    # -------------------------------------------------------------------------
    
    model.optimize()
    cobra.io.save_matlab_model(model,'iEC1364_W_p_coumaratemod_tmp.mat')
    del(model)                                    
    
    
    # =========================================================================
    # MODEL ADAPTATION TO THE PARAMETERS PASSED TO THE 'EcoliPputidaFLYCOP_oneConf' function
    # P. putida
    
    model=cobra.io.load_matlab_model('ModelsInput/iJN1463_naringeninB12_tmp.mat')
    # model.objective = "BIOMASS_KT2440_Core2"  # Cambiar el objetivo del modelo para optimizar biomasa (core), un objetivo realista
    model.objective = "BIOMASS_KT2440_WT3"  # WT, en lugar de 'core'  - asegurar objetivo biomasa (clave)
    
    # This reaction ('EX_fru(e)') controls the global fru exchange flux for P. putida KT
    model.reactions.get_by_id("EX_fru(e)").bounds=(frc2, 0)
    # The rest of reactions depend on the 'fru' flux already specified
    model.reactions.get_by_id("FRUtex").bounds=(0, 1000)   # fru[e] --> fru[p]
    model.reactions.get_by_id("FRUptspp").bounds=(0, 1000)   # fru[p] + pep[c] --> f1p[c] + pyr[c]
    model.optimize()
    
    # -------------------------------------------------------------------------
    # FLUX VARIABILITY ANALYSIS: optimizar producción de NARINGENINA al tiempo que crece P. putida KT (objective: BIOMASS_WT)
    # Excretar naringenina aunque se pierda una parte de la capacidad de crecimiento máximo (obj.: BIOMASS) == 15% sobre objetivo global  // David (jupyter notebook, en definición de modelo)
    dictNarValue=cobra.flux_analysis.variability.flux_variability_analysis(model,{'EX_nar(e)'},fraction_of_optimum=(1 - 0.15))  # EXCRECIÓN NARINGENINA
    NarLimit=dictNarValue['EX_nar(e)']['maximum']
    model.reactions.get_by_id('matB').bounds=(0, NarLimit)
    model.reactions.get_by_id('naringenintpp').bounds=(NarLimit,1000)
    model.reactions.get_by_id('naringenintex').bounds=(NarLimit,1000)
    model.reactions.get_by_id('EX_nar(e)').bounds=(NarLimit,NarLimit)  # PONER SIEMPRE EL MISMO NÚMERO
    # -------------------------------------------------------------------------
    
    model.optimize()
    cobra.io.save_matlab_model(model,'iJN1463_naringeninB12_tmp.mat')
    del(model)
    
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
    # MAT to COMETS
    mat_to_comets('iEC1364_W_p_coumaratemod_tmp.mat')
    mat_to_comets('iJN1463_naringeninB12_tmp.mat')
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
    # Community parameter modifications
    # =================================            
    # 4.- [shell script] Write automatically the COMETS parameter about initial biomass of strains // Initial biomass --> parameter subject to optimization (.pcs)
    massedit.edit_files(['EcPp2_layout_template2.txt'],["re.sub(r'XXX','"+str(Ecbiomass)+"',line)"], dry_run=False)  # dry_run = False --> guardar archivo modificado // True, mostrar diferencias. En ese caso, ¿guarda?
    massedit.edit_files(['EcPp2_layout_template2.txt'],["re.sub(r'YYY','"+str(KTbiomass)+"',line)"], dry_run=False)
  # end-if building models
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------


  # [COMETS by command line] Run COMETS
  if not(os.path.exists('IndividualRunsResults')):
    os.makedirs('IndividualRunsResults')
  totfitness=0
  sumpCA=0  # pCA quantity variable (production by E. coli)
  sumNar=0  # Nar quantity variable (production by P.putida KT)
  fitnessList=[]  # List with the different values for 'totfitness' in every execution ('n' repeats)
  
  # path=os.getcwd()
  # print(path)
  # print("\n---------------------------")
  for i in range(repeat):
        with open("output.txt", "w") as f:
            subprocess.run(args=['./comets_scr', 'comets_script_template'], stdout=f, stderr=subprocess.STDOUT)  # ejecutar COMETS con layout --> media_log_template / total_biomass_log_template / flux_log_template
            
        # [R call] Run script to generate one graph:subprocess.call
        title=str(sucr1)+'_'+str(Ecbiomass)+'_'+str(frc2)+'_'+str(KTbiomass)  
        # print(title)
        
        subprocess.run(['../../Scripts/plot_biomassX2_vs_4mediaItem_modGS_limNut.sh template2 sucr T4hcinnm fru nar nh4 pi '+str(maxCycles)+' '+title+' blue black darkmagenta yellow orange aquamarine EcoliWT KT2440'], shell=True)
                                                                                           #  3    4        5   6   7   8                                                                               Green   Red
        
        # Compute fitness (measure to optimize):
        # (A) DETERMINE ENDCYCLE: when sucrose is exhausted {}
        with open("biomass_vs_sucr_T4hcinnm_fru_nar_nh4_pi_template2.txt", "r") as sources: # Creado en ejecución COMETS 'subprocess.run()'
            lines = sources.readlines()                                                            
            iniPointV=lines[0].split()  # Initial line, initial values                                                          
            iniBiomass=float(iniPointV[1])+float(iniPointV[2])  # Biomass sum: Ecbiomass + KTbiomass
            endCycle=0
            
            # Endcycle occurs when sucrose is exhausted. Otherwise, 'endcycle' = last cycle
            for line in lines:
                sucrConc=float(line.split()[3])
                endCycle=int(line.split()[0])
                if sucrConc == float(0.0):
                    break;
            
        # (B) FINAL BIOMASS // FINAL CONCENTRATIONS: pCA, Nar, limiting nutrients
        finalLineV=lines[endCycle].split()  # Line where the 'endcycle' is reached // Either sucrConc = 0.0, either encycle = last_cycle
        final_Ecbiomass = float(finalLineV[1])
        final_KTbiomass = float(finalLineV[2])
        
        totpCA=float(finalLineV[4])  
        totNar=float(finalLineV[6])
        Final_nh4=float(finalLineV[7])  # First limiting nutrient
        Final_pi=float(finalLineV[8])  # Second limiting nutrient
        
        # PRINTING
        print("Execution: "+str(i+1)+" of "+str(repeat)+". CYCLE: "+str(endCycle))
        print("Final line: ", finalLineV, " Final cycle: ", endCycle)
        print("T4hcinnm: "+str(totpCA)+"\t\t"+"Nar: "+str(totNar))
        print("Final Ec biomass: ", final_Ecbiomass, "\tFinal KT biomass: ", final_KTbiomass)
        finalBiomass = final_Ecbiomass + final_KTbiomass
        
        # (C) COMPUTE FITNESS: maximize pCA AND/OR Nar
        fitTime=1-(float(endCycle)/float(maxCycles))  # maxCycles == Number of total cycles, stated in the layout_template
        fitpCA=float(totpCA/final_Ecbiomass)  # Normalized with respect to the final E.coli biomass (mM / g biomasa)
        fitNar=float(totNar/final_KTbiomass)  # Normalized with respect to the final P.putida KT biomass (mM / g biomasa)
        
        # PENDIENTE PRECISAR
        fitness=fitNar

        print("Fitness: "+str(round(fitness,6))+" in cycle "+str(endCycle), "\n")

        totfitness += fitness  # 'n' repeats
        fitnessList.append(fitness)  # List with fitness values in 'n' repeats
        sumpCA += totpCA  # Total pCA for 'n' repeats
        sumNar += totNar  # Total Nar for 'n' repeats

        # ---------------------------------------------------------------------
        # Copy individual solution
        file='IndividualRunsResults/'+'biomass_vs_sucr_T4hcinnm_fru_nar_nh4_pi_run'+str(i+1)+'_'+str(fitness)+'_'+str(endCycle)+'.pdf'
        shutil.move('biomass_vs_sucr_T4hcinnm_fru_nar_nh4_pi_template2_plot.pdf',file)        
        if(dirPlot != ''):
            file2=dirPlot+'biomass_vs_sucr_T4hcinnm_fru_nar_nh4_pi'+str(sucr1)+'_'+str(Ecbiomass)+'_'+str(frc2)+'_'+str(KTbiomass)+'_run'+str(i+1)+'_'+str(fitness)+'_'+str(endCycle)+'.pdf'
            shutil.move(file,file2)
            
        file='IndividualRunsResults/'+'total_biomass_log_run'+str(i+1)+'.txt'
        shutil.move('total_biomass_log_template2.txt',file)
        file='IndividualRunsResults/'+'media_log_run'+str(i+1)+'.txt'
        shutil.move('media_log_template2.txt',file)
        file='IndividualRunsResults/'+'flux_log_run'+str(i+1)+'.txt'
        shutil.move('flux_log_template2.txt',file)   

  avgfitness=totfitness/repeat  # 'totfitness' average in 'n' repeats
  if(repeat>1):
      sdfitness=statistics.stdev(fitnessList)  # standard deviations for 'n' values
  else:
      sdfitness=0.0
      
  avgpCA = sumpCA/repeat
  avgNar = sumNar/repeat
  # --------------------------------------------------------------------------- 
  # Display results in terminal
  print("Fitness_function\tconfiguration\t\tfitness\t\tsd\t\tpCA(mM)\tFinalEc(gL-1)\tNar(mM)\tFinalKT(gL-1)\tendCycle")  # UNITS: mM (metabolites)  //  gL-1 (biomass)
  
  print(fitFunc+"\t\t"+str(sucr1)+','+str(Ecbiomass)+','+str(frc2)+','+str(KTbiomass)+"\t"+
        str(round(avgfitness,6))+"\t\t"+str(round(sdfitness, 6))+
        "\t"+str(round(avgpCA,6))+"\t\t"+str(round(final_Ecbiomass, 4))+"\t\t"+str(round(avgNar,6))+"\t"+str(round(final_KTbiomass, 4))+"\t"+str(endCycle)+"\n")
    
  
  # Save results in 'configurationsResults(...).txt' file
  if not os.path.isfile(dirPlot+"configurationsResults"+fitFunc+".txt"): 
      myfile = open(dirPlot+"configurationsResults"+fitFunc+".txt", "a")
      myfile.write("Fitness_function\tconfiguration\tfitness\tsd\tpCA_mM\tFinalEc_gL\tNar_mM\tFinalKT_gL\tendCycle\tNH4_mM\tpi_mM\n")
      
      myfile.write(fitFunc+"\t"+str(sucr1)+','+str(Ecbiomass)+','+str(frc2)+','+str(KTbiomass)+
                   "\t"+str(round(avgfitness, 6))+"\t"+str(round(sdfitness, 6))+
                   "\t"+str(round(avgpCA, 6))+"\t"+str(round(final_Ecbiomass, 4))+"\t"+str(round(avgNar,6))+"\t"+str(round(final_KTbiomass, 4))+"\t"+str(endCycle)+
                   "\t"+str(round(Final_nh4, 4))+"\t"+str(round(Final_pi, 4))+"\n")
      myfile.close()
  
  else:
      myfile = open(dirPlot+"configurationsResults"+fitFunc+".txt", "a")
      
      myfile.write(fitFunc+"\t"+str(sucr1)+','+str(Ecbiomass)+','+str(frc2)+','+str(KTbiomass)+
                   "\t"+str(round(avgfitness, 6))+"\t"+str(round(sdfitness, 6))+
                   "\t"+str(round(avgpCA, 6))+"\t"+str(round(final_Ecbiomass, 4))+"\t"+str(round(avgNar,6))+"\t"+str(round(final_KTbiomass, 4))+"\t"+str(endCycle)+
                   "\t"+str(round(Final_nh4, 4))+"\t"+str(round(Final_pi, 4))+"\n")
      myfile.close()
      
      
  print("Avg.fitness(sd): "+str(avgfitness)+"  (+/-"+str(sdfitness)+")")
  if(sdfitness>(0.1 * avgfitness)):  # Correction if SD is too high. Maximum allowed SD ~ 10% (avgfitness)
      avgfitness=0.0
      
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# MODEL SUMMARY
  model = cobra.io.load_matlab_model('iEC1364_W_p_coumaratemod_tmp.mat')
  model.optimize()
  print("\nMODEL SUMMARY E. coli")
  print(model.summary())
  print()
  del(model)
    
  model = cobra.io.load_matlab_model('iJN1463_naringeninB12_tmp.mat')
  model.optimize()
  print("\nMODEL SUMMARY KT")
  print(model.summary())
  print()
  del(model)
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
  
  return avgfitness,sdfitness
# end-def EcoliPputidaOneConf
################################################################




