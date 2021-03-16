#!/usr/bin/env Rscript

# FLYCOP 
# Author: Beatriz García-Jiménez
# April 2018

# Error in eval(substitute(select), nl, parent.frame()) : 
#  object 'fitness' not found
# Calls: subset -> subset.data.frame -> eval -> eval
# Execution halted

suppressMessages(library(car))
suppressMessages(library(ellipse))
suppressMessages(library(RColorBrewer))

args = commandArgs(trailingOnly=TRUE)
if (length(args)<3) {
  stop("At least 3 arguments must be supplied: <domainName (string)> <experimentID (number)> <fitnessID (string)>", call.=FALSE)
} else {
  domainName=args[1]
  id=args[2]
  fitnessID=args[3]
}

# --------------------------------------------------------------------------------------
# cleaning
suffix=paste("Scenario",id,sep="")
setwd(paste(domainName,'_scenario',id,'_FLYCOPdataAnalysis',sep=""))


my_colors <- brewer.pal(11, "RdYlBu")
my_colors=colorRampPalette(my_colors)(25)
data=read.csv("tableParamWithFitness.csv",sep='\t',header=TRUE) 
formula=formula(paste("~",paste(colnames(data),collapse="+"),sep=""))

print("Chivato1")
header=paste(suffix,", Fitness=", fitnessID, sep="")
# correlation ellipse plot
corrMatrix<-cor(data)
pdf(paste('correlationEllipsePlot_',suffix,".pdf",sep=""),title=header)
plotcorr(corrMatrix, col=my_colors[corrMatrix*15+15], type="lower", mar=c(1,1,1,1), main=paste("Correlation plot.",suffix))
invisible(dev.off())
write.table(corrMatrix,paste('corrMatrix_',suffix,".txt",sep=""),quote=FALSE,sep="\t")
print("Chivato2")


# --------------------------------------------------------------------------------------
# Scatterplot, with lower diagonal with correlations:
panel.cor <- function(x, y, digits = 3, prefix = "", cex.cor=1, ...) # from help(pairs) # Only correlation, with modifications from below code
{
  usr <- par("usr"); on.exit(par(usr))
  par(usr = c(0, 1, 0, 1))
  # correlation coefficient
  r <- cor(x,y)
  txt <- format(c(r, 0.123456789), digits = digits)[1]
  txt <- paste("r= ", txt, sep = "")
  text(0.5, 0.6, txt, cex=1)
}
pdf(paste('scatterplotMatrix_',suffix,"_withCorr.pdf",sep=""),title=header)
scatterplotMatrix(formula, data=data, smooth=list(smoother=""),lower.panel=panel.cor,main=header)
invisible(dev.off())
print("Chivato3")
# --------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------
# Removing not stable configurations
# To retrieve standard deviation values:
tableSd=read.csv('avgfitnessAndStdev.txt',sep=",",header=FALSE,row.names=NULL)
colnames(tableSd)=c('mean','sd')
pdf(paste('fitnessVsSd_',suffix,'.pdf',sep=""))
plot(tableSd,main=paste("Correlation plot.",suffix))
invisible(dev.off())
pdf(paste('fitnessVsSd_',suffix,'sdLt10pavg.pdf',sep=""))
plot(tableSd[tableSd$sd<(0.1*tableSd$mean),],main=paste("Correlation plot",suffix,'sd<10pavg',sep=", "))
invisible(dev.off())
print("Chivato4")


data$sd=tableSd$sd  # Añadir sd a tabla de nombre "data"
data <- subset(data,select=c(1:(length(data)-2),sd,fitFunc))  # Cambio de orden de columnas: sd (5a posición); fitFunc (6a pos)
dataSorted <- data [with(data, order(-fitFunc)), ]
write.table(dataSorted,paste('dataTable_',suffix,".txt",sep=""),quote=FALSE,sep="\t",row.names=TRUE, col.names=TRUE)
data_sdLt10p=data[data$sd<(0.1*data$fitFunc),]
pdf(paste('scatterplotMatrix_',suffix,'sdLt10pavg.pdf',sep=""),title=paste(header,'sd<10pavg',sep=', '))
scatterplotMatrix(formula,data=data_sdLt10p, smooth=list(smoother=""),lower.panel=panel.cor, main=paste(header,'sd<10pavg',sep=', '))
invisible(dev.off())
print("Chivato5")


# --------------------------------------------------------------------------------------
corrMatrix<-cor(data_sdLt10p)
pdf(paste('correlationEllipsePlot_',suffix,'sdLt10pavg.pdf',sep=""),title=paste(header,'sd<10pavg',sep=', '))
plotcorr(corrMatrix, col=my_colors[corrMatrix*15+15], type="lower", mar=c(1,1,1,1), main=paste(header,'sd<10pavg',sep=', '))
invisible(dev.off())
print("Chivato6")

sink(paste('corrMatrices_',suffix,'.txt',sep=''))
print('All configurations:')
print(dim(data)[1])
cor(data)
print('Sd<10pavg:')
print(dim(data_sdLt10p)[1])
cor(data_sdLt10p)
sink()

# help(sink)
