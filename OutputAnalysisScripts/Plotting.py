#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 11:52:44 2021

@author: Iván Martín Martín
"""

"""
DESCRIPTION

    xxx
    
EXPECTED INPUT

    xxx
        
OUTPUT

    xxx
    
NOTE THAT:
    
    xxx
    
"""
import matplotlib.pyplot as plt
import seaborn as sns

def two_subplots_subsetylim(x_label, y_label, DataFrame, subset_ylim, name_image):
    # plt.clf()
    fig1 = plt.figure(num=0, clear=True, figsize=(7, 7))
    
    # First subplot
    plt.subplot(211)
    plt.xlabel(x_label)  
    plt.ylabel(y_label)
    plt.plot(DataFrame[x_label], DataFrame[y_label], '^g') 
    
    # Second subplot: subset to amplify y-axis scale
    plt.subplot(212)
    plt.xlabel(x_label)  
    plt.ylabel(y_label)
    subset_ratiosDataframe = DataFrame[DataFrame[y_label] < subset_ylim]
    plt.plot(subset_ratiosDataframe[x_label], subset_ratiosDataframe[y_label], '^c')  
    
    fig1.savefig(name_image+".png")  # If it is desired to save the figure
    plt.close(fig1)


def two_subplots_subsetxlim(x_label, y_label, DataFrame, subset_xlim, name_image):
    # plt.clf()
    fig1 = plt.figure(num=0, clear=True, figsize=(7, 7))
    
    # First subplot
    plt.subplot(211)
    plt.xlabel(x_label)  
    plt.ylabel(y_label)
    plt.plot(DataFrame[x_label], DataFrame[y_label], '^g') 
    
    # Second subplot: subset to amplify y-axis scale
    plt.subplot(212)
    plt.xlabel(x_label)  
    plt.ylabel(y_label)
    subset_ratiosDataframe = DataFrame[DataFrame[x_label] < subset_xlim]
    plt.plot(subset_ratiosDataframe[x_label], subset_ratiosDataframe[y_label], '^c')  
    
    fig1.savefig(name_image+".png")  # If it is desired to save the figure
    plt.close(fig1)
    
    
def two_subplots_subset_x_lowerlim(x_label, y_label, DataFrame, subset_xlim, name_image):
    # plt.clf()
    fig1 = plt.figure(num=0, clear=True, figsize=(7, 7))
    
    # First subplot
    plt.subplot(211)
    plt.xlabel(x_label)  
    plt.ylabel(y_label)
    plt.plot(DataFrame[x_label], DataFrame[y_label], '^g') 
    
    # Second subplot: subset to amplify y-axis scale
    plt.subplot(212)
    plt.xlabel(x_label)  
    plt.ylabel(y_label)
    subset_ratiosDataframe = DataFrame[DataFrame[x_label] > subset_xlim]
    plt.plot(subset_ratiosDataframe[x_label], subset_ratiosDataframe[y_label], '^c')  
    
    fig1.savefig(name_image+".png")  # If it is desired to save the figure
    plt.close(fig1)


def two_subplots_subsetlims(x_label, y_label, DataFrame, subset_xlim, subset_ylim, name_image):
    # plt.clf()
    fig1 = plt.figure(num=0, clear=True, figsize=(7, 7))
    
    # First subplot
    plt.subplot(211)
    plt.xlabel(x_label)  
    plt.ylabel(y_label)
    plt.plot(DataFrame[x_label], DataFrame[y_label], '^g') 
    
    # Second subplot: subset to amplify y-axis scale
    plt.subplot(212)
    plt.xlabel(x_label)  
    plt.ylabel(y_label)
    subset_ratiosDataframe = DataFrame[DataFrame[x_label] < subset_xlim]
    subset_ratiosDataframe = subset_ratiosDataframe[subset_ratiosDataframe[y_label] < subset_ylim]
    plt.plot(subset_ratiosDataframe[x_label], subset_ratiosDataframe[y_label], '^c')  
    
    fig1.savefig(name_image+".png")  # If it is desired to save the figure
    plt.close(fig1)
    
    
def two_plots_twolabels(x_label, y_label1, y_label2, DataFrame, name_image):
    # plt.clf()
    fig1 = plt.figure(num=0, clear=True, figsize=(7, 7))
    
    # First subplot
    plt.subplot(211)
    plt.xlabel(x_label)  
    plt.ylabel(y_label1)
    plt.plot(DataFrame[x_label], DataFrame[y_label1], '^g') 
    
    # Second subplot: subset to amplify y-axis scale
    plt.subplot(212)
    plt.xlabel(x_label)  
    plt.ylabel(y_label2)
    plt.plot(DataFrame[x_label], DataFrame[y_label2], '^c')  
    
    fig1.savefig(name_image+".png")  # If it is desired to save the figure
    plt.close(fig1)
    
    
def two_plots_twolabels_xlim(x_label, y_label1, y_label2, DataFrame, xlim, name_image):
    # plt.clf()
    fig1 = plt.figure(num=0, clear=True, figsize=(7, 7))
    subset_ratiosDataframe = DataFrame[DataFrame[x_label] < xlim]
    
    # First subplot
    plt.subplot(211)
    plt.xlabel(x_label)  
    plt.ylabel(y_label1)
    plt.plot(subset_ratiosDataframe[x_label], subset_ratiosDataframe[y_label1], '^g') 
    
    # Second subplot: subset to amplify y-axis scale
    plt.subplot(212)
    plt.xlabel(x_label)  
    plt.ylabel(y_label2)
    plt.plot(subset_ratiosDataframe[x_label], subset_ratiosDataframe[y_label2], '^c')  
    
    fig1.savefig(name_image+".png")  # If it is desired to save the figure
    plt.close(fig1)
    
    
def two_plots_twolabels_x_lowerlim(x_label, y_label1, y_label2, DataFrame, xlim, name_image):
    # plt.clf()
    fig1 = plt.figure(num=0, clear=True, figsize=(7, 7))
    subset_ratiosDataframe = DataFrame[DataFrame[x_label] > xlim]
    
    # First subplot
    plt.subplot(211)
    plt.xlabel(x_label)  
    plt.ylabel(y_label1)
    plt.plot(subset_ratiosDataframe[x_label], subset_ratiosDataframe[y_label1], '^g') 
    
    # Second subplot: subset to amplify y-axis scale
    plt.subplot(212)
    plt.xlabel(x_label)  
    plt.ylabel(y_label2)
    plt.plot(subset_ratiosDataframe[x_label], subset_ratiosDataframe[y_label2], '^c')  
    
    fig1.savefig(name_image+".png")  # If it is desired to save the figure
    plt.close(fig1)
    
    
def one_plot(x_label, y_label, DataFrame, name_image, plot_title):
    # plt.clf()
    fig2 = plt.figure(num=0, clear=True, figsize=(7, 7))
    
    # One Plot
    plt.subplot(111)
    plt.xlabel(x_label)  
    plt.ylabel(y_label)
    plt.plot(DataFrame[x_label], DataFrame[y_label], '^c')  
    plt.title(plot_title, fontsize = 14)
    
    fig2.savefig(name_image+".png")  # If it is desired to save the figure
    plt.close(fig2)
    
    
def one_plot_xlim(x_label, y_label, DataFrame, xlim, name_image, plot_title):
    # plt.clf()
    fig2 = plt.figure(num=0, clear=True, figsize=(7, 7))
    subset_ratiosDataframe = DataFrame[DataFrame[x_label] < xlim]
    
    # One Plot
    plt.subplot(111)
    plt.xlabel(x_label)  
    plt.ylabel(y_label)
    plt.plot(subset_ratiosDataframe[x_label], subset_ratiosDataframe[y_label], '^c')  
    plt.title(plot_title, fontsize = 14)
    
    fig2.savefig(name_image+".png")  # If it is desired to save the figure
    plt.close(fig2)


def one_plot_x_lowerlim(x_label, y_label, DataFrame, xlim, name_image, plot_title):
    # plt.clf()
    fig2 = plt.figure(num=0, clear=True, figsize=(7, 7))
    subset_ratiosDataframe = DataFrame[DataFrame[x_label] > xlim]
    
    # One Plot
    plt.subplot(111)
    plt.xlabel(x_label)  
    plt.ylabel(y_label)
    plt.plot(subset_ratiosDataframe[x_label], subset_ratiosDataframe[y_label], '^c')  
    plt.title(plot_title, fontsize = 14)
    
    fig2.savefig(name_image+".png")  # If it is desired to save the figure
    plt.close(fig2)
    
    
# Default whiskers: 1.5*(IQR)
def basic_boxplot(dataframe, x_var, y_var, x_label, y_label, filename):
    fig = plt.figure(num=0, clear=True, figsize=(7, 7))
    ax_boxplot = sns.boxplot(x = x_var, y = y_var, data = dataframe)
    ax_boxplot.set(xlabel = x_label, ylabel = y_label)
    fig.savefig(filename+".png")
    plt.close(fig)


# Default whiskers: 1.5*(IQR)
# Note that ylims should be a tuple
def basic_boxplot_ylims(dataframe, x_var, y_var, x_label, y_label, filename, ylims):
    fig = plt.figure(num=0, clear=True, figsize=(7, 7))
    plt.ylim(ylims[0], ylims[1])
    ax_boxplot = sns.boxplot(x = x_var, y = y_var, data = dataframe)
    ax_boxplot.set(xlabel = x_label, ylabel = y_label)
    fig.savefig(filename+".png")
    plt.close(fig)


def basic_scatter(dataframe, x_col, y_col, x_label, y_label, filename, plot_title):
    fig = plt.figure(num=0, clear=True, figsize=(7, 7))
    ax_cat = sns.stripplot(x=x_col, y=y_col, jitter = True, data = dataframe)
    ax_cat.set(xlabel=x_label, ylabel=y_label)
    plt.title(plot_title, fontsize = 14)
    fig.savefig(filename+".png")
    plt.close(fig)
    

def basic_scatter_ylim(dataframe, x_col, y_col, x_label, y_label, ylim, filename, plot_title):
    fig = plt.figure(num=0, clear=True, figsize=(7, 7))
    ax_cat = sns.stripplot(x=x_col, y=y_col, jitter = True, data = dataframe)
    ax_cat.set(xlabel=x_label, ylabel=y_label)
    plt.ylim(0, ylim)
    plt.title(plot_title, fontsize = 14)
    fig.savefig(filename+".png")
    plt.close(fig)



# EN CASO DE DOBLE FIGURA, VARIOS AXES
"""
fig1, axes1 = plt.subplots(num=0, clear=True, figsize=(15, 5), nrows=1, ncols=2)
ax_cat = sns.stripplot(ax = axes1[0], x="EVRrank", y="EVR", jitter = True, data = df_snp_pca_ratio)
ax_cat.set(xlabel='EVR Ranks', ylabel='Explained Variance Ratio')

ax_cat = sns.stripplot(ax = axes1[1], x="EVRrank", y="EVR", jitter = True, data = df_snp_pca_ratio)
ax_cat.set(xlabel='EVR Ranks', ylabel='Explained Variance Ratio')
axes1[1].set_ylim(0, 0.01)
"""





























