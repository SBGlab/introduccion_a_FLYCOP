#!/usr/bin/python

###############################################################################
# SCRIPT DESCRIPTION   
###############################################################################
"""
EcPp3 - Glycosilation project
Series of utilities, namely:
    
    - Initialize models:
        * initialize_models_iEC1364_W_p_coumarate function
        * initialize_models_iEC1364_W_unique_nar7glu function
        * initialize_models_iJN1463_narB12 function
    - mat_to_comets function
    - dead_biomass_tracking function
    - EcoliPputidaFLYCOP_oneConf

"""
# -----------------------------------------------------------------------------


# MODULES
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
# -----------------------------------------------------------------------------




###############################################################################
# FUNCTIONS to individually initialize GEM models   
###############################################################################

def initialize_models_iEC1364_W_p_coumarate():
 # Only to run 1st time, to build the model!
 if not(os.path.exists('ModelsInput/iEC1364_W_p_coumarate.xml')):
     print('ERROR! Not iEC1364_W_p_coumarate.xml file with GEM in ModelsInput!')
 else:
  path=os.getcwd()  # original path == "MicrobialCommunities"
  os.chdir('ModelsInput')
  
  # ---------------------------------------------------------------------------
  # E. coli W for taking sucrose and excreting fructose and T4hcinnm
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
  cobra.io.save_matlab_model(model,"iEC1364_W_p_coumarate.mat")
  del(model)
  model = cobra.io.load_matlab_model("iEC1364_W_p_coumarate.mat")
  
  # Replace brackets with compartment location (e.g. "[c]") in rxn ids by '_' (e.g. "_c") 
  for rxn in model.reactions:
    rxn.id = re.sub('__40__p__41__',r'(p)',rxn.id)
    rxn.id = re.sub('__40__c__41__',r'(c)',rxn.id)
    rxn.id = re.sub('__40__e__41__',r'(e)',rxn.id)    
  # To solve possible problems in changing names     
  model.repair()
  cobra.io.save_matlab_model(model,"iEC1364_W_p_coumarate.mat")
  del(model)
  model = cobra.io.load_matlab_model("iEC1364_W_p_coumarate.mat")
  
  
  # MODEL ADJUSTEMENTS
  # ==================
  # Avoid glucose exchange (although there is no glucose in the original media)
  model.reactions.get_by_id("EX_glc__D(e)").bounds = (0,0)
  # Put sucrose as carbon source and maximize uptake, later changed by the parameter 'sucr1'
  model.reactions.get_by_id("EX_sucr(e)").bounds=(-15,0)
  # OXYGEN UPTAKE
  model.reactions.get_by_id("EX_o2(e)").bounds = (-20, 0)
  
  # NITROGEN UPTAKE
  # Uptake rate for NH4, later changed by NH4_Ec parameter
  model.reactions.get_by_id("EX_nh4(e)").bounds = (-15, 1000)
  # PHOSPHATE UPTAKE
  model.reactions.get_by_id("EX_pi(e)").bounds = (-10, 1000)  
  
  # MAKE SURE FRUCTOSE METABOLISM IS SHUTTED DOWN
  model.reactions.get_by_id("XYLI2").bounds = (0, 0)
  model.reactions.get_by_id("HEX7").bounds = (0, 0)  
  model.reactions.get_by_id("FRUpts2pp").bounds = (0, 0)
  model.reactions.get_by_id("FRUptspp").bounds = (0, 0)
  
  
  # ACTIVATED REACTION: FFSD: h2o[c] + suc6p[c] --> fru[c] + g6p[c] (sucrose hydrolysis)
  model.reactions.get_by_id("FFSD").bounds = (0, 1000)
  
  # To un-limit the fructose production, for the flux variability analysis
  model.reactions.get_by_id('FRUtpp').bounds=(-1000,1000)  
  model.reactions.get_by_id('FRUtex').bounds=(-1000,1000)  
  model.reactions.get_by_id('EX_fru(e)').bounds=(-1000,1000)
  
  # B12 auxotrophy: control / dependence with P.putida KT2440
  model.reactions.ADOCBLS.bounds=(0,0)
  
  # Optimize T4hcinnm production from tyrosine
  model.reactions.get_by_id('TAL').bounds=(0,1000)  # TAL: tyr_L[c] --> T4hcinnm[c] + nh4[c]
  
  
  # SAVE MODEL (tmp)
  cobra.io.save_matlab_model(model,"iEC1364_W_p_coumarate_tmp.mat")
  del(model)
  os.chdir(path)


# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
  
  
def initialize_models_iEC1364_W_unique_nar7glu():
 # Only to run 1st time, to build the model!
 if not(os.path.exists('ModelsInput/iEC1364_W_unique_nar7glu.xml')):
     print('ERROR! Not iEC1364_W_unique_nar7glu.xml file with GEM in ModelsInput!')
 else:
  path=os.getcwd()  # original path == "MicrobialCommunities"
  os.chdir('ModelsInput')
  
  # ---------------------------------------------------------------------------
  # E. coli W for glycosilating naringenin
  # ---------------------------------------------------------------------------
  model=cobra.io.read_sbml_model("iEC1364_W_unique_nar7glu.xml")
  
  # Replace brackets with compartment location (e.g. "[c]") in metabolite ids by '_' (e.g. "_c") 
  for metabolite in model.metabolites:
    metabolite.id = re.sub('__91__c__93__',r'[c]',metabolite.id)
    metabolite.id = re.sub('__91__p__93__$',r'[p]',metabolite.id)
    metabolite.id = re.sub('__91__e__93__',r'[e]',metabolite.id)
    # metabolite.id = re.sub('__',r'_',metabolite.id)
    metabolite.compartment = ''
  # To solve possible problems in changing names     
  model.repair()
  cobra.io.save_matlab_model(model,"iEC1364_W_unique_nar7glu.mat")
  del(model)
  model = cobra.io.load_matlab_model("iEC1364_W_unique_nar7glu.mat")
  
  # Replace brackets with compartment location (e.g. "[c]") in rxn ids by '_' (e.g. "_c") 
  for rxn in model.reactions:
    rxn.id = re.sub('__40__p__41__',r'(p)',rxn.id)
    rxn.id = re.sub('__40__c__41__',r'(c)',rxn.id)
    rxn.id = re.sub('__40__e__41__',r'(e)',rxn.id)    
  # To solve possible problems in changing names     
  model.repair()
  cobra.io.save_matlab_model(model,"iEC1364_W_unique_nar7glu.mat")
  del(model)
  model = cobra.io.load_matlab_model("iEC1364_W_unique_nar7glu.mat")
  
  
  # MODEL ADJUSTEMENTS
  # ==================
  # Avoid glucose exchange (although there is no glucose in the original media)
  model.reactions.get_by_id("EX_glc__D(e)").bounds = (0,0)
  # Put sucrose as carbon source and maximize uptake, later changed by the parameter 'sucr1'
  model.reactions.get_by_id("EX_sucr(e)").bounds=(-15,0)
  # OXYGEN UPTAKE
  model.reactions.get_by_id("EX_o2(e)").bounds = (-20, 0)
  
  # NITROGEN UPTAKE
  # Uptake rate for NH4, later changed by NH4_Ec parameter
  model.reactions.get_by_id("EX_nh4(e)").bounds = (-15, 1000)
  # PHOSPHATE UPTAKE
  model.reactions.get_by_id("EX_pi(e)").bounds = (-10, 1000)  
  
  # FRUCTOSE METABOLISM IS ACTIVATED AGAIN FOR THE GLYCOSILATOR STRAIN E. coli W 
  model.reactions.get_by_id("XYLI2").bounds = (0, 0)  # AVOID: XYLI2: glc_D[c] <=> fru[c] (we want just fructose metabolism)
  
  model.reactions.get_by_id("HEX7").bounds = (-1000, 1000)  # HEX7: atp[c] + fru[c] <=> adp[c] + f6p[c] + h[c]
  model.reactions.get_by_id("FRUpts2pp").bounds = (-1000, 1000)  # FRUpts2pp: fru[p] + pep[c] <=> f6p[c] + pyr[c]
  model.reactions.get_by_id("FRUptspp").bounds = (-1000, 1000)  # FRUptspp: fru[p] + pep[c] <=> f1p[c] + pyr[c]
  
  # ACTIVATED REACTION: FFSD: h2o[c] + suc6p[c] --> fru[c] + g6p[c] (sucrose hydrolysis)
  model.reactions.get_by_id("FFSD").bounds = (0, 1000)
  
  # AVOID FRUCTOSE SECRETION
  model.reactions.get_by_id('FRUtpp').bounds=(0,0)  
  model.reactions.get_by_id('FRUtex').bounds=(0,0)  
  model.reactions.get_by_id('EX_fru(e)').bounds=(0,0)
  
  # B12 auxotrophy: control / dependence with P.putida KT2440
  model.reactions.ADOCBLS.bounds=(0,0)
  
  # SHUT DOWN T4hcinnm METABOLISM
  model.reactions.get_by_id('TAL').bounds=(0,0)  # TAL: tyr_L[c] --> T4hcinnm[c] + nh4[c]
  model.reactions.get_by_id('T4HCINNMtpp').bounds=(0,0)  # T4HCINNMtpp:  T4hcinnm[c] --> T4hcinnm[p]
  model.reactions.get_by_id('T4HCINNMtex').bounds=(0,0)  # T4HCINNMtex:  T4hcinnm[p] --> T4hcinnm[e]
  model.reactions.get_by_id('EX_T4hcinnm(e)').bounds=(0,0)  # EX_T4hcinnm(e):  T4hcinnm[e] --> 
  
  
  
  # NARINGENIN RELATED-REACTIONS
  # ----------------------------
  # Naringenin uptake by E.coli
  model.reactions.get_by_id("naringenintpp").bounds = (-1000, 0)  # naringenintpp: nar[c] <-- nar[p]
  model.reactions.get_by_id("naringenintex").bounds = (-1000, 0)  # naringenintex: nar[p] <-- nar[e]
  model.reactions.get_by_id("EX_nar(e)").bounds = (-1000, 0)  # EX_nar(e): nar[e] <--

  # Naringenin glycosilation
  model.reactions.get_by_id("DE_FLVA7GT1_FR").bounds = (0, 1000)  # DE_FLVA7GT1_FR: nar[c] + udpg[c] --> h[c] + nar7glu[c] + udp[c]

  # Naringenin export, previous to FVA
  model.reactions.get_by_id("nar7glu_tpp").bounds = (0, 1000)  # nar7glu_tpp: nar7glu[c] --> nar7glu[p]
  model.reactions.get_by_id("nar7glu_tex").bounds = (0, 1000)  # nar7glu_tex: nar7glu[p] --> nar7glu[e]
  
  # SAVE MODEL (tmp)
  cobra.io.save_matlab_model(model,"iEC1364_W_unique_nar7glu_tmp.mat")
  del(model)
  os.chdir(path)


# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
  
  
def initialize_models_iJN1463_narB12():
 # Only to run 1st time, to build the model!
 if not(os.path.exists('ModelsInput/iJN1463_naringeninB12.xml')):
     print('ERROR! Not iJN1463_naringeninB12.xml file with GEM in ModelsInput!')
 else:
  path=os.getcwd()  # original path == "MicrobialCommunities"
  os.chdir('ModelsInput')
  
  # ---------------------------------------------------------------------------
  # P.putida KT 2440 model for taking fructose and secreting B12
  # ---------------------------------------------------------------------------
  model=cobra.io.read_sbml_model('iJN1463_naringeninB12.xml')

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
  
  
  # MODEL ADJUSTEMENTS
  # ==================
  # This model cannot take sucrose from media: model.reactions.get_by_id("EX_sucr(e)").bounds = (0, 0)  
  
  # FRU reactions
  model.reactions.get_by_id("EX_fru(e)").bounds=(-15,0)  # Maximize uptake, maximum upper bound. Later changed by the parameter 'frc2'
  model.reactions.get_by_id("FRUtex").bounds = (0, 1000)

  # PREVENT P.putidaKT FROM TAKING glc[e] from the media
  model.reactions.get_by_id("EX_glc__D(e)").bounds = (0, 0)
  # OXYGEN UPTAKE
  model.reactions.get_by_id("EX_o2(e)").bounds = (-20, 0)
  
  # NITROGEN UPTAKE
  model.reactions.get_by_id("EX_nh4(e)").bounds = (-12, 1000)  # Later changed by NH4_KT parameter 
  # PHOSPHATE UPTAKE 
  model.reactions.get_by_id("EX_pi(e)").bounds = (-10, 1000)
  
  # pCOUMARATE UPTAKE
  model.reactions.get_by_id("EX_T4hcinnm(e)").bounds = (-1000, 0)
  model.reactions.get_by_id("T4HCINNMtex").bounds = (0, 1000)
  model.reactions.get_by_id("T4HCINNMtpp").bounds = (0, 1000)
  model.reactions.get_by_id("4CMCOAS").bounds = (0, 0)  # T4hcinnm[c] + atp[c] + coa[c] --> amp[c] + coucoa[c] + ppi[c]
  
  # MALON reactions - no MALON secretion
  model.reactions.get_by_id("EX_malon(e)").bounds = (0, 0)
  model.reactions.get_by_id("MALONtex").bounds = (0, 0)
  model.reactions.get_by_id("MALONpp").bounds = (0, 0)
  model.reactions.get_by_id("MALONHY").bounds = (0, 0)  # Reacción de hidrólisis de malcoa[c] --> malon[c]
        
  # NARINGENIN PRODUCTION reactions - optimize production
  model.reactions.get_by_id("matB").bounds = (0, 1000)
  model.reactions.get_by_id("AS_C_4CMCOAS_FR").bounds = (0, 1000)
  model.reactions.get_by_id("AS_C_CHALS1_FR").bounds = (0, 1000)
  model.reactions.get_by_id("AS_CHALIS1_FR").bounds = (0, 1000)
  
  # PROMOTE NARINGENIN SECRETION 
  # -------------------------------------------------------------------------
  model.reactions.get_by_id("EX_nar(e)").bounds = (0, 1000)  # EX_nar(e): nar[e] -->
  model.reactions.get_by_id("naringenintex").bounds = (0, 1000)  # naringenintex: nar[p] --> nar[e]
  model.reactions.get_by_id("naringenintpp").bounds = (0, 1000)  # naringenintpp: nar[c] --> nar[p]
  
  # SAVE MODEL (tmp)
  cobra.io.save_matlab_model(model,"iJN1463_naringeninB12_tmp.mat")
  del(model)
  os.chdir(path)
  
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
###############################################################################




###############################################################################   
### FUNCTION mat_to_comets ####################################################    
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
###############################################################################




###############################################################################    
### FUNCTION dead_biomass_tracking  ###########################################
# Dead Tracking within the community simulation: 
# if biomass of any strain (or both strains) decreases during more than 'n_cycles' consecutive cycles
# -----------------------------------------------------------------------------
def dead_biomass_tracking(COMETS_file, endCycle, n_cycles = 10):
    CometsTable = pd.read_csv(COMETS_file, sep="\t", header=None)
    
    biomass_track = 0
    count_cons_cycles = 0
    initial_dead = 0
    
    # The endcycle can occur when the substrate (sucrose) is finally exhausted, which might not always happen in the last cycle
    # cycles_number = len(CometsTable) - 1 # Lenght: 241 (initial row + 240 cycles)    
    
    for row in CometsTable.itertuples():  # Note tuple 241 = cycle 240; tuple 0 = initial situation
        cycle = row[1]
        
        if cycle == 0:
            last_biomass1 = row[2]
            last_biomass2 = row[3]
            
        else:
            biomass1 = row[2]
            biomass2 = row[3]
                
            if ((biomass1 - last_biomass1) < 0) or ((biomass2 - last_biomass2) < 0):  # cannot distinguish between the microbe experiencing biomass loss
                count_cons_cycles += 1                                                # might be just one or both
                last_dead = cycle
                
            else:
                count_cons_cycles = 0
                
            last_biomass1 = row[2]
            last_biomass2 = row[3]
                
        if count_cons_cycles > 10 and not biomass_track:
            biomass_track = 1
            initial_dead = last_dead - count_cons_cycles
            
                
    if biomass_track:
        dead_cycles = str(initial_dead)+"-"+str(last_dead)     
        return biomass_track, dead_cycles
            
    else:
        return biomass_track, "NoDeadTracking"
    
# -----------------------------------------------------------------------------
### FUNCTION dead_biomass_tracking
###############################################################################




###############################################################################
### FUNCTION EcoliPputidaOneConf ##############################################
def EcoliPputidaFLYCOP_oneConf(sucr1, Ecbiomass, Ecbiomass_glyc, frc2, KTbiomass, nh4_Ec, nh4_KT, fitFunc='MaxNaringenin', maxCycles = 240, dirPlot='', repeat=5):  
  '''
  Call: avgFitness, sdFitness = EcoliPputidaFLYCOP_oneConf(sucr1, Ecbiomass, Ecbiomass_glyc, frc2, KTbiomass, nh4_Ec, nh4_KT)
  Start with no more than 5 repeats (1st trial)

  INPUTS: sucr1: lower bound of sucrose uptake in model 1 (E.coli) (mM)
          Ecbiomass: initial E. coli biomass (gL-1) for the base model
          Ecbiomass_glyc: initial E. coli biomass (gL-1) for the glycosilator strain
          frc2: lower bound of fructose uptake in model 2 (P.putida) (mM)
          KTbiomass: initial P. putida KT biomass (gL-1)
          nh4_Ec: lower bound of nh4 uptake in model 1 (E.coli) (mM)
          nh4_KT: lower bound of nh4 uptake in model 2 (P.putida) (mM)
          
          fitFunc: fitness function to optimize. 'MaxNaringenin', maximize Naringenin production by P. putida KT2440 (mM)
                                                 
          maxCycles: cycles in COMETS run, stated in file 'layout_template'. It is not used in the Python scripts (wrapper, individualTest). If desired to change, see 'layout_template'
          dirPlot: copy of the plots with several run results.
          repeat: number of runs with the same configuration (COMETS, not number of SMAC iterations)
          
          Other nutrients to be tracked: O2.
          
  OUTPUT: avgFitness: average fitness of 'repeat' COMETS runs with the same configuration (due to it is not deterministic)
          sdFitness: standard deviation of fitness during 'repeat' COMETS runs (see above)
  '''

  if not(os.path.exists('ModelsInput/iEC1364_W_unique_nar7glu_tmp.mat')): # or os.path.exists('ModelsInput/iJN1463_naringeninB12_tmp.mat')): 
      initialize_models_iEC1364_W_p_coumarate()
      initialize_models_iEC1364_W_unique_nar7glu()
      initialize_models_iJN1463_narB12()
      print("Inicializamos modelos\n")

  print("Fitness function: ", fitFunc)


  # Single GEMs parameter modifications
  # ===================================  
  if not(os.path.exists('iEC1364_W_p_coumarate_tmp.mat.txt')) or not (os.path.exists('iEC1364_W_unique_nar7glu_tmp.mat.txt')) or not (os.path.exists('iJN1463_naringeninB12_tmp.mat.txt')):
    
    # ========================================================================= 
    # MODEL ADAPTATION TO THE PARAMETERS PASSED TO THE 'EcoliPputidaFLYCOP_oneConf' function
    # E. coli W: iEC1364_W_p_coumarate
    
    model=cobra.io.load_matlab_model('ModelsInput/iEC1364_W_p_coumarate_tmp.mat')
    model.objective = "BIOMASS_Ec_iJO1366_WT_53p95M"  # WT, instead of 'core'
    
    # This reaction ('EX_sucr(e)') controls the global sucr exchange flux for E. coli W
    model.reactions.get_by_id("EX_sucr(e)").bounds=(sucr1, 0)
    # The rest of reactions depend on the sucr flux already specified
    model.reactions.get_by_id("SUCtpp").bounds=(0, 1000)  # sucr[p] --> sucr[c]  
    model.reactions.get_by_id("SUCRtpp").bounds=(0, 1000)  # sucr[p] --> sucr[c]
    model.reactions.get_by_id("SUCRtex").bounds=(0, 1000)  # sucr[e] --> sucr[p]
    model.optimize()
    
    # NH4 uptake rate
    model.reactions.get_by_id("EX_nh4(e)").bounds=(nh4_Ec, 0)

    
    # -------------------------------------------------------------------------
    # FLUX VARIABILITY ANALYSIS: pCA, fructose. 20% over global objective (optimize biomass production)
    dictOptValueFru = cobra.flux_analysis.flux_variability_analysis(model, {'EX_fru(e)'}, fraction_of_optimum=(1-0.20))
    dictOptValuepCA = cobra.flux_analysis.flux_variability_analysis(model, {'EX_T4hcinnm(e)'}, fraction_of_optimum=((1-0.20)))
   
    
    # FRUCTOSA
    # ======================
    FruExLimit=dictOptValueFru['EX_fru(e)']['maximum']
    model.reactions.get_by_id("FRUtpp").bounds=(0, FruExLimit)
    model.reactions.get_by_id("FRUtex").bounds=(-FruExLimit, 0)
    model.reactions.get_by_id("EX_fru(e)").bounds=(FruExLimit, FruExLimit)  
    
    
    # pCUMARATO
    # ======================
    pCALimit=dictOptValuepCA['EX_T4hcinnm(e)']['maximum']
    model.reactions.get_by_id('T4HCINNMtpp').bounds=(pCALimit,1000)
    model.reactions.get_by_id('T4HCINNMtex').bounds=(pCALimit,1000)
    model.reactions.get_by_id('EX_T4hcinnm(e)').bounds=(pCALimit,pCALimit)  
    
    
    cobra.io.save_matlab_model(model,'iEC1364_W_p_coumarate_tmp.mat')
    # -------------------------------------------------------------------------
    
    model.optimize()
    cobra.io.save_matlab_model(model,'iEC1364_W_p_coumarate_tmp.mat')
    del(model)                                    
    # =========================================================================
    # =========================================================================
    
    
    
    # ========================================================================= 
    # MODEL ADAPTATION TO THE PARAMETERS PASSED TO THE 'EcoliPputidaFLYCOP_oneConf' function
    # E. coli W: iEC1364_W_unique_nar7glu
    
    model=cobra.io.load_matlab_model('ModelsInput/iEC1364_W_unique_nar7glu_tmp.mat')
    model.objective = "BIOMASS_Ec_iJO1366_WT_53p95M"  # WT, instead of 'core'
    
    # This reaction ('EX_sucr(e)') controls the global sucr exchange flux for E. coli W
    model.reactions.get_by_id("EX_sucr(e)").bounds=(sucr1, 0)
    # The rest of reactions depend on the sucr flux already specified
    model.reactions.get_by_id("SUCtpp").bounds=(0, 1000)  # sucr[p] --> sucr[c]  
    model.reactions.get_by_id("SUCRtpp").bounds=(0, 1000)  # sucr[p] --> sucr[c]
    model.reactions.get_by_id("SUCRtex").bounds=(0, 1000)  # sucr[e] --> sucr[p]
    model.optimize()
    
    # NH4 uptake rate
    model.reactions.get_by_id("EX_nh4(e)").bounds=(nh4_Ec, 0)

    
    # -------------------------------------------------------------------------
    # FLUX VARIABILITY ANALYSIS: glycosilated naringenin. 20% over global objective (optimize biomass production)
    dictOptValueglycnar = cobra.flux_analysis.flux_variability_analysis(model, {'EX_nar7glu(e)'}, fraction_of_optimum=((1-0.20)))
   
    # Glycosilated naringenin
    # =======================
    GlycNarLimit=dictOptValueglycnar['EX_nar7glu(e)']['maximum']
    model.reactions.get_by_id("nar7glu_tpp").bounds=(GlycNarLimit, 1000)  
    model.reactions.get_by_id("nar7glu_tex").bounds=(GlycNarLimit, 1000)  
    model.reactions.get_by_id("EX_nar7glu(e)").bounds=(GlycNarLimit, GlycNarLimit)  
    
    
    cobra.io.save_matlab_model(model,'iEC1364_W_unique_nar7glu_tmp.mat')
    # -------------------------------------------------------------------------
    
    model.optimize()
    cobra.io.save_matlab_model(model,'iEC1364_W_unique_nar7glu_tmp.mat')
    del(model)                                    
    # =========================================================================
    # =========================================================================
    
    
    
    # =========================================================================
    # MODEL ADAPTATION TO THE PARAMETERS PASSED TO THE 'EcoliPputidaFLYCOP_oneConf' function
    # P. putida KT2440: iJN1463_naringeninB12
    
    model=cobra.io.load_matlab_model('ModelsInput/iJN1463_naringeninB12_tmp.mat')
    model.objective = "BIOMASS_KT2440_WT3"  # WT, instead of core
    
    # This reaction ('EX_fru(e)') controls the global fru exchange flux for P. putida KT
    model.reactions.get_by_id("EX_fru(e)").bounds=(frc2, 0)
    # The rest of reactions depend on the 'fru' flux already specified
    model.reactions.get_by_id("FRUtex").bounds=(0, 1000)   # fru[e] --> fru[p]
    model.reactions.get_by_id("FRUptspp").bounds=(0, 1000)   # fru[p] + pep[c] --> f1p[c] + pyr[c]
    model.optimize()
    
    # NH4 uptake rate
    model.reactions.get_by_id("EX_nh4(e)").bounds=(nh4_KT, 0)

    
    # -------------------------------------------------------------------------
    # FLUX VARIABILITY ANALYSIS: naringenin. 20% over global objective (optimize biomass production)
    dictNarValue=cobra.flux_analysis.variability.flux_variability_analysis(model,{'EX_nar(e)'},fraction_of_optimum=(1 - 0.20))
    NarLimit=dictNarValue['EX_nar(e)']['maximum']
    
    model.reactions.get_by_id('matB').bounds=(0, NarLimit)
    model.reactions.get_by_id('naringenintpp').bounds=(NarLimit,1000)
    model.reactions.get_by_id('naringenintex').bounds=(NarLimit,1000)
    model.reactions.get_by_id('EX_nar(e)').bounds=(NarLimit,NarLimit)
    # -------------------------------------------------------------------------
    
    model.optimize()
    cobra.io.save_matlab_model(model,'iJN1463_naringeninB12_tmp.mat')
    del(model)
    # =========================================================================
    # =========================================================================
    
    
    
    # =========================================================================
    # MAT to COMETS
    mat_to_comets('iEC1364_W_p_coumarate_tmp.mat')
    mat_to_comets('iEC1364_W_unique_nar7glu_tmp.mat')
    mat_to_comets('iJN1463_naringeninB12_tmp.mat')
    # =========================================================================



    # Community parameter modifications
    # =================================            
    # 4.- [shell script] Write automatically the COMETS parameter about initial biomass of strains // Initial biomass --> parameter subject to optimization (.pcs)
    massedit.edit_files(['EcPp3_layout_template2.txt'],["re.sub(r'XXX','"+str(Ecbiomass)+"',line)"], dry_run=False)  # dry_run = False --> guardar archivo modificado
    massedit.edit_files(['EcPp3_layout_template2.txt'],["re.sub(r'YYY','"+str(Ecbiomass_glyc)+"',line)"], dry_run=False)
    massedit.edit_files(['EcPp3_layout_template2.txt'],["re.sub(r'ZZZ','"+str(KTbiomass)+"',line)"], dry_run=False)
  # end-of building models
  # ===========================================================================

  # ===========================================================================
  # [COMETS by command line] Run COMETS
  if not(os.path.exists('IndividualRunsResults')):
    os.makedirs('IndividualRunsResults')
  totfitness=0
  sum_Nar=0  # Naringenin quantity variable (production by P.putida KT)
  sum_glycNar=0  # Glycosilated naringenin quantity variable (production by E.coli W, glycosilator strain)
  fitnessList=[]  # List with the different values for 'totfitness' in every execution ('n' repeats)
  

  for i in range(repeat):
        with open("output.txt", "w") as f:
            subprocess.run(args=['./comets_scr', 'comets_script_template'], stdout=f, stderr=subprocess.STDOUT)
            
        # [R call] Run script to generate one graph:subprocess.call
        title=str(sucr1)+'_'+str(Ecbiomass)+'_'+str(Ecbiomass_glyc)+'_'+str(frc2)+'_'+str(KTbiomass)+'_'+str(nh4_Ec)+'_'+str(nh4_KT)
        subprocess.run(['../../Scripts/plot_biomassX2_vs_4mediaItem_glic.sh template2 sucr nar7glu fru nar nh4 pi o2 '+str(maxCycles)+' '+title+' blue black darkmagenta yellow orange aquamarine EcoliWT EcoliWT_glyc KT2440'], shell=True)
                                                                                           
        
        # Compute fitness (measure to optimize):
        # (A) DETERMINE ENDCYCLE: when sucrose is exhausted
        with open("biomass_vs_sucr_nar7glu_fru_nar_nh4_pi_o2_template2.txt", "r") as sources: # Creado en ejecución COMETS 'subprocess.run()'
            lines = sources.readlines()                                                            
            endCycle=0
            # iniPointV=lines[0].split()  # Initial line, initial values                                                          
            # iniBiomass=float(iniPointV[1])+float(iniPointV[2]+float(iniPointV[3])  # Biomass sum: Ecbiomass + Ecbiomass_glyc + KTbiomass
            
            # Endcycle occurs when either sucrose or NH4 are exhausted. Otherwise, 'endcycle' = last cycle
            for line in lines:
                sucrConc=float(line.split()[4])
                NH4conc=float(line.split()[8])
                endCycle=int(line.split()[0])
                if float(sucrConc) < 0.001 or float(NH4conc) < 0.001:  # Nunca llega a ser exactamente 0.0, habría que poner < 0.001 (por ejemplo, pero es adaptable)
                    break;  # ¿Columna que registre cuál de ambos nutrientes se agota?
            
            
        # (B) FINAL BIOMASS // FINAL CONCENTRATIONS: pCA, Nar, limiting nutrients
        finalLineV=lines[endCycle].split()  # Line where the 'endcycle' is reached // Either sucrConc = 0.0, either encycle = last_cycle
        final_Ecbiomass = float(finalLineV[1])
        final_Ecbiomass_glyc = float(finalLineV[2])
        final_KTbiomass = float(finalLineV[3])
        
        tot_glicNar=float(finalLineV[5])  # Final glycosilated naringenin (by E.coli)
        tot_Nar=float(finalLineV[7])  # Final Naringenin (by P.putida)
        Final_nh4=float(finalLineV[8])  # First limiting nutrient
        Final_pi=float(finalLineV[9])  # Second limiting nutrient
        Final_O2=float(finalLineV[10])  # Final O2
        
        # DEAD TRACKING
        biomass_track, dead_process = dead_biomass_tracking("biomass_vs_sucr_nar7glu_fru_nar_nh4_pi_o2_template2.txt", endCycle = endCycle, n_cycles = 10)
        # Pi OVERCONSUMPTION TRACKING
        # pi_overconsumption, pi_cycles = metabolite_tracking_overconsumption("biomass_vs_sucr_T4hcinnm_fru_nar7glu_nh4_pi_o2_template2.txt", 10.0, 9)  # Disabled utility
        
        # PRINTING
        print("Execution: "+str(i+1)+" of "+str(repeat)+". CYCLE: "+str(endCycle))
        print("Final line: ", finalLineV, " Final cycle: ", endCycle)
        print("Naringenin: "+str(tot_Nar)+"\t"+"Glycosilated Nar: "+str(tot_glicNar))
        print("Final Ec biomass: ", final_Ecbiomass, "\tFinal Ec_glyc biomass: ", final_Ecbiomass_glyc, "\tFinal KT biomass: ", final_KTbiomass)
        
        
        # (C) COMPUTE FITNESS: maximize pCA AND/OR Nar
        fitNar = tot_glicNar / (final_Ecbiomass + final_Ecbiomass_glyc + final_KTbiomass)  # Final glycosilated naringenin yield over global biomass (the three microbes)
        
        # PENDIENTE PRECISAR
        fitness=fitNar
        print("Fitness: "+str(round(fitness,6))+" in cycle "+str(endCycle), "\n")

        totfitness += fitness  # 'n' repeats
        fitnessList.append(fitness)  # List with fitness values in 'n' repeats
        sum_Nar += tot_Nar  # Total naringenin for 'n' repeats
        sum_glycNar += tot_glicNar  # Total glycosilated naringenin for 'n' repeats

        # ---------------------------------------------------------------------
        # Copy individual solution
        file='IndividualRunsResults/'+'biomass_vs_sucr_nar7glu_fru_nar_nh4_pi_o2_run'+str(i+1)+'_'+str(fitness)+'_'+str(endCycle)+'.pdf'
        shutil.move('biomass_vs_sucr_nar7glu_fru_nar_nh4_pi_o2_template2_plot.pdf',file)        
        if(dirPlot != ''):
            file2=dirPlot+'biomass_vs_sucr_nar7glu_fru_nar_nh4_pi_o2_'+title+'_run'+str(i+1)+'_'+str(fitness)+'_'+str(endCycle)+'.pdf'
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
      
  avgNar = sum_Nar/repeat
  avgglycNar = sum_glycNar/repeat
  # --------------------------------------------------------------------------- 
  # Display results in terminal
  print("Fitness_function\tBaseConfig\tfitFunc\tsd\tGlycNar(mM)\tNar(mM)\tFinalEc(gL-1)\tFinalEc_glyc(gL-1)\tFinalKT(gL-1)\n")  # UNITS: mM (metabolites)  //  gL-1 (biomass)
  
  print(fitFunc+"\t"+str(sucr1)+','+str(Ecbiomass)+','+str(Ecbiomass_glyc)+','+str(frc2)+','+str(KTbiomass)+","+str(nh4_Ec)+','+str(nh4_KT)+
        "\t"+str(round(avgfitness,6))+"\t"+str(round(sdfitness, 6))+
        "\t"+str(round(avgglycNar,6))+"\t"+str(round(avgNar, 6))+
        "\t"+str(round(final_Ecbiomass, 4))+"\t"+str(round(final_Ecbiomass_glyc, 4))+"\t"+str(round(final_KTbiomass, 4))+"\n")
    
  
  # Save results in 'configurationsResults(...).txt' file
  if not os.path.isfile(dirPlot+"configurationsResults"+fitFunc+".txt"): 
      myfile = open(dirPlot+"configurationsResults"+fitFunc+".txt", "a")
      myfile.write("Fitness_function\tBaseConfig\tfitFunc\tsd\tGlycNar_mM\tNar_mM\tFinalEc_gL\tFinalEc_glyc_gL\tFinalKT_gL\tendCycle\tNH4_mM\tpi_mM\tDeadTracking\tDT_cycles\tFinalSucr\tFinalO2\n")
      
      myfile.write(fitFunc+"\t"+str(sucr1)+','+str(Ecbiomass)+','+str(Ecbiomass_glyc)+','+str(frc2)+','+str(KTbiomass)+","+str(nh4_Ec)+','+str(nh4_KT)+
                   "\t"+str(round(avgfitness, 6))+"\t"+str(round(sdfitness, 6))+
                   "\t"+str(round(avgglycNar, 6))+"\t"+str(round(avgNar, 6))+
                   "\t"+str(round(final_Ecbiomass, 4))+"\t"+str(round(final_Ecbiomass_glyc,4))+"\t"+str(round(final_KTbiomass, 4))+"\t"+str(endCycle)+
                   "\t"+str(round(Final_nh4, 4))+"\t"+str(round(Final_pi, 4))+"\t"+str(biomass_track)+"\t"+dead_process+"\t"+str(sucrConc)+"\t"+str(Final_O2)+"\n")
      myfile.close()
  
  else:
      myfile = open(dirPlot+"configurationsResults"+fitFunc+".txt", "a")
      
      myfile.write(fitFunc+"\t"+str(sucr1)+','+str(Ecbiomass)+','+str(Ecbiomass_glyc)+','+str(frc2)+','+str(KTbiomass)+","+str(nh4_Ec)+','+str(nh4_KT)+
                   "\t"+str(round(avgfitness, 6))+"\t"+str(round(sdfitness, 6))+
                   "\t"+str(round(avgglycNar, 6))+"\t"+str(round(avgNar, 6))+
                   "\t"+str(round(final_Ecbiomass, 4))+"\t"+str(round(final_Ecbiomass_glyc,4))+"\t"+str(round(final_KTbiomass, 4))+"\t"+str(endCycle)+
                   "\t"+str(round(Final_nh4, 4))+"\t"+str(round(Final_pi, 4))+"\t"+str(biomass_track)+"\t"+dead_process+"\t"+str(sucrConc)+"\t"+str(Final_O2)+"\n")
      myfile.close()
      
      
  print("Avg.fitness(sd): "+str(avgfitness)+"  (+/-"+str(sdfitness)+")")
  if(sdfitness>(0.1 * avgfitness)):  # Correction if SD is too high. Maximum allowed SD ~ 10% (avgfitness)
      avgfitness=0.0
      
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# MODEL SUMMARY
  model = cobra.io.load_matlab_model('iEC1364_W_p_coumarate_tmp.mat')
  model.optimize()
  print("\nMODEL SUMMARY E. coli W (base)")
  print(model.summary())
  print()
  del(model)
  
  model = cobra.io.load_matlab_model('iEC1364_W_unique_nar7glu_tmp.mat')
  model.optimize()
  print("\nMODEL SUMMARY E. coli W (glycosilator strain)")
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
# end-of EcoliPputidaOneConf
###############################################################################








