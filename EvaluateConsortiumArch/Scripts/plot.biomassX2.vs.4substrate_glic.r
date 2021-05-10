#!/usr/bin/env Rscript

# FLYCOP 
# Author: Beatriz García-Jiménez, Iván Martín Martín
# April 2018 // Modification: April 2021

args = commandArgs(trailingOnly=TRUE)
if (length(args)<10) {
  stop("At least 18_19 arguments must be supplied: <input_file.txt> <output_file.pdf> <met1_ID> <met2_ID> <met3_ID> <met4_ID> <met5_ID> <met6_ID> <endCycle> <title> <colSubs1> <colSubs2> <colSubs3> <colSubs4> <colSubs5> <colSubs6> [<strain1> <strain2> <strain3>]", call.=FALSE)
} else {
  inputFile=args[1]
  outFile=args[2]
  met1=args[3]
  met2=args[4]
  met3=args[5]
  met4=args[6]
  met5=args[7]
  met6=args[8]
  endCycle=as.numeric(args[9])
  title=args[10]
  color1=args[11]
  color2=args[12]
  color3=args[13]
  color4=args[14]
  color5=args[15]
  color6=args[16]
  if(length(args)==18){
    strain1=args[17]
    strain2=args[18]}
  if(length(args)==19){
    strain1=args[17]
    strain2=args[18]
    strain3=args[19]}
}

# MAX value for x
xMax=endCycle

# READ COMETS FILE (format: columns)
# ----------------------------------
# 2models
if(length(args)==18){
    # 7 columns, 7 substrates	
    df=read.csv(inputFile,sep='\t',header=FALSE,col.names=c('sub1','sub2','sub3','sub4', 'sub5', 'sub6', 'sub7', 'hours', 'biomass1','biomass2'))
    yMax=max(df$biomass1,df$biomass2)}  # MAX value for biomass
    
# 3models
if(length(args)==19){
    # 7 columns, 7 substrates		
    df=read.csv(inputFile,sep='\t',header=FALSE,col.names=c('sub1','sub2','sub3','sub4', 'sub5', 'sub6', 'sub7', 'hours', 'biomass1','biomass2','biomass3'))  
    yMax=max(df$biomass1,df$biomass2,df$biomass3)}  # MAX value for biomass
  
# MAX value for substrates
y2Max=max(df$sub1,df$sub2,df$sub3,df$sub4,df$sub5,df$sub6)


# PLOT FILE
# ---------
pdf(outFile,pointsize=20)

# BIOMASS
par(lwd=3)
plot(df$hours*0.1,df$biomass1,xlab='time(h)',ylab='biomass (gr/L)',type='l',lwd=4,col="green",ylim=c(0,yMax),main=title)
par(new=TRUE)

plot(df$hours*0.1,df$biomass2,xlab="",ylab="",type='l',lwd=4,col="red",ylim=c(0,yMax))
par(new=TRUE)

if(length(args)==19){
plot(df$hours*0.1,df$biomass3,xlab="",ylab="",type='l',lwd=4,col="darkgrey",ylim=c(0,yMax))}


# METABOLITES
par(new=TRUE,lwd=2)
plot(df$hours*0.1,df$sub1,type='l',col=color1,axes=FALSE,xlab="",ylab="",lwd=4,ylim=c(0,y2Max))
par(new=TRUE)
plot(df$hours*0.1,df$sub2,type='l',col=color2,axes=FALSE,xlab="",ylab="",lwd=4,ylim=c(0,y2Max))
par(new=TRUE)
plot(df$hours*0.1,df$sub3,type='l',col=color3,axes=FALSE,xlab="",ylab="",lwd=4,ylim=c(0,y2Max))
par(new=TRUE)
plot(df$hours*0.1,df$sub4,type='l',col=color4,axes=FALSE,xlab="",ylab="",lwd=4,ylim=c(0,y2Max))
par(new=TRUE)
plot(df$hours*0.1,df$sub5,type='l',col=color5,axes=FALSE,xlab="",ylab="",lwd=4,ylim=c(0,y2Max))
par(new=TRUE)
plot(df$hours*0.1,df$sub6,type='l',col=color6,axes=FALSE,xlab="",ylab="",lwd=4,ylim=c(0,y2Max))

axis(side=4)
mtext('metabolite Conc. (mM)',side=4,cex=par("cex.lab"))
par(lty=1)


# LEGEND FOR THE PLOT
# -------------------
if(length(args)==18){
legend("left", c(strain1,strain2,met1,met2,met3,met4,met5,met6), lty=c(1,1,1,1,1,1,1,1), lwd=c(3,3,4,4,4,4,4,4), col=c("green","red",color1,color2,color3,color4,color5,color6),cex=0.65)}

if(length(args)==19){
legend("left", c(strain1,strain2,strain3,met1,met2,met3,met4,met5,met6), lty=c(1,1,1,1,1,1,1,1,1), lwd=c(3,3,3,4,4,4,4,4,4), col=c("green","red","darkgrey",color1,color2,color3,color4,color5,color6),cex=0.65)}

invisible(dev.off())










