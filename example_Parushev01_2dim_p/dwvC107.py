## Copyright (C) 2012 Joel H. Levine
##
## Permission is hereby granted, free of charge, to any person obtaining
## a copy of this software and associated documentation files (the "Software"),
## to deal in the Software without restriction,including without limitation
## the rights to use, copy, modify, merge, publish, distribute, sublicense,
## and/or sell copies of the Software, and to permit persons to whom the Software
## is furnished to do so, subject to the following conditions:
##
## The above copyright notice and this permission notice shall be included
## in all copies or substantial portions of the Software.
##
## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
## OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
## FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
## THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
## LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
## FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
## IN THE SOFTWARE.

# C105  fixes bug in output (in sq sym model p, perhaps others, output was impossible
#raw_input("105 imported")
# C103  from C101, skipping C102
#       Fix bug that is making square symmetric tables inoperable
#       Report was:
#       global name 'nibble_re_identical_to_ce_sq_sym' is not defined
# B041  Re-introducing dubious capacity to nibble on minkowski and attenuation

# B039  I've messed up 038 by introducing Cauchy -- take it out of 038
#       but figure it out here.  The Cauchy thing is also driving whatever
#       makes the row and col coordinates occasionally unequal.  I've also
#       begun to run the model in a loop for mink and attenuation (not
#       yet running parallel)   For that I added a return from main.
#          It is filing the last value, not the best value
#       Since the bounce can drive it up hill the last is not necessarily the best
# B038  Restore missing data option 2/3/10
# B037  add shuffling of parameters.  Unfortunately B037Shuffling.py
#       was built (inadvertently) on a Novemeber copy instgead of the 2/8/09
#       copy.  So here in Shuffling2 I am starting with 2/8/09 copy and patching in
#       written, compilable, but not yet test parts of dwvB037SHUFFLING

#026-B030
# 2/11/07
# B030 is being modified for integration with the GUI
# B030 026BU seems to be what I used with Johannes' stuff.  The runs that were complete through
#     externally drawn graphics are on SevenH1.  There was some sort of data change for
#     SevenH2 but no graphics, signifying not taken all the way.
#       028 and 029 were working on NETFLIX with mprectangle  (movie preference).  It required
#       several additions:  missing data, different fit, different model.   In 029 I appear to
#       have been adding output for nearest neighbors, but it is not a running program.
#       For integration with the GUI, go back to 026BU, although I will want the NETFLIX stuff
#       for that reason the numbering of versions is forking from 026BU to B030, leaving stuff
#       in 028 and 029 for subsequent excavation.
#026  add storage and recovery, work gram-schmitt into the semi-starts
#023  add storage and recovery
#     The original storage and recovery routines used numpy.  Eventually,
#     that may become standard.  But, the present version is an add on and
#     there is no 1.0 package for the Mac (it requires compilation).  So, assume
#     that, for now, the tendency to eat memory will persist (found in 0.9).
#     I'm still using numpy (arrays) for re,ce,rx,and cx.  If necessary for
#     portability I can push those back to lists too.
#     The test run of Johannes Lohmann's Seven got below 18,000 in about
#     22 hours.  It is at 17,856 in (very roughly) 31 hours (using
#     a list of lists for ob, arrays for coords and effects).Now descending
#     at about 10 points per hour, about 1/20th to 1/40th of 1% per hour.
#     There exists an easy (fast running) adaptation of downhill simplex
#     that can be run on even with this number of parameters.
#022
#17-20 experimenting with memory and with complete rewrite.  The memory
#problem is either endemic to numpy or else I've done something wierd in
#the way I use it.  However, using a list of lists does not have the problem
#and appears to be faster as well.  (See short codes for experiments.)
#Rather than rewrite, and create new bugs and sub-optimal procedures, adapt
#016.  -- although it will need the improved output.
#I might start with doubling the data, using the old ob (an array), and
#introducing obLL, as a list of lists.

# CHANGED MY MIND.  THERE IS GOOD STUFF IN 020.  REBUILD IT STARTING IN 022

#f=open("SevenH2","w")
#f.close()

#Found the memory bug in numpy itself.  
#Just any large matrix, accessed repeatedly, drives the bug.

#When I compared it to using a list of lists as an array, not only did it not add to memory, it was also faster than numpy.

#Considering that I am not using any serious matrix operations, other than
#Occasionally summing, ob, at least, can be a list of lists.  Note filed on tutor@python.com
#So, switch ob to a list of lists.  Since I use vector functions for standardizing
#rx,cs,re, and ce, and because they are much smaller, leave then alone for now.

#rebuild from scratch.  Note that even though it has random.seed(1) at top of
#dwv018.  It starts with same random number.  But by the time it gets to main
#it is already different (unless I use seed again).  I don't understand
#that so maybe the problem with memory, whatever it is, has already happened
#(although that's unlikely, considering that the problem seems to depend on
#data size where, as yet, I have no data.

# well,  apparently results of random.seed(1) are not available elsewhere
# So it has to be invoked repeatedly -- although having it in main might do the
# job of getting into common.


#import gc  What is this or was this?  No file by this name in my folder.  Is it in python's library
import random,time
#from time import *
import copy
from gram_schmidt import *
from Tkinter import *  #for askopenfile name, hope it does not conflict with IDLE
from tkFileDialog import askopenfilename  #to get a template
#import rectangle_stock_plot007
import rectangle_driver007inprocess
import os,signal
import principle_components,gram_schmidt02,standardizep2a2
import order_column_vectors_by_variance
from running_medians02 import *
from spread_sheet_table_object10 import *

try:
        from numpy import *
        numpac="numpy"
except:
        from Numeric import *
        numpc="Numeric"

def time_muncher():
    #used for checking threads or devices for getting back to the GUI
    #while computations continue
    print "Inside time muncher ***************************"
    #raw_input("time muncher running")
    x=1
    for i in arange (100000):
        print i
        #if i%20==0:  print
        for j in arange(100):
            for k in arange(100):
                x=x+1
    #raw_input("time mucher has completed Now at bottom.")




def read_face_array(root):
        print "root",root
        print "ZZZ in 'read_face'array'"
        inf=open(root,"r")
        #print "AAA"
        stuff=inf.readlines()
        #print "BBB"
        #print "debug.  It has length ",len(stuff)
        print "at 123 in dwv:  The array file has ",len(stuff)," lines."
        for i in range(len(stuff)):
            print "%3i"%((i)),"<"+str(stuff[i]).strip()+">"
        if len(stuff)==1:
                #print stuff
                stuff=stuff[0].split("\r")
        for i in arange(len(stuff)):
                stuff[i]=stuff[i].strip()
        print "read as ",len(stuff)," lines."
        nrow=int(stuff[0])
        ncol=int(stuff[1])
        data=zeros((nrow,ncol),dtype=float)
        ptr=1
        for row in arange(nrow):
            ptr+=1
            row_stuff=stuff[ptr].split(",")
            for col in arange(ncol):
                data[row,col]=float(row_stuff[col].strip())
        rlab=[]         
        for row in arange(nrow):
                ptr+=1
                rlab.append(stuff[ptr].strip())
        clab=[] 
        for col in arange(ncol):
                ptr+=1
                clab.append(stuff[ptr].strip())

        return nrow, ncol, data, rlab, clab

def start_dwv_from_ob(ob,c):

    nrow=int(c["nrow"]);ncol=int(c["ncol"]);ndim=int(c["ndim"])
    omission_value=int(c["omission_value"])
    mod_type=c["mod_type"]
    mod_form=c["mod_form"]
    use_diagonal=c["use_diagonal"]
    rx = zeros((nrow,ndim),float)
    re = zeros((nrow),float)
    c["attenuation_power"]=c["requested_attenuation_power"]+0  #Re_start -- program may have tried to optimize it
    c["minkowski_power"]=c["requested_minkowski_power"]+0  #Re_start -- program may have tried to optimize it

    #get initial row effects from standard random model
    #row_sum=sum(ob,1)
    #col_sum=sum(ob,0)
    #table_sum=sum(row_sum)
    row_sum=[]
    for row in arange(nrow):
        row_sum.append(0)
    col_sum=[]
    table_sum=0.
    for col in arange(ncol):
        col_sum.append(0)
    for row in arange(nrow):
        for col in arange(ncol):
            orc=ob[row][col]
            if int(ob[row][col])!=omission_value:   #2/6/10
                if not (use_diagonal and row==col):  #2/6/10  
                    row_sum[row]+=orc
                    col_sum[col]+=orc
                table_sum+=orc
            
    for row in arange(nrow):
        if row_sum[row]==0.:
            print "\n\nProblem:"
            print "\nRow number ",row," sums to zero, implying it has no usable data."
            print "The solution for a row with no data at all is indeterminate."
            print "Please remove this row, and its label, from the data and begin again."
            print ob[row]
            raw_input("Press any key to stop the program.")
            exit()
                
        re[row]=log2(row_sum[row]/(table_sum**.5)) #16 did not use log2, though it would be more logical-- so what (it works)

    for row in arange(nrow):
        for dim in arange(ndim):
            rx[row,dim]=random.uniform(-.001,.001)
            
            
    mod_type=mod_type.lower()
    #print "at aaa 197",mod_type
    #print '"' in mod_type
    #print "'" in mod_type
    if '"' in mod_type or "'" in mod_type:
        print
        print "Error:  a quotation mark is showing up as part of"
        print "        the name of the mod_type.  "
        print "  Likely fix:  remove quotation marks where mod_type is"
        print "        specified in the setup file.\n"
        print "currently:  ",mod_type,type(mod_type)
        
    if mod_type == "square_symmetric":
        cx=rx
        ce=re
    elif mod_type== "square_asymmetric":
        cx=rx
        ce=zeros((ncol),float)
        #ce=log2(col_sum/(table_sum**.5)   )
        for col in arange(ncol):
            print "\n\nProblem:"
            print "\nColumn number ",col," sums to zero, implying it has no usable data."
            print "The solution for a column with no data at all is indeterminate."
            print "Please remove this columns, and its label, from the data and begin again."
            raw_input("Press any key to stop the program.")
            exit()
                
                
            ce[col]=log2(col_sum[col]/(table_sum**.5))          
    elif mod_type== "rectangular":

        cx=zeros((ncol,ndim),float)
        for col in arange(ncol):
            for dim in arange(ndim):
                cx[col,dim]=random.uniform(-.001,.001)
        ce=zeros((ncol),float)
        #ce=log2(col_sum/(table_sum**.5)   )
        for col in arange(ncol):
            ce[col]=log2(col_sum[col]/(table_sum**.5))
    else:
        raw_input("mod_type <"+str(mod_type)+"> not recognized -- STOP\n all characters should be lower case")
    #problem:  the errors near 0 in the distance model will, when combined
    #with near zero starting coordinates, immediately divide into two distant packages (rows versus columns)
    #and it can't get back"        
    if mod_form=="nn" or mod_form=="i":
        rx*=1000.
        cx*=1000.

    return re,ce,rx,cx

def chi_square(obs,fitted):
    if fitted<0:  return 1e10    
    if obs<1e-20: #copy from DwV20_A_2.f90
        #print "at 236, observed=",obs    
        return fitted
    else:
        if fitted<=1e-10:
            #print "AT 240,  fittED=",fitted  
            return 1e10
        else:
            if ((obs-fitted)*(obs-fitted))/fitted <0:
                raw_input("negative chi square !"+str(obs)+" "+str(fitted))        
            return abs(((obs-fitted)*(obs-fitted))/fitted ) 


def full_eval_err02(c,ob,re,ce,rx,cx,mod_form,d_start):
    #print c["root"],c["mod_type"]
    #raw_input("check root")

    d_start=c["d_start"]  #bypass input 1/21/12
    nrow=c["nrow"];ncol=c["ncol"];mod_type=c["mod_type"];use_diagonal=c["use_diagonal"]
    minkowski_power=c["minkowski_power"];attenuation_power=c["attenuation_power"]
    erf=c["erf"];omission_value=c["omission_value"]

    evrc=get_fitted_table_of_values(re,ce,rx,cx,attenuation_power,minkowski_power,mod_form,d_start) #rxi is a vector of length ndim, ditto for cxi

    error=0.
    if mod_type=="square_symmetric":
        if use_diagonal:
            for row in arange(nrow):
                for col in arange(row+1):
                    if int(ob[row,col])!=omission_value:    
                        error+=erf(ob[row,col],evrc[row,col])
        else:
            for row in arange(nrow):
                for col in arange(row):
                    if int(ob[row,col])!=omission_value:    
                        error+=erf(ob[row,col],evrc[row,col])

    else:
        if use_diagonal:
            for row in arange(nrow):
                for col in arange(ncol):
                    if int(ob[row,col])!=omission_value:    
                        error+=erf(ob[row,col],evrc[row,col])
        else:            
            for row in arange(nrow):
                for col in arange(ncol):
                    if row!=col:     
                        if int(ob[row,col])!=omission_value:    
                            error+=erf(ob[row,col],evrc[row,col])
    return error  

def full_eval_err02_FixPrintout(c,ob,re,ce,rx,cx,mod_form,d_start):
    #output to file is coming out wrong on power model, OK on i
    #because it is getting the total error right from full_eval_err02
    #just give the working routine more output.

    #print c["root"],c["mod_type"]
    #raw_input("check root")

    d_start=c["d_start"]  #bypass input 1/21/12
    nrow=c["nrow"];ncol=c["ncol"];mod_type=c["mod_type"];use_diagonal=c["use_diagonal"]
    minkowski_power=c["minkowski_power"];attenuation_power=c["attenuation_power"]
    erf=c["erf"];omission_value=c["omission_value"]

    error_component=zeros((nrow,ncol),float)    #new

    evrc=get_fitted_table_of_values(re,ce,rx,cx,attenuation_power,minkowski_power,mod_form,d_start) #rxi is a vector of length ndim, ditto for cxi

    error=0.
    if mod_type=="square_symmetric":
        if use_diagonal:
            for row in arange(nrow):
                for col in arange(row+1):
                    if int(ob[row,col])!=omission_value:    
                        error_component[row,col]=erf(ob[row,col],evrc[row,col])
                        error+=error_component[row,col]
        else:
            for row in arange(nrow):
                for col in arange(row):
                    if int(ob[row,col])!=omission_value:    
                        error_component[row,col]=erf(ob[row,col],evrc[row,col])
                        error+=error_component[row,col]

    else:
        if use_diagonal:
            for row in arange(nrow):
                for col in arange(ncol):
                    if int(ob[row,col])!=omission_value:   
                        error_component[row,col]= erf(ob[row,col],evrc[row,col])
                        error+=error_component[row,col]
        else:            
            for row in arange(nrow):
                for col in arange(ncol):
                    if row!=col:     
                        if int(ob[row,col])!=omission_value: 
                            error_component[row,col]=   erf(ob[row,col],evrc[row,col])   
                            error+=error_component[row,col]
    return error,evrc,error_component
  
def full_eval_err02_extra_debugging_output(c,ob,re,ce,rx,cx,mod_form,d_start):
    #print c["root"],c["mod_type"]
    #raw_input("check root")

    
    nrow=c["nrow"];ncol=c["ncol"];mod_type=c["mod_type"];use_diagonal=c["use_diagonal"]
    minkowski_power=c["minkowski_power"];attenuation_power=c["attenuation_power"]
    erf=c["erf"];omission_value=c["omission_value"]

    evrc=get_fitted_table_of_values_extra_debugging_output(re,ce,rx,cx,attenuation_power,minkowski_power,mod_form,d_start) #rxi is a vector of length ndim, ditto for cxi

    error=0.
    if mod_type=="square_symmetric":
        if use_diagonal:
            for row in arange(nrow):
                for col in arange(row+1):
                    if int(ob[row,col])!=omission_value:    
                        error+=erf(ob[row,col],evrc[row,col])
        else:
            for row in arange(nrow):
                for col in arange(row):
                    if int(ob[row,col])!=omission_value:    
                        error+=erf(ob[row,col],evrc[row,col])

    else:
        if use_diagonal:
            for row in arange(nrow):
                for col in arange(ncol):
                    if int(ob[row,col])!=omission_value:    
                        error+=erf(ob[row,col],evrc[row,col])
        else:            
            for row in arange(nrow):
                for col in arange(ncol):
                    if row!=col:     
                        if int(ob[row,col])!=omission_value:    
                            error+=erf(ob[row,col],evrc[row,col])
    return error  
##
##def full_eval_err02_check(c,ob,re,ce,rx,cx,mod_form,d_start):
##    #This should print detail that can be reproduced on a spreadsheet
##
##    out_spread=open("dwv_out_spread","w")     
##
##    
##    nrow=c["nrow"];ncol=c["ncol"];mod_type=c["mod_type"];use_diagonal=c["use_diagonal"]
##    minkowski_power=c["minkowski_power"];attenuation_power=c["attenuation_power"]
##    erf=c["erf"];omission_value=c["omission_value"]
##
##
##    #Show controls
##    line=""
##    line+="nrow "+str(nrow)+"\n"
##    line+="ncol "+str(ncol)+"\n"
##    line+="mod_type "+str(mod_type)+"\n"
##    line+="use_diagonal "+str(use_diagonal)+"\n"
##    line+="minkowski_power "+str(minkowski_power)+"\n"
##    line+="attenuation_power "+str(attenuation_power)+"\n"
##    line+="erf "+str(erf)+"\n"
##    line+="omission_value "+str(omission_value)+"\n"
##    out_spread.write(line)
###??? is there no switch for turning omission_value on and off
##    line="\n\nObserved\n"
##    line+="Observed"
##    for col in range(ncol):
##        line+=","+c["clab"][col]
##    line+="\n"    
##    for row in range(nrow):
##        line+=c["rlab"][row]
##        for col in range(ncol):
##            line+=",%8.2f"%(float(ob[row,col]))
##        line+="\n"
##    out_spread.write(line)    
##            
##            
##
##
##
##    #evrc=get_fitted_table_of_values(re,ce,rx,cx,attenuation_power,minkowski_power,mod_form,d_start) #rxi is a vector of length ndim, ditto for cxi
##    evrc=get_fitted_table_of_values_check(c,out_spread,re,ce,rx,cx,attenuation_power,minkowski_power,mod_form,d_start) #rxi is a vector of length ndim, ditto for cxi
##
##    error=0.
##    if mod_type=="square_symmetric":
##        if use_diagonal:
##            for row in arange(nrow):
##                for col in arange(row+1):
##                    if int(ob[row,col])!=omission_value:    
##                        error+=erf(ob[row,col],evrc[row,col])
##        else:
##            for row in arange(nrow):
##                for col in arange(row):
##                    if int(ob[row,col])!=omission_value:    
##                        error+=erf(ob[row,col],evrc[row,col])
##
##    else:
##        if use_diagonal:
##            for row in arange(nrow):
##                for col in arange(ncol):
##                    if int(ob[row,col])!=omission_value:
##                        #print "at 496, type ob",type(ob),"type evrc",type(evrc)     
##                        error+=erf(ob[row,col],evrc[row,col])
##        else:            
##            for row in arange(nrow):
##                for col in arange(ncol):
##                    if row!=col:     
##                        if int(ob[row,col])!=omission_value:    
##                            error+=erf(ob[row,col],evrc[row,col])
##    return error  
##


def full_evLL(c,re,ce,rx,cx,mod_form,d_start):
    # raw_input("old routine full_evLL.  Replace it") *used once during output
    nrow=c["nrow"];ncol=c["ncol"];mod_type=c["mod_type"];use_diagonal=c["use_diagonal"]
    minkowski_power=c["minkowski_power"];attenuation_power=c["attenuation_power"]
    erf=c["erf"];omission_value=c["omission_value"]
    ev=zeros((nrow,ncol),float)
    if mod_type=="square_symmetric":
        for row in arange(nrow):
            for col in arange(ncol):
                if col>=row:
                    try:
                        ev[row,col]=get_fitted_value(re[row],ce[col],rx[row,:],cx[col,:],
                                                     attenuation_power,minkowski_power,mod_form,d_start)
                    except:
                        print "at c row",row,type(row),"nrow",nrow,"col",col,"ncol",ncol,use_diagonal,mod_type
                        print "at c- row re",re[row]
                        print "at c- row ce",ce[col]
                        print "at c- row rx[row,:]",rx[row,:]
                        print "at c- row cx[col,:]",cx[col,:]
                        print len(rx)
                        print rx[row,0]
                        print rx[row,:]
                else:
                    ev[row,col]=ev[col,row]
    else:
        for row in arange(nrow):
            for col in arange(ncol):
                #print "check attentuation power type",type(attenuation_power)
                #raw_input("check attenuation type")
                try:
                    ev[row,col]=get_fitted_value(re[row],ce[col],rx[row,:],cx[col,:],
                                                 attenuation_power,minkowski_power,mod_form,d_start)
                except:
                    print "at d row",row,type(row),"nrow",nrow,"col",col,"ncol",ncol,use_diagonal,mod_type
                    print "at d- row re",re[row]
                    print "at d- row ce",ce[col]
                    print "at d- row rx[row,:]",rx[row,:]
                    print "at d- row cx[col,:]",cx[col,:]
                    print len(rx)
                    print rx[row,0]
                    print rx[row,:]                    
    return ev

def row_eval_err(row,c,ob,re,ce,rx,cx):
    raw_input("old routine, replace row_eval_err")
    nrow=c["nrow"];ncol=c["ncol"];mod_type=c["mod_type"];use_diagonal=c["use_diagonal"]
    minkowski_power=c["minkowski_power"];attenuation_power=c["attenuation_power"]
    erf=c["erf"];omission_value=c["omission_value"]
    mod_form=c["mod_form"];d_start=c["d_start"]
    error=0.
    
    for col in arange(ncol):
        if int(ob[row,col])!=omission_value:    
            evrc=               get_fitted_value(re[row],ce[col],rx[row,:],cx[col,:],
                                                 attenuation_power,minkowski_power,mod_form,d_start)
            evrc_check_vec=get_fitted_row_values(re[row],ce,rx[row,:],cx,
                                                 attenuation_power,minkowski_power,mod_form,d_start)
            if evrc!=evrc_check_vec[col]:
        #    print "row","col",row,col,"single",evrc,"from vec",evrc_check_vec[col]
        #    print  d1
        #    print  d2[col],"col=",col
        #    print d2
        #    print
        #    print rei1
        #    print rei2
        #    print
        #    print cej1
        #    print cej2[col]
        #    print
        #    print a1
        #    print a2
            
                raw_input("non match") 
                error+=erf(ob[row,col] , evrc)
        #if col==0:
        #    print "evrc item",col,evrc
        #    print "re[row]",re[row]
        #    print "ce[col]",ce[col]
        #    print "rx[row,:]",rx[row,:]
        #    print "cx[col,:]",cx[col,:],attenuation_power,minkowski_power
    #print
    return error

def row_col_eval_sq_asym_err02(row_and_col,c,ob,re,ce,rx,cx):
    #use where symmetry requires checking fit in row i and col i at the same time    
    nrow=c["nrow"];ncol=c["ncol"];mod_type=c["mod_type"];use_diagonal=c["use_diagonal"]
    minkowski_power=c["minkowski_power"];attenuation_power=c["attenuation_power"]
    erf=c["erf"];omission_value=c["omission_value"]
    ndim=c["ndim"] # only for debugging to check rx=cx
    mod_form=c["mod_form"];d_start=c["d_start"]
    error=0.
                
#bookmark BBBB
    if mod_type!="square_asymmetric":
            raw_input("error -- this code intended for square asymmetric at 385")
    else:

            #debug
            #for comparison
            #compare_ev=get_fitted_table_of_values(re,ce,rx,cx,attenuation_power,minkowski_power,mod_form,d_start) #rxi is a vector of length ndim, ditto for cxi

            evrc=get_fitted_row_values(re[row_and_col],ce,rx[row_and_col,:],cx,
                               attenuation_power,minkowski_power,mod_form,d_start)
            #for debugging:
            #evrc=compare_ev[row_and_col,:]
            #for ii in range(ncol):
            #    if evrc[ii]!=compare_ev[row_and_col,ii]:
            #        raw_input("comparison fails at 401")
                    
            for col in arange(ncol): 
                if use_diagonal or col!=row_and_col:
                    if ob[row_and_col,col]!=omission_value:
                        error+=erf(ob[row_and_col,col], evrc[col])
                        
            evrc=get_fitted_col_values(re,ce[row_and_col],rx,cx[row_and_col,:],
                                       attenuation_power,minkowski_power,mod_form,d_start)

            #for debugging
            #evrc=compare_ev[:,row_and_col]
            #for ii in range(ncol):
            #    if evrc[ii]!=compare_ev[ii,row_and_col]:
            #        raw_input("                       comparison fails at 415")
            
            for row in arange(nrow): #now down the column
                if row!=row_and_col:  #don't double count the diagonal
                    if ob[row,row_and_col]!=omission_value:    
                        error+=erf(ob[row,row_and_col] , evrc[row])  #Can I get the chi-square to be indifferent between numbers and arrays (and then do this as an array)
    return error

def row_col_eval_sq_sym_err02(row_and_col,c,ob,re,ce,rx,cx):
    #use where symmetry requires checking fit in row i and col i at the same time    
    nrow=c["nrow"];ncol=c["ncol"];mod_type=c["mod_type"];use_diagonal=c["use_diagonal"]
    minkowski_power=c["minkowski_power"];attenuation_power=c["attenuation_power"]
    erf=c["erf"];omission_value=c["omission_value"]
    ndim=c["ndim"] # only for debugging to check rx=cx
    mod_form=c["mod_form"];d_start=c["d_start"]
    error=0.

                
    if mod_type!="square_symmetric":
            raw_input("error -- this code intended for square symmetric at 390")
    else:

            #debug
            #for comparison
            #compare_ev=get_fitted_table_of_values(re,ce,rx,cx,attenuation_power,minkowski_power,mod_form,d_start) #rxi is a vector of length ndim, ditto for cxi

            evrc=get_fitted_row_values(re[row_and_col],ce,rx[row_and_col,:],cx,
                               attenuation_power,minkowski_power,mod_form,d_start)
            #evrc=compare_ev[row_and_col,:]
            #5/21/2012:  Looks like the compare_ev was never written (and would be a pain since I haven't fitted it)    
            #for ii in range(ncol):
            #    if evrc[ii]!=compare_ev[row_and_col,ii]:
            #        raw_input("comparison fails at 389")


                    
            #for col in arange(row_and_col): #up to the diagonal only (data are square and symmetrical)
            for col in arange(ncol): 
                if use_diagonal or col!=row_and_col:
                    if ob[row_and_col,col]!=omission_value:
                        error+=erf(ob[row_and_col,col], evrc[col])
##            evrc=get_fitted_col_values(re,ce[row_and_col],rx,cx[row_and_col,:],
##                                       attenuation_power,minkowski_power,mod_form,d_start)
##            for row in arange(row_and_col,nrow): #now down the column
##                if row!=row_and_col:  #don't double count the diagonal
##                    if ob[row,row_and_col]!=omission_value:    
##                        error+=erf(ob[row,row_and_col] , evrc[row])  #Can I get the chi-square to be indifferent between numbers and arrays (and then do this as an array)
    return error

def rowi_coli_of_square_symmetric_data_eval(row_and_col,c,ob,re,ce,rx,cx):

    #Need this because the ordinary row routine checks for symmetry
    #and if symmetric it stops at the diagonal.  (If it were not for
    #that it would suffice to check a full row.

    if c["mod_type"]!="square_symmetric":
            raw_input("inappropriate programming at 610")
    #use where symmetry of coordinates (but not effects or data)
    #requires checking fit in row i and col i at the same time    
    nrow=c["nrow"]
    ncol=c["ncol"]
    mod_type=c["mod_type"]
    use_diagonal=c["use_diagonal"]
    minkowski_power=c["minkowski_power"]
    attenuation_power=c["attenuation_power"]
    erf=c["erf"]
    omission_value=c["omission_value"]
    ndim=c["ndim"] # only for debugging to check rx=cx
    mod_form=c["mod_form"]
    d_start=c["d_start"]
                

    error=0.
    #first piece
    evrc=get_fitted_row_values(re[row_and_col],ce,rx[row_and_col,:],cx,
                attenuation_power,minkowski_power,mod_form,d_start)
    for col in arange(row_and_col):
        if use_diagonal or col!=row_and_col:
            if ob[row_and_col,col]!=omission_value:                    
                error+=erf(ob[row_and_col,col] , evrc[col])
    #second piece            
    evrc=get_fitted_col_values(re,ce[row_and_col],rx,cx[row_and_col,:],
                               attenuation_power,minkowski_power,mod_form,d_start)
    for row in arange(row_and_col+1,nrow):
        if ob[row,row_and_col]!=omission_value:    
            error+=erf(ob[row,row_and_col] , evrc[row])  #Can I get the chi-square to be indifferent between numbers and arrays (and then do this as an array)
    return error



def row_eval_err02(row,c,ob,re,ce,rx,cx):
    nrow=c["nrow"];ncol=c["ncol"];mod_type=c["mod_type"];use_diagonal=c["use_diagonal"]
    minkowski_power=c["minkowski_power"];attenuation_power=c["attenuation_power"]
    erf=c["erf"];omission_value=c["omission_value"]
    mod_form=c["mod_form"];d_start=c["d_start"]
    error=0.

    #try to work on whole row (for speed)

    evrc=get_fitted_row_values(re[row],ce,rx[row,:],cx,
                               attenuation_power,minkowski_power,mod_form,d_start)
    for col in arange(ncol):
        if use_diagonal or row!=col:    
            if int(ob[row,col])!=omission_value:    
                error+=erf(ob[row,col] , evrc[col])
        
    return error

##def col_eval_err(col,c,ob,re,ce,rx,cx):
##    nrow=c["nrow"];ncol=c["ncol"];mod_type=c["mod_type"];use_diagonal=c["use_diagonal"]
##    minkowski_power=c["minkowski_power"];attenuation_power=c["attenuation_power"]
##    erf=c["erf"];omission_value=c["omission_value"]
##    mod_form=c["mod_form"];d_start=c["d_start"]
##    error=0.
##
##    for row in arange(nrow):            
##        if int(ob[row,col])!=omission_value:    
##            evrc=get_fitted_value(re[row],ce[col],rx[row,:],cx[col,:],
##                                  attenuation_power,minkowski_power,mod_form,d_start)
##            error+=erf(ob[row,col] , evrc)
##    return error

def col_eval_err02(col,c,ob,re,ce,rx,cx):
    nrow=c["nrow"];ncol=c["ncol"];mod_type=c["mod_type"];use_diagonal=c["use_diagonal"]
    minkowski_power=c["minkowski_power"];attenuation_power=c["attenuation_power"]
    erf=c["erf"];omission_value=c["omission_value"]
    mod_form=c["mod_form"];d_start=c["d_start"]
    error=0.

    #for comparison, compare to the full evrc
    evrc_comparison=get_fitted_table_of_values(re,ce,rx,cx,attenuation_power,minkowski_power,mod_form,d_start) #rxi is a vector of length ndim, ditto for cxi

    evrc=get_fitted_col_values(re,ce[col],rx,cx[col,:],
                               attenuation_power,minkowski_power,mod_form,d_start)

    different=False
    for cki in range(nrow):
        if abs(evrc[cki]-evrc_comparison[cki,col])>1e-10:
            raw_input("problem with predicted values at 554*****"+str(evrc[cki]-evrc_comparison[cki,col]))
    for row in arange(nrow):
        if use_diagonal or row!=col:    
            if int(ob[row,col])!=omission_value:    
                error+=erf(ob[row,col] , evrc[row])  #Can I get the chi-square to be indifferent between numbers and arrays (and then do this as an array)
    return error

def get_fitted_value(rei,cej,rxi,cxj,attenuation_power,minkowski_power,mod_form,d_start): #rxi is a vector of length ndim, ditto for cxi
                        
    ndim=size(rxi)

    if mod_form=="CA":  #correspondence analysis
            #Stay with the existing program where the row and col effects
            # It is consistent with the way I got starting values for these things
            # The goodness of fit criterion is different from the algebraic
            # solution for correspondence analysis -- but this will give it the
            # best chi-square the form can produce, giving it the benefit of
            # chi-square, leaving the form of the reconstruction formula.

            #If I am going to let the row and column multipliers vary (which
            # it appears they, the correspondence analysis people, do not
            # then working in logs puts them in a roughly commensurable
            # scale of effect vis a vis the coordinates.  (The standard
            # solution seems to use the null model multipliers as masses
            # and then apply the decomposition to successive layers of
            # residuals.

            #Hmmm:  Following Greenacre, pp 57-58, they use the row multipliers
            # as the null-model multipliers -- whatever that is supposed to mean
            # when there are missing cells.  
            decomp=0.
            for dim in arange(ndim):
                decomp+=rxi[dim]*cxj[dim]
            return (2**(rei*cej))*(1+decomp)
        
    else:  #all distance models 
    
            distance=0.
            for dim in arange(ndim):
                diff=abs(rxi[dim]-cxj[dim])
                #print "one dim diff",diff
                try:
                    distance+=diff**minkowski_power
                except:
                    print "debug*****************:",type(diff),type(minkowski_power)
                    print "diff:",diff
                    print "minkowski_power",minkowski_power
                    distance+=diff**minkowski_power
                #print "dim distance",dim,distance
            #raw_input("fv")
            #print "distance1b single without minkowski fraction",distance         
            distance**=(1./minkowski_power)
            #print "distance1b single",distance
            
            """ Cauchy form

                  1
         = ----------------, where d is the minkowski distance from x to y with minkowski parameter m
                          a
            [ 1 + d(x,y,m)  ]


        or

        # DECIDED NOT IMPLiMENTED -- INSTEAD IMPLiMENTED STARTED INVERSE DISTANCE
        interpreted as fudge for 0 distance, change the fudge  (Could also use started distance with c_start=0 and
        started_distance^a

                  1
         = ----------------, where d is the minkowski distance from x to y with minkowski parameter m 
                                a
            [ c_start + d(x,y,m)  ]

        OR

        STARTED INVERSE DISTANCE

                  1
         = ----------------, where d is the minkowski distance from x to y with minkowski parameter m 
                                a
            [ (d(x,y,m)+d_start)  ]


        """
            # 12/18/2011  Redundant parentheses for clarity
            if mod_form=="c":
                return  (2**(rei+cej))*(1./(1+distance**attenuation_power)) #Cauchy-like form
        
            elif mod_form in ["started_pcauchy","started_p_cauchy"]:
                return  (2**(rei+cej))*(1./(1+(distance+d_start)**attenuation_power)) #Cauchy-like form
                    
            elif mod_form=="p":    # "Power norm"
                if d_start:
                    return (2**(rei+cej) -((distance+d_start)**attenuation_power))  #work in exponentials base 2
                else:    
                    return (2**(rei+cej) -(distance**attenuation_power))  #work in exponentials base 2
            elif mod_form=="i":    # Inverse Power
                if d_start:    
                    return (2**(rei+cej))/((distance+d_start)**attenuation_power)  #work in exponentials base 2
                else:
                    return (2**(rei+cej))/(distance**attenuation_power)  #work in exponentials base 2
            else:
                raw_input("impossible value of mod_form, mod_form="+str(mod_form)+"at 582")            

def get_fitted_row_values(rei,ce,rxi,cx,attenuation_power,minkowski_power,mod_form,d_start): #rxi is a vector of length ndim, ditto for cxi
    ndim=size(rxi)
    ncol=size(ce)


    if mod_form=="CA":
            decomp=zeros((ncol),float)
            for dim in arange(ndim):
                    decomp[:]+=cx[:ncol,dim]*rxi[dim]  #Check -- have I got the array or math form chosen correctly
            return power(2,(rei+ce[:]))*(1+decomp)        
    else:


            distance=zeros((ncol),float)
            
            for dim in arange(ndim):
                dim_diff=abs(cx[:ncol,dim]-rxi[dim])
                try:
                    distance[:]+=dim_diff[:]**minkowski_power
                except:
                    print "dim",dim,"ncol",ncol    
                    print "type of dim_diff",type(dim_diff)    
                    print "debug*****************:",type(diff),type(minkowski_power)
                    print "dim_diff:"#,dim_diff
                    print "minkowski_power",minkowski_power
                    print "length distance & shape:",len(distance),shape(distance,)
                    print "length dim_diff & shape:",len(dim_diff),shape(dim_diff)
                    print "length cx & shape:",len(cx),shape(cx)
                    print 
                    distance[:]+=dim_diff**minkowski_power
            #distance**=(1./minkowski_power)    
            #distance=distance**(1./minkowski_power)  ###  Wow, very basic but this gave me the wrong numbers.
            inverse_mink=1./minkowski_power
            #power(distance,inverse_mink)  Error, misleading example in pdf manual
            #ufunction:  array, power, place in which to store result
            # can also write as distance=power(distance,inverse_mink)
            power(distance,inverse_mink,distance) #manual is amibiguous (because is assumes intepreter_
                
            #return 2**(rei+ce[:] -(distance[:]**attenuation_power))  #work in exponentials base 2
            
            if mod_form=="p":  #power-normal
                return power(2,(rei+ce[:] -(distance[:]**attenuation_power)))  #work in exponentials base 2
            elif mod_form=="c": #cauchy form
                return power(2,rei+ce[:])/(1+distance[:]**attenuation_power)
            elif mod_form in ["started_pcauchy","started_p_cauchy"]:
                return power(2,rei+ce[:])/(1+(distance[:]+d_start)**attenuation_power)
            elif mod_form=="i":
                if d_start:    
                    return 2**(rei+ce[:])/((distance[:]+d_start)**attenuation_power)  #work in exponentials base 2
                else:
                    return 2**(rei+ce[:])/(distance[:]**attenuation_power)  #work in exponentials base 2            
            else:
                raw_input("impossible value of mod_form at 634: "+str(mod_form))
            #return  2**(rei+cej)*(1./(1+distance**attenuation_power)) #Cauchy-like form

def get_fitted_col_values(re,cej,rx,cxj,attenuation_power,minkowski_power,mod_form,d_start): #rxi is a vector of length ndim, ditto for cxi
    ndim=size(cxj)
    nrow=size(re)
    if mod_form=="CA":
            decomp=zeros((nrow),float)
            for dim in arange(ndim):
                    decomp[:]=cxj[dim]*rx[:,dim]  #Check -- have I got the array or math form chosen correctly
            return power(2,(re[:]+cej))*(1+decomp)        
    else:        
            #distance=zeros((nrow),float)
            distance=abs(cxj[0]-rx[:,0])**minkowski_power
            
            for dim in arange(1,ndim):
                dim_diff=abs(cxj[dim]-rx[:,dim])
                try:
                    #distance[:]+=dim_diff[:]**minkowski_power
                    distance[:]+=power(dim_diff,minkowski_power)
                except:
                    print "debug*****************:",type(diff),type(minkowski_power)
                    print "diff:",diff
                    print "minkowski_power",minkowski_power
                    distance[:]+=diff**minkowski_power
            #distance**=(1./minkowski_power)    #Not available in numpy, but it does not flag the error.
            #distance=distance**(1./minkowski_power)  ###  Wow, very basic but this gave me the wrong numbers for fitted row values.   
            inverse_mink=1./minkowski_power
            power(distance,inverse_mink,distance)
                
            if mod_form=="p":        
            #return 2**(re[:]+cej -(distance[:]**attenuation_power))  #work in exponentials base 2
                return power(2,(re[:]+cej -(distance[:]**attenuation_power)))  #work in exponentials base 2
            elif mod_form=="c":
                return power(2,re[:]+cej)/(1+(distance[:]**attenuation_power))  #work in exponentials base 2
            elif mod_form in ["started_pcauchy","started_p_cauchy"]:
                return power(2,re[:]+cej)/(1+((distance[:]+d_start)**attenuation_power))  #work in exponentials base 2
            elif mod_form=="i":
                if d_start:    
                    return 2**(re[:]+cej)/((distance[:]+d_start)**attenuation_power)  #work in exponentials base 2
                else:
                    return 2**(re[:]+cej)/(distance[:]**attenuation_power)  #work in exponentials base 2
            else:
                raw_input("impossible value for mod_form at 664:  "+str(mod_form))
        
def get_fitted_table_of_values(re,ce,rx,cx,attenuation_power,minkowski_power,mod_form,d_start): #rxi is a vector of length ndim, ditto for cxi
    #print "incoming attenuation and minkowski",attenuation_power,minkowski_power
    #minkowski_power=1.0
    #attenuation_power=2.
    #print "work ing attenuation and minkowski",attenuation_power,minkowski_power
    ndim=size(cx,1)
    nrow=size(re)
    ncol=size(ce)

    if mod_form=="CA":
            decomp=zeros((nrow,ncol),float)
            for dim in arange(ndim):
                decomp+=outer(rx[:,dim],cx[:,dim])
            return power(2,(add.outer(re,ce)))*(1+decomp )       

    else:        
            distance=abs(subtract.outer(rx[:,0],cx[:,0]))**minkowski_power
            #print distance
            #print "size rx",size(rx,0),size(rx,1)
            #print 'size cx',size(cx,0),size(cx,1)
            #print "size distance",size(distance,0),size(distance,1)
            
            for dim in arange(1,ndim):  #might be able to get rid of this dim loop too.  Hmm not by subtactin cx and rx (it comes out 4 dimensional)
                #dim_diff=abs(cxj[dim]-rx[:,dim])  #Need an expand/broadcast function as I used in FORTRAN to spread it out (Python has one too).
                #dim_diff=abs(subtract.outer(rx[:,dim],cx[:,dim]))
                distance=distance+abs(subtract.outer(rx[:,dim],cx[:,dim]))**minkowski_power
            #distance**=(1./minkowski_power)    
            #distance=distance**(1./float(minkowski_power))  ###  Wow, very basic but **= not defined but doesn't raise an error
            minkowski_inverse=1./minkowski_power    
            power(distance,minkowski_inverse,distance)    


            try:  #debug
                #return power(2,(add.outer(re,ce) -(distance**float(attenuation_power))))  #work in exponentials base 2
                if mod_form=="p":
                    return power(2,(add.outer(re,ce) -(distance**float(attenuation_power))))  #work in exponentials base 2
                elif mod_form=="c":
                    return power(2,(add.outer(re,ce)))/(1+(distance**float(attenuation_power)))  #work in exponentials base 2
                elif mod_form in ["started_pcauchy","started_p_cauchy"]:
                    return power(2,(add.outer(re,ce)))/(1+((distance+d_start)**float(attenuation_power)))  #work in exponentials base 2
                elif mod_form=="i":
                    if d_start:
                        #print "d_start"*3,d_start,type(d_start)    
                        return power(2,(add.outer(re,ce)))/((distance+d_start)**float(attenuation_power))  #work in exponentials base 2
                    else:
                        return power(2,(add.outer(re,ce)))/((distance)**float(attenuation_power))  #work in exponentials base 2
                else:
                    print "impossible event at 923"
                    print "924 mod_form <"+mod_form+">"
                    count_ch=1
                    print "char# char ascii-ord"
                    for ch in mod_form:
                        print count_ch,ch,ord(ch)
                        count_ch+=1                    
                    raw_input("impossible event at 930 , mod_form="+str(mod_form))    
            except:
                print
                print "error exception near 746"
                print "attenuation_power",attenuation_power
                print "size(add.outer(re,ce),0)",size(add.outer(re,ce),0)
                print "size(add.outer(re,ce),1)",size(add.outer(re,ce),1)
                print 'size(distance[:],0)',size(distance,0)
                print "size(distance[:],1)",size(distance,1)
                print "size(rx,0),size(rx,1),size(cx,0),size(cx,1)"
                print size(rx,0),size(rx,1),size(cx,0),size(cx,1)
                print "mod_form at 753=",mod_form
                print "d_start at 753=",d_start
                print raw_input("Driving the bug again: at 755 "+"mod_form=<"+str(mod_form)+">")
                #return power(2,(add.outer(re,ce) -(distance**float(attenuation_power))))  #work in exponentials base 2
                if mod_form=="p":
                    return power(2,(add.outer(re,ce) -(distance**float(attenuation_power))))  #work in exponentials base 2
                elif mod_form=="c":
                    return power(2,(add.outer(re,ce)))/(1+(distance**float(attenuation_power)))  #work in exponentials base 2
                elif mod_form=="i":
                    if d_start:    
                        return power(2,(add.outer(re,ce)))/((distance+d_start)**float(attenuation_power))  #work in exponentials base 2
                    else:
                        return power(2,(add.outer(re,ce)))/((distance)**float(attenuation_power))  #work in exponentials base 2
                else:
                    raw_input("impossible event at 710, mod_form="+str(mod_form))    

            #return distance,2**(add.outer(re,ce) -(distance[:]**attenuation_power))  #work in exponentials base 2

def get_fitted_table_of_values_extra_debugging_output(re,ce,rx,cx,attenuation_power,minkowski_power,mod_form,d_start): #rxi is a vector of length ndim, ditto for cxi
    #print "incoming attenuation and minkowski",attenuation_power,minkowski_power
    #minkowski_power=1.0
    #attenuation_power=2.
    #print "work ing attenuation and minkowski",attenuation_power,minkowski_power
    ndim=size(cx,1)
    nrow=size(re)
    ncol=size(ce)

    if mod_form=="CA":
            decomp=zeros((nrow,ncol),float)
            for dim in arange(ndim):
                decomp+=outer(rx[:,dim],cx[:,dim])
            return power(2,(add.outer(re,ce)))*(1+decomp )       

    else:        
            distance=abs(subtract.outer(rx[:,0],cx[:,0]))**minkowski_power
            #print distance
            #print "size rx",size(rx,0),size(rx,1)
            #print 'size cx',size(cx,0),size(cx,1)
            #print "size distance",size(distance,0),size(distance,1)
            
            for dim in arange(1,ndim):  #might be able to get rid of this dim loop too.  Hmm not by subtactin cx and rx (it comes out 4 dimensional)
                #dim_diff=abs(cxj[dim]-rx[:,dim])  #Need an expand/broadcast function as I used in FORTRAN to spread it out (Python has one too).
                #dim_diff=abs(subtract.outer(rx[:,dim],cx[:,dim]))
                distance=distance+abs(subtract.outer(rx[:,dim],cx[:,dim]))**minkowski_power
            #distance**=(1./minkowski_power)    
            #distance=distance**(1./float(minkowski_power))  ###  Wow, very basic but **= not defined but doesn't raise an error
            minkowski_inverse=1./minkowski_power    
            power(distance,minkowski_inverse,distance)    


            try:  #debug
                #return power(2,(add.outer(re,ce) -(distance**float(attenuation_power))))  #work in exponentials base 2
                if mod_form=="p":
                    return power(2,(add.outer(re,ce) -(distance**float(attenuation_power))))  #work in exponentials base 2
                elif mod_form=="c":
                    print "product of multipliers"    
                    print power(2,(add.outer(re,ce)))
                    print "denominators"
                    print (1+(distance**float(attenuation_power)))
                    return power(2,(add.outer(re,ce))) / (1+(distance**float(attenuation_power)))  #work in exponentials base 2
                elif mod_form=="i":
                    if d_start:
                        #print "d_start"*3,d_start,type(d_start)    
                        return power(2,(add.outer(re,ce)))/((distance+d_start)**float(attenuation_power))  #work in exponentials base 2
                    else:
                        return power(2,(add.outer(re,ce)))/((distance)**float(attenuation_power))  #work in exponentials base 2
                else:
                    raw_input("impossible event at , mod_form="+str(mod_form))    
            except:
                print
                print "error exception near 746"
                print "attenuation_power",attenuation_power
                print "size(add.outer(re,ce),0)",size(add.outer(re,ce),0)
                print "size(add.outer(re,ce),1)",size(add.outer(re,ce),1)
                print 'size(distance[:],0)',size(distance,0)
                print "size(distance[:],1)",size(distance,1)
                print "size(rx,0),size(rx,1),size(cx,0),size(cx,1)"
                print size(rx,0),size(rx,1),size(cx,0),size(cx,1)
                print "mod_form at 753=",mod_form
                print "d_start at 753=",d_start
                print raw_input("Driving the bug again: at 755")
                #return power(2,(add.outer(re,ce) -(distance**float(attenuation_power))))  #work in exponentials base 2
                if mod_form=="p":
                    return power(2,(add.outer(re,ce) -(distance**float(attenuation_power))))  #work in exponentials base 2
                elif mod_form=="c":
                    return power(2,(add.outer(re,ce)))/(1+(distance**float(attenuation_power)))  #work in exponentials base 2
                elif mod_form=="i":
                    if d_start:    
                        return power(2,(add.outer(re,ce)))/((distance+d_start)**float(attenuation_power))  #work in exponentials base 2
                    else:
                        return power(2,(add.outer(re,ce)))/((distance)**float(attenuation_power))  #work in exponentials base 2
                else:
                    raw_input("impossible event at 710, mod_form="+str(mod_form))    

            #return distance,2**(add.outer(re,ce) -(distance[:]**attenuation_power))  #work in exponentials base 2

#bookmark AAAA
# This IS working with the row_col_eval stuff                    
def nibble_re_identical_to_ce_row_sq_asym(c,ob, re,ce,rx,cx,step,improved, row):
        #Insurance:  Something is wandering 2/7/10
        #re[:]=ce[:]
        savepr=re[row]
        savepc=ce[row]
        #temporarily check location of error with full eval
        #err_0=full_eval_err02(c,ob,re,ce,rx,cx,c['mod_form'],c['d_start'])
        #err_0=row_eval_err02(row,c,ob,re,ce,rx,cx)      #re=ce implies square symmetric & therefore rx=cx too
        err_0=row_col_eval_sq_asym_err02(row,c,ob,re,ce,rx,cx) #so it suffices to check one row all the way across
        re[row]+=step                                    #without reflecting on the diagonal  
        ce[row]+=step                                   #NEED TO CHECK CORRESPONDING ROUTINE FOR RX
        #err_right=full_eval_err02(c,ob,re,ce,rx,cx,c['mod_form'],c['d_start'])
        #err_right=row_eval_err02(row,c,ob,re,ce,rx,cx)  #FOR IT RE NOT NECESSARILY = CE THEREFOR NEED TO DO BOTH
        err_right=row_col_eval_sq_asym_err02(row,c,ob,re,ce,rx,cx)  #THE RELEVANT ROW AND THE RELEVANT COL (WO DIAGONAL)                   
        if err_right<err_0:
            err_0=err_right
            improved=True
        else:
            re[row]-=2*step
            ce[row]-=2*step
            #err_left=full_eval_err02(c,ob,re,ce,rx,cx,c['mod_form'],c['d_start'])
            #err_left=row_eval_err02(row,c,ob,re,ce,rx,cx)
            err_left=row_col_eval_sq_asym_err02(row,c,ob,re,ce,rx,cx)
            if err_left<err_0:
                err_0=err_left
                improved=True
            else:
                re[row]+=step
                ce[row]+=step

def nibble_re_identical_to_ce_sq_sym(c,ob, re,ce,rx,cx,step,improved):
        row_list=range(len(re))
        random.shuffle(row_list)
        #print row_list
        #raw_input("continue debugging at 1076")
        for row in row_list:
            nibble_re_identical_to_ce_row_sq_sym(c,ob, re,ce,rx,cx,step,improved, row)

def nibble_re_identical_to_ce_row_sq_sym(c,ob, re,ce,rx,cx,step,improved, row):
        #Insurance:  Something is wandering 2/7/10
        #print "debug  check sq sym 1083" #mod_type at 1082 is",c["mod_type"]
        #raw_input("got to 850 -- should not have   debug")
        #if c["mod_type"]!="square_symmetric":
        #    print "Error:  mod_type is ",c["mod_type"],"but the program call a routine for square_symmetric data"
        #    raw_input("at 853")
        re[:]=ce[:]
        savepr=re[row]
        savepc=ce[row]
        #temporarily check location of error with full eval
        #err_0=full_eval_err02(c,ob,re,ce,rx,cx,c['mod_form'],c['d_start'])
        #err_0=row_eval_err02(row,c,ob,re,ce,rx,cx)      #re=ce implies square symmetric & therefore rx=cx too
        err_0=row_col_eval_sq_sym_err02(row,c,ob,re,ce,rx,cx) #so it suffices to check one row all the way across
        re[row]+=step                                    #without reflecting on the diagonal  
        ce[row]+=step                                   #NEED TO CHECK CORRESPONDING ROUTINE FOR RX
        #err_right=full_eval_err02(c,ob,re,ce,rx,cx,c['mod_form'],c['d_start'])
        #err_right=row_eval_err02(row,c,ob,re,ce,rx,cx)  #FOR IT RE NOT NECESSARILY = CE THEREFOR NEED TO DO BOTH
        err_right=row_col_eval_sq_sym_err02(row,c,ob,re,ce,rx,cx)  #THE RELEVANT ROW AND THE RELEVANT COL (WO DIAGONAL)                   
        if err_right<err_0:
            err_0=err_right
            improved=True
        else:
            re[row]-=2*step
            ce[row]-=2*step
            #err_left=full_eval_err02(c,ob,re,ce,rx,cx,c['mod_form'],c['d_start'])
            #err_left=row_eval_err02(row,c,ob,re,ce,rx,cx)
            err_left=row_col_eval_sq_sym_err02(row,c,ob,re,ce,rx,cx)
            if err_left<err_0:
                err_0=err_left
                improved=True
            else:
                re[row]+=step
                ce[row]+=step

def nibble_e(c,ob, re,ce,rx,cx,step,improved):
    #No! this assumes square    
    nrow=size(re)
    ncol=size(ce)
    set1=range(nrow)
    set2=range(1,ncol+1)  #keep away from having 0 in both sets
    set2=list(-1*array(set2)  ) 
    #print set1
    #print set2
    #raw_input("check for pos and neg sets, used for re or for ce")
    set=set1+set2
    #random.shuffle(set)
    #print set
    for rc in set:
        if rc>=0:
            nibble_re_row(c,ob, re,ce,rx,cx,step,improved,rc)
        else:
            nibble_ce_col(c,ob, re,ce,rx,cx,step,improved,-rc-1)
                
def nibble_re(c,ob, re,ce,rx,cx,step,improved):
    nrow=size(re)
    err_0=10e20
    for row in arange(nrow):
        nibble_re_row(c,ob, re,ce,rx,cx,step,improved,row)
        
def nibble_re_row(c,ob, re,ce,rx,cx,step,improved,row):
        savep=re[row]
        #swap err evaluations during debugging
        #err_0=row_eval_err02(row,c,ob,re,ce,rx,cx)
        #print "err_0",err_0,re[row],"step",step
        err_0=full_eval_err02(c,ob,re,ce,rx,cx,c["mod_form"],c["d_start"])
        re[row]+=step
        if c["mod_type"]=="square_symmetric":ce[row]=re[row]
        #err_right=row_eval_err02(row,c,ob,re,ce,rx,cx)
        err_right=full_eval_err02(c,ob,re,ce,rx,cx,c["mod_form"],c["d_start"])
        #print "     err_RIGHT re",err_right,row,re[row]
        if err_right<err_0:
            err_0=err_right
            improved=True
        else:
            re[row]-=2*step
            if c["mod_type"]=="square_symmetric":ce[row]=re[row]
            #err_left=row_eval_err02(row,c,ob,re,ce,rx,cx)
            err_left=full_eval_err02(c,ob,re,ce,rx,cx,c["mod_form"],c["d_start"])
        #    print "        err_LEFT re",err_left,row,re[row]
            if err_left<err_0:
                err_0=err_left
                improved=True
            else:
                re[row]+=step
                if c["mod_type"]=="square_symmetric":ce[row]=re[row]
        #print '                        leaving with re[row]=',re[row]
        #raw_input("check re_row")
                
def nibble_ce(c,ob, re,ce,rx,cx,step,improved):  
    ncol=size(ce)
    err_0=10e20
    for col in arange(ncol):
        nibble_ce_col(c,ob, re,ce,rx,cx,step,improved,col) 

def nibble_ce_col(c,ob, re,ce,rx,cx,step,improved,col):  
        savep=ce[col]
        #swaps for debugging
        #err_0=col_eval_err02(col,c,ob,re,ce,rx,cx)
        err_0=full_eval_err02(c,ob,re,ce,rx,cx,c["mod_form"],c["d_start"])
        ce[col]+=step
        #err_right=col_eval_err02(col,c,ob,re,ce,rx,cx)
        err_right=full_eval_err02(c,ob,re,ce,rx,cx,c["mod_form"],c["d_start"])

        if err_right<err_0:
            err_0=err_right
            improved=True
        else:
            ce[col]-=2*step
            #err_left=col_eval_err02(col,c,ob,re,ce,rx,cx)
            err_left=full_eval_err02(c,ob,re,ce,rx,cx,c["mod_form"],c["d_start"])
            if err_left<err_0:
                err_0=err_left
                improved=True
            else:
                ce[col]+=step

#bookmark CCC
def nibble_dimension_of_rx_identical_to_cx_sq_asym(c,obLL,dimension, re,ce,rx,cx,step,improved):
    rx[:,:]=cx[:,:]   #Insurance -- probably not necessary    
    nrow=size(re)
    err_0=10e20
    #print "top of nibble_dimension_of_rx, dimension=",dimension
    row_numbers=arange(nrow)    #range(nrow)
    #random.shuffle(row_numbers)
    #debug
    #errx=full_eval_err02(c,obLL,re,ce,rx,cx,c['mod_form'],c['d_start'])
    #print "\nNew Starting error:  ",comma_form(errx)
    #raw_input("debugging for CA too large at 1016 before nibble_dimension_of_rx_ident")
    #print "debugging at 872"


    #debug: find out where rx is departing from cx (on the map, rx is staying near 0)
    same=True
    message=""
    for ii in range(size(rx,0)):
        for dd in range(size(rx,1)):
            if rx[ii,dd]!=cx[ii,dd]:
                same=False
                message+=str(ii)+" "+str(dd)+" "+str(rx[ii,dd])+"!="+str(cx[ii,dd])
                message+="  difference  "+str(rx[ii,dd]-cx[ii,dd])+"\n"
                                 
    if not same:
        raw_input("rx != cx at 966  before nibbling on rx ident \n"+message)
                    


        
    for row in row_numbers: #arange(nrow):  #This says, 'for item in array'.  I'm surprised it works.  But it treats it like a list    
        nibble_dimension_of_rx_identical_to_cx_row_sq_asym_dim(c,obLL,dimension, re,ce,rx,cx,step,improved,row)

    #debug
    #errx=full_eval_err02(c,obLL,re,ce,rx,cx,c['mod_form'],c['d_start'])
    #print "\nNew Starting error:  ",comma_form(errx)
    #raw_input("debugging for CA too large at 1022 after nibble dimension of rx ident")
    #print "debugging at 883"


    #debug: find out where rx is departing from cx (on the map, rx is staying near 0)
    same=True
    message=""
    for ii in range(size(rx,0)):
        for dd in range(size(rx,1)):
            if rx[ii,dd]!=cx[ii,dd]:
                same=False
                message+=str(ii)+" "+str(dd)+" "+str(rx[ii,dd])+"!="+str(cx[ii,dd])
                message+="  difference  "+str(rx[ii,dd]-cx[ii,dd])+"\n"
                                 
    if not same:
        raw_input("rx != cx at 992  before nibbling on rx ident \n"+message)
                    


        

#culprit?
        #Not working with specialized eval
def nibble_dimension_of_rx_identical_to_cx_row_sq_asym_dim(c,ob,dimension, re,ce,rx,cx,step,improved,row):
        #Insurance:  (One graph of Burt stuff (square symm with missing data is drifting during iterations
        rx[:,:]=cx[:,:]
        #continue
        #print "debug inside nibble_dimension_of_rx..."
        #print rx
        #print cx
        savepr=rx[row,dimension]        
        savepc=cx[row,dimension]        
#temporarily be sure the error is in row_eval_err02
        #err_0=full_eval_err02(c,ob,re,ce,rx,cx,c['mod_form'],c['d_start'])
        #err_0=row_eval_err02(row,c,ob,re,ce,rx,cx)
        #err_0=row_col_eval_err02(row,c,ob,re,ce,rx,cx)
        err_0=row_col_eval_sq_asym_err02(row,c,ob,re,ce,rx,cx)
        #print "debug row",row,"dimension",dimension,"step"
        #print "debug err0 at 972                    ",err_0,savepr
        rx[row,dimension]+=step
        cx[row,dimension]+=step
#temporarily be sure the error is in row_eval_err02
        #err_right=full_eval_err02(c,ob,re,ce,rx,cx,c['mod_form'],c['d_start'])
        #err_right=row_eval_err02(row,c,ob,re,ce,rx,cx)
        #err_right=row_col_eval_err02(row,c,ob,re,ce,rx,cx) #efficient but not working
        err_right=row_col_eval_sq_asym_err02(row,c,ob,re,ce,rx,cx)
        #print "debug err_right 979:                               ",err_right,rx[row,dimension]
        if err_right<err_0:
            err_0=err_right;    improved=True
        else:
            rx[row,dimension]-=2*step
            cx[row,dimension]-=2*step
#temporarily be sure the error is in row_eval_err02
            #err_left=full_eval_err02(c,ob,re,ce,rx,cx,c['mod_form'],c['d_start'])
            #err_left=row_eval_err02(row,c,ob,re,ce,rx,cx)
            #err_left=row_col_eval_err02(row,c,ob,re,ce,rx,cx)
            err_left=row_col_eval_sq_asym_err02(row,c,ob,re,ce,rx,cx)
            #print "debug err_left 991:",err_left,rx[row,dimension]
            if err_left<err_0:
                err_0=err_left; improved=True
            else:
                rx[row,dimension]+=step
                cx[row,dimension]+=step
        
                
def nibble_dimension_of_rx_identical_to_cx_sq_sym(c,obLL,dimension, re,ce,rx,cx,step,improved):
    rx[:,:]=cx[:,:]  #Insurance.  It should not be necessary.   
    nrow=size(re)
    err_0=10e20
    #print "top of nibble_dimension_of_rx, dimension=",dimension
    row_numbers=arange(nrow)    #range(nrow)
    #remove for debugging:
    #random.shuffle(row_numbers)
    #debug
    #errx=full_eval_err02(c,obLL,re,ce,rx,cx,c['mod_form'],c['d_start'])
    #print "\nNew Starting error:  ",comma_form(errx)
    #raw_input("debugging for CA too large at 1016 before nibble_dimension_of_rx_ident")
    #print "debugging at 876"
        
    for row in row_numbers: #arange(nrow):  #This says, 'for item in array'.  I'm surprised it works.  But it treats it like a list    
        nibble_dimension_of_rx_identical_to_cx_row_sq_sym_dim(c,obLL,dimension, re,ce,rx,cx,step,improved,row)
    #debug
    #errx=full_eval_err02(c,obLL,re,ce,rx,cx,c['mod_form'],c['d_start'])
    #print "\nNew Starting error:  ",comma_form(errx)
    #raw_input("debugging for CA too large at 1022 after nibble dimension of rx ident")
    #print "debugging at 884"

def nibble_dimension_of_rx_identical_to_cx_row_sq_sym_dim(c,ob,dimension, re,ce,rx,cx,step,improved,row):
        #Insurance:  (One graph of Burt stuff (square symm with missing data is drifting during iterations
        rx[:,:]=cx[:,:]
        #continue
        savepr=rx[row,dimension]        
        savepc=cx[row,dimension]        
#temporarily be sure the error is in row_eval_err02
        #err_0=full_eval_err02(c,ob,re,ce,rx,cx,c['mod_form'],c['d_start'])
        #err_0=row_eval_err02(row,c,ob,re,ce,rx,cx)
        #err_0=row_col_eval_err02(row,c,ob,re,ce,rx,cx)
        err_0=row_col_eval_sq_sym_err02(row,c,ob,re,ce,rx,cx)
        rx[row,dimension]+=step
        cx[row,dimension]+=step
#temporarily be sure the error is in row_eval_err02
        #err_right=full_eval_err02(c,ob,re,ce,rx,cx,c['mod_form'],c['d_start'])
        #err_right=row_eval_err02(row,c,ob,re,ce,rx,cx)
        #err_right=row_col_eval_err02(row,c,ob,re,ce,rx,cx) #efficient but not working
        err_right=row_col_eval_sq_sym_err02(row,c,ob,re,ce,rx,cx)
        if err_right<err_0:
            err_0=err_right;    improved=True
        else:
            rx[row,dimension]-=2*step
            cx[row,dimension]-=2*step
#temporarily be sure the error is in row_eval_err02
            #err_left=full_eval_err02(c,ob,re,ce,rx,cx,c['mod_form'],c['d_start'])
            #err_left=row_eval_err02(row,c,ob,re,ce,rx,cx)
            #err_left=row_col_eval_err02(row,c,ob,re,ce,rx,cx)
            err_left=row_col_eval_sq_sym_err02(row,c,ob,re,ce,rx,cx)
            if err_left<err_0:
                err_0=err_left; improved=True
            else:
                rx[row,dimension]+=step
                cx[row,dimension]+=step


def nibble_xxxx(c,ob, re,ce,rx,cx,step,improved):
    nrow=size(re)
    ncol=size(ce)
    ndim=size(rx,1)
    
    set1=range(nrow)
    set2=range(1,ncol+1)  #keep away from having 0 in both sets
    set2=list(-1*array(set2)  ) 
    #print set1
    #print set2
    #raw_input("check for pos and neg sets, used for re or for ce")
    set=set1+set2

    for dim in xrange(ndim):
            #random.shuffle(set)
            #print set
            for rc in set:
                if rc>=0:
                    nibble_dimension_of_rx_row_dim(c,ob,dim, re,ce,rx,cx,step,improved,rc)
                else:
                    nibble_dimension_of_cx_col_dim(c,ob,dim, re,ce,rx,cx,step,improved,-rc-1)
                    

def nibble_x(c,ob, re,ce,rx,cx,step,improved):
        nrow=size(re)
        ncol=size(ce)
        ndim=size(rx,1)

        set=[]
        for dim in xrange(ndim):
                for row in range(nrow):
                        set.append(["rx",row,dim])
                for col in range(ncol):
                        set.append(["cx",col,dim])
        #random.shuffle(set)                
    
        for item in set:
                rc,k,d=item        
                if rc=="rx":
                        nibble_dimension_of_rx_row_dim(c,ob,d, re,ce,rx,cx,step,improved,k)
                else:
                        nibble_dimension_of_cx_col_dim(c,ob,d, re,ce,rx,cx,step,improved,k)
                        
def nibble_x02(c,ob, re,ce,rx,cx,step,improved):
        #Since I'm having trouble fixing the alternative to nibble_x
        #maybe I can generalize nibble_x to the necessary cases
        nrow=size(re)
        ncol=size(ce)
        ndim=size(rx,1)
        mod_type=c["mod_type"]

        set=[]
        for dim in xrange(ndim):
                for row in range(nrow):
                        set.append(["rx",row,dim])
                for col in range(ncol):
                        set.append(["cx",col,dim])
        #random.shuffle(set)                
    
        for item in set:
                rc,k,d=item
                if mod_type=="rectangular":
                        if rc=="rx":
                                nibble_dimension_of_rx_row_dim(c,ob,d, re,ce,rx,cx,step,improved,k)
                        else:
                                nibble_dimension_of_cx_col_dim(c,ob,d, re,ce,rx,cx,step,improved,k)
                elif mod_type=="square_asymmetric":
                        #print "culprit at 1115  "*3
                        #nibble_dimension_of_rx_row_dim(c,ob,d, re,ce,rx,cx,step,improved,k)
                        #nibble_dimension_of_cx_col_dim(c,ob,d, re,ce,rx,cx,step,improved,k)
#This is the culprit
                        nibble_dimension_of_rx_identical_to_cx_row_sq_asym_dim(c,ob,
                                        d, re,ce,rx,cx,step,improved,k)
                elif mod_type=="square_symmetric":        
                        nibble_dimension_of_rx_identical_to_cx_row_sq_sym_dim(c,ob,
                                        d, re,ce,rx,cx,step,improved,k)
                else:
                        raw_input("impossible mod_type at 1121: "+mod_type)

##        #debug: find out where rx is departing from cx (on the map, rx is staying near 0)
##        same=True
##        message=""
##        for ii in range(size(rx,0)):
##                for dd in range(size(rx,1)):
##                         if rx[ii,dd]!=cx[ii,dd]:
##                                 same=False
##                                 message+=str(ii)+" "+str(dd)+" "+str(rx[ii,dd])+"!="+str(cx[ii,dd])
##                                 message+="  difference  "+str(rx[ii,dd]-cx[ii,dd])+"\n"
##                                 
##        if not same:
##                raw_input("rx != cx at 1139 \n"+message)
                    
            
def nibble_dimension_of_rx(c,obLL,dimension, re,ce,rx,cx,step,improved):  
    nrow=size(re)
    err_0=10e20
    #print "top of nibble_dimension_of_rx, dimension=",dimension
    for row in arange(nrow):
        nibble_dimension_of_rx_row_dim(c,obLL,dimension, re,ce,rx,cx,step,improved,row)
        
def nibble_dimension_of_rx_row_dim(c,obLL,dimension, re,ce,rx,cx,step,improved,row):  
        savep=rx[row,dimension]        
        err_0=row_eval_err02(row,c,obLL,re,ce,rx,cx)
        rx[row,dimension]+=step
        err_right=row_eval_err02(row,c,obLL,re,ce,rx,cx)

        if err_right<err_0:
            err_0=err_right;    improved=True
        else:
            rx[row,dimension]-=2*step
            err_left=row_eval_err02(row,c,obLL,re,ce,rx,cx)
            if err_left<err_0:
                err_0=err_left; improved=True
            else:
                rx[row,dimension]+=step
            
def nibble_dimension_of_cx(c,obLL,dimension, re,ce,rx,cx,step,improved):  
    ncol=size(ce)  #This is nrow of the vector, not nrow of the data
    err_0=10e20
    for col in arange(ncol):
        nibble_dimension_of_cx_col_dim(c,obLL,dimension, re,ce,rx,cx,step,improved,col) 

def nibble_dimension_of_cx_col_dim(c,obLL,dimension, re,ce,rx,cx,step,improved,col):  
        savep=cx[col,dimension]
        
        err_0=          col_eval_err02(col,c,obLL,re,ce,rx,cx)
        cx[col,dimension]+=step
        err_right=      col_eval_err02(col,c,obLL,re,ce,rx,cx)

        if err_right<err_0:
            err_0=err_right;    improved=True    
        else:
            cx[col,dimension]-=2*step
            err_left=   col_eval_err02(col,c,obLL,re,ce,rx,cx)
            if err_left<err_0:
                err_0=err_left; improved=True
            else:
                cx[col,dimension]+=step                                        
       
def quick_view5(obLL,re,ce,rx,cx,rlab,clab):
    nrow=size(obLL)
    ncol=size(obLL[0])
    print "nrow and ncol=",nrow," and ",ncol
    print "ob"  #Verify
    rlim=min(nrow,5);   clim=min(ncol,5)
    print "\nVerfying data or FIRST 5 ROWS and 5 COLUMNS:"    

    #print ob[0:rlim,0:clim]
    for row in arange(rlim):
        try:    
            print obLL[row][:clim]
        except:
            print "\n\nFailure in dwvB037 inside quick_view5"
            print "rlim",rlim
            print "clim",clim
            print "nrow from rlab",len(rlab)
            print "ncol from clab",len(clab)
            print "nrow from len re",len(re)
            print "ncol from len ce",len(ce)
            print "row",row
            print "rlab",rlab
            print "clim",clim
            print "obLL"
            print obLL
            #print rlab[row]
            
    print "\n\nFirst five ROW LABELS:"
    print rlab[:rlim]
    print "\nFirst five COLUMN LABELs"
    print clab[:clim]
    
    #print "\n\nStarting effects for first 5 rows:\n",re[:rlim]
    #print "\n\nStarting coordinates for first 5 rows:"
    #print rx[:rlim,:]
    #print "\n\nStarting effects for first 5 columns:"
    #print ce[:clim]
    #print "\nStarting coordinates for first 5 columns:"
    #print cx[:clim,:]
    
def standardize_parameters(re,ce,rx,cs,mod_type,minkowski_power,
                           damper=1.):

    ## 9/15/08 This was not doing anything, the damper was defaulting to default 0
    ## remove the messing with the coordinates.  Restore adjustment of multipliers
    ## using default damper 1    

    #damper=.5  #Looks like I wrote the routine and then turned it off the damping

    #Effects of standardization are too great for the optimizer to overcome.  Damp them    
    re_mean=sum(re[0:])/float(nrow)  #re_mean=re.sum()/float(nrow)
    ce_mean=sum(ce[0:])/float(ncol)
    diff=ce_mean-re_mean
    half_diff=diff*.5
    re[0:]+=damper*half_diff
    ce[0:]-=damper*half_diff

##    if minkowski!=2:
##        junk=zeros((nrow+ncol),float)
##        for d in arange(ndim):
##            junk[0:nrow]=rx[0:nrow,d]
##            junk[nrow:nrow+ncol]=cx[0:ncol,d]
##            mean=sum(junk[0:])/float(nrow+ncol)
##            junk[0:]-=damper*mean
##            # no need to read it back in to the original.  It is already there.
##    else:
##        for d in arange(ndim):
##            xmean=sum(rx[0:,d])/float(nrow)
##            rx[0:,d]-=damper*xmean
##            ymean=sum(cx[0:,d])/float(ncol)
##            cx[0:,d]-=damper*ymean
##
##
##    #re-order dimensions by their variance
##    sd=[]
##    for d in arange(ndim):
##        ss=0
##        for r in arange(nrow):
##            ss+=rx[r,d]**2   # can rewrite using numpy documentation
##        for c in arange(ncol):
##            ss+=cx[c,d]**2
##        sd.append([ss,rx[:,d],cx[:,d]])
##    sd.sort()
##    sd.reverse()
##    for d in arange(ndim):
##            rx[:,d]=sd[d][1]
##            cx[:,d]=sd[d][2]
##                  
##        

    return re,ce,rx,cx

# NOT orthonormal basis (orthogonal, with each vector having unit length
def gram_schmidt(nrow,ncol,array):

    basis=zeros((nrow,ncol),float)       #orthogonal and normal (unit vectors) or sd=1
    components=zeros((nrow,ncol),float)  #orthogonal remainders
    for row in arange(nrow):
        for col in arange(ncol):
            components[row,col]=1*array[row,col]   

    for col in arange(1,ncol):  #each column after the first is made orthogonal to all predecessors
        for preceeding in arange(col):
            #print "preceding",preceeding
            #print "removing projection onto ",preceeding,"from vector",col
            numerator=0.
            denominator=0.
            for row in arange(nrow):
                crp=components[row,preceeding]
                numerator+=components[row,col]*crp
                denominator+=crp*crp
            for row in arange(nrow):
                components[row,col]-=(numerator/denominator)*components[row,preceeding]

    for col in arange(ncol):
        average_length=0
        for row in arange(nrow):
            average_length+=components[row,col]**2
        average_length/=float(nrow)    
        average_length**=.5
        for row in arange(nrow):
            basis[row,col]=components[row,col]/(2*average_length) #shorter
    return components,basis        

def combine_principal_components(rx,cx,nrow,ncol,ndim):
        #print "incoming:",type(rx),type(cx)
        r_and_cx=zeros((nrow+ncol,ndim))
        r_and_cx[0:nrow,:ndim]=rx[0:nrow,:ndim]
        r_and_cx[nrow:nrow+ncol]=cx[0:ncol,:ndim]
        #print "doing pc"
        #raw_input("")
        r_and_cx=principle_components.pc(nrow+ncol,ndim,r_and_cx)
        r=array(r_and_cx[0:nrow,:ndim])
        c=array(r_and_cx[nrow:nrow+ncol,:ndim])
        #print "returning:",type(r),type(c)
        #raw_input("")
        return r,c

def combine_order_positive_skew(rx,cx,nrow,ncol,ndim):
        #print "incoming:",type(rx),type(cx)
        r_and_cx=zeros((nrow+ncol,ndim))
        r_and_cx[0:nrow,:ndim]=rx[0:nrow,:ndim]
        r_and_cx[nrow:nrow+ncol]=cx[0:ncol,:ndim]
        #print "doing pc"
        #raw_input("")
        #r_and_cx=principle_components.positive_skew(r_and_cx)
        r_and_cx=order_column_vectors_by_variance.order_column_vectors_by_variance(r_and_cx)
        r=array(r_and_cx[0:nrow,:ndim])
        c=array(r_and_cx[nrow:nrow+ncol,:ndim])
        #print "returning:",type(r),type(c)
        #raw_input("")
        return r,c
                
def opt(self,npass,c,obLL,
        re_original,ce_original,rx_original,cx_original,
        rlab,clab,n_opt_iter,note,least_err):

    mod_type=c["mod_type"]
    if mod_type=="square_symmetric":
        ce_original[:]=re_original[:]
        cx_original[:,:]=rx_original[:,:]
    if mod_type=="square_asymmetric":
        cx_original[:]=rx_original[:]
    #used for evaluations while searching for a bug:     
    mod_form=c["mod_form"]
    d_start=c["d_start"]   
    opt_minkowski=c["opt_minkowski"]
    opt_attenuation=c["opt_attenuation"]
    opt_d_start=c["opt_d_start"]
    re=re_original[:]; ce=ce_original[:]; rx=rx_original[:,:]; cx=cx_original[:,:]

    #debug
    #maxe_diff=0
    #for iii in range(size(re)):
    #    e_diff=abs(re[iii]-ce[iii])
    #    if e_diff>maxe_diff: maxe_diff=e_diff
    #print "1434 max difference of re versus ce",maxe_diff
    #raw_input("1434 at top of opt")



    
    #global canvas  #having canvas global may be the source of many problems.  However,
    #for the moment this may allow me to get rid of it when useful

##        raw_input( "ready to fork")
##        #Trying to close the graphics, Tk window inorder to reopen it
##        for p in pid_list:
##                print "killing  pid",p
##                os.kill(p,signal.SIGKILL)
##        newpid=os.fork()
##        if newpid==0: #child
##                rectangle_driver006inprocess.rectangle_driver_setup_mat006(c['nrow'],c['ncol'],c['ndim'],rx,cx,
##                        obLL,rlab,clab,"temp_file",c)
##                tk().quit()
##        else:  #parent
##                pid_list.append(newpid)
##                raw_input("continuing main program")


        #print shape(rx),type(rx),shape(cx),type(cx)
    ## the pc and standardization is not mathematically correct for mink!=2 atten!=2
    ## However, it seems to work for nudging out of local minima -- for which it
    ## then works out of the errors introduced by the nudging -- try it.
    #try for fewer nudges after start by doing every 2nd or every 3rd or ...
    c['pacer_modulus']=2
    try:
        c['pacer']+=1
        c['pacer']=c['pacer']%c['pacer_modulus']  #count by modulo
    except:  #where 'pacer' had no value
        print "Resetting pacer to 0"    
        c['pacer']=0            
            

    #if c["minkowski_power"]==2 or c["inside_a_semi-start"]: # or npass<1000:

    #Removed 7/6/09 for Ian's stuff (that doesn't replicate)
    #but it has been in use, eg for SP data
    #if c["minkowski_power"]==2 or c["inside_a_semi-start"]: # or c['pacer']==0:


    #debug
    #debug
    #maxe_diff=0
    #for iii in range(size(re)):
    #    e_diff=abs(re[iii]-ce[iii])
    #    if e_diff>maxe_diff: maxe_diff=e_diff
    #print "1485 max difference of re versus ce",maxe_diff
    #raw_input("1486 at top of opt")
        
    #errx=full_eval_err02(c,obLL,re,ce,rx,cx,mod_form,d_start)
    #print "\nNew Starting error:  ",comma_form(errx)
    #raw_input("debugging for CA too large at 11340 in opt, before some standardizing")

    
    if c["minkowski_power"]==2 and c["attenuation_power"]==2: # or c["inside_a_semi-start"]: # or c['pacer']==0:
        #print "pc:  minkowski_power==2 and/or inside_a_semi-start" #or npass<1000"
        print "pc:  minkowski_power==2 and/or inside_a_semi-start and/or npass==0"
        print "minkowski_power:  ",c['minkowski_power'],
        print "inside_a_semi-start:  ",c['inside_a_semi-start'],
        print ".  Pacer:  ",c['pacer'],",modulus",c['pacer_modulus']                                    
                                    
        rx,cx=combine_principal_components(rx,cx,c["nrow"],c["ncol"],c["ndim"])
        if c["attenuation_power"]==2:
                rx,cx=standardizep2a2.standardize_variance(rx,cx)
        else:  #temporary, see notes below
            if npass<1000:    
                print "Kludge standardized variances"
                rx,cx=standardizep2a2.standardize_variance(rx,cx)
        
    else:             
        print "Kludge wtd pc and standardized variances"
        #The problem appears to be that I should shuffle r and c coordinates during nibble
        #For the moment it is severely handicapped for Non-Euclidean, Non-Gaussian
        #But this is some improvement.
        if 1==0:

                #Line removed 7/6/09 like the above
                rx1,cx1=combine_principal_components(rx,cx,c["nrow"],c["ncol"],c["ndim"])
                rx2,cx2=standardizep2a2.standardize_variance(rx1,cx1)
                wt1=.01
                wt2=1.-wt1
                rx=(wt1*rx+wt2*rx2)
                cx=(wt1*cx+wt2*cx2)
##    #debug
##    errx=full_eval_err02(c,obLL,re,ce,rx,cx,mod_form,d_start)
##    print "\nNew Starting error:  ",comma_form(errx)
##    raw_input("debugging for CA too large at 1375 AFTER    some standardizing")
##
##    #debug
##    maxe_diff=0
##    for iii in range(size(re)):
##        e_diff=abs(re[iii]-ce[iii])
##        if e_diff>maxe_diff: maxe_diff=e_diff
##    print "1532 max difference of re versus ce",maxe_diff
##    raw_input("1532 ")
                
    #print "re-order, force positive skew"    
    rx,cx=combine_order_positive_skew(rx,cx,c["nrow"],c["ncol"],c["ndim"])

    print "\nBacking off with rounding at AA " #  TURNED OFF, TRY WITH IAN's DATA"
    
    rx=round_array(rx[:,:],3)
    if mod_type=="square_symmetric":
        cx=rx
    else:    
        cx=round_array(cx[:,:],3)

    # I suspect that initially, when fit is bad, it tries to accommodate by
    # increasing the attenuation power.  Therefore, hold it back until things get
    # better.  Keep it constant during a semi_start.
    if opt_minkowski   and not c["inside_a_semi-start"]: c["minkowski_power"]+=random.uniform(-.0025,.0025)
    if opt_attenuation and not c["inside_a_semi-start"]: c["attenuation_power"]+=random.uniform(-.0025,.0025)

     

    if c['last_column_gt_first_column']:
        mult=0.
        #mid=int(size(cx,0)/2)    
        #mid=int(size(cx,0)*.66)  #for current work that is last month of 3  
        for d in range(size(cx,1)):
            mid=int(size(cx,0)*mult)  #for current work that is last month of 3  
            #comparing last to first ignores curvature of a parabola, it can be going down
            #even if last point is greater than first.  So compare to middle
                
            if cx[-1,d]-cx[mid,d]<0:  
                print "forcing change of sign, dimension ",d," positive."
                cx[:,d]*=-1.
                rx[:,d]*=-1.
            else:
                print "checking mid=",mid,"midle",cx[mid,d],"last",cx[-1,d], "mult",mult   
            mult=  1.-((1.-mult)*.5) #move half way to 1 (cycles get faster)    

    #if c['nudge_columns_toward_table_order']:
    #print "\n  imposing repeated running medians of 3 column coordinates in calendar order.\n"
    #for d in range(size(cx,1)):
    #    cx[:,d]=running_medians(cx[:,d])

    #print re
    #print
    #print ce
    #errx=full_eval_err02(c,obLL,re,ce,rx,cx,mod_form,d_start)
    #print "\nNew Starting error:  ",comma_form(errx)
    #raw_input("debugging for CA too large at 1432 after AA")

    pid_list=[]    
    ke=c.keys()
    ke.sort()
    #for k in ke:
    #        print k,c[k]
    #raw_input("check c")
    #err1=full_eval_err(c,obLL,re,ce,rx,cx)
    err1=full_eval_err02(c,obLL,re,ce,rx,cx,mod_form,d_start)

    t0=time.ctime()
    round_to=5

    e_step=.1; x_step=.1;attenuation_step=.01; minkowski_step=.01; d_start_step=.01
    #if c["mod_form"]=="CA":  x_step=.01
    #x_step=.001  #debug

    #rx=2*rx
#    if 1==1: #if c["minkowski_power"]==2:
#        rx,cx=combine_principal_components(rx,cx,c["nrow"],c["ncol"],c["ndim"])
    #err1=full_eval_err(c,obLL,re,ce,rx,cx)
    err1=full_eval_err02(c,obLL,re,ce,rx,cx,mod_form,d_start)
    #print "err1 after pc",err1
    #raw_input("")
    
##    if 1==1:  #back off a little to add a bit of randomization and roughness (avoiding local minima)
##        for dim in xrange(c["ndim"]):
##            for row in xrange(c["nrow"]):
##                rx[row,dim]+=(random.uniform(-.5,.5))/float(10**round_to)
##            if c["mod_type"]=="rectangular":
##                for col in xrange(c["ncol"]):
##                    cx[col,dim]+=(random.uniform(-.5,.5))/float(10**round_to)
                    
    line=comma_form(err1)+"  mod_type= "+c["mod_type"]+", Number of dimensions="+str(c["ndim"])
    line+= ", Minkowski_power="+str(c["minkowski_power"])+", Attenuation power="+str(c["attenuation_power"])
    line+=", nrow="+str(c["nrow"])+", ncol="+str(c["ncol"])+"\n"
    c_keys=c.keys()
    c_keys.sort()
    print "controls for this run:"
    for ck in c_keys:
        print ck,c[ck]
    print line
    pid_list=[]
    for full_pass in xrange(n_opt_iter): #32 (3 for speed during debugging)


#Curious--  what if I impose running medians every time?

#        print "\n imposing repeated running medians of 3 column coordinates in calendar order.\n"
#        for d in range(size(cx,1)):
#            cx[:,d]=running_medians(cx[:,d])
#        Answer:  Fit is much worse.  Overnight 61,544 with these lines versus 46245 without them (for retrospective 7/18/08 run)


        #print "full_pass",full_pass    
##        raw_input("ready_to_fork")
##        for pi in pid_list:
##                print "killing pid:",pi
##                #os.kill(pi,signal.SIGKILL)
##                raw_input("did something get told to stop?")
##        newpid=os.fork()
##        if newpid==0: #child
##                print "child calling graphics",newpid 
##                rectangle_driver006inprocess.rectangle_driver_setup_mat006(c['nrow'],c['ncol'],c['ndim'],rx,cx,
##                        obLL,rlab,clab,"temp_file",c)
##        elif newpid!=0: #parent
        if 1==1:
##                raw_input("try to forget canvas")
##                try:
##                        #canvas=""
##                        print "succeeded?"
##                except:
##                        pass
##                rectangle_driver006inprocess.rectangle_driver_setup_mat006(c['nrow'],c['ncol'],c['ndim'],rx,cx,
##                        obLL,rlab,clab,"temp_file",c)
               
                #print "debug full_pass",full_pass,"n_opt_iter",n_opt_iter
                #print "parent appending pid",newpid
                #pid_list.append(newpid)
                improved=False
                npass+=1
                #raw_input( "near top of opt, calling nibble_re")
                #print "debug circa 1075", size(rx,0),size(rx,1),size(cx,0),size(cx,1)
                #raw_input("")

                #debug
                #errx=full_eval_err02(c,obLL,re,ce,rx,cx,mod_form,d_start)
                #print "\nNew Starting error:  ",comma_form(errx)
                #raw_input("debugging for CA too large at 1494")

                #debug
                #maxe_diff=0
                #for iii in range(size(re)):
                #    e_diff=abs(re[iii]-ce[iii])
                #    if e_diff>maxe_diff: maxe_diff=e_diff
                #print "1663 max difference of re versus ce",maxe_diff
                #raw_input("1663 ")

                #do multipliers
                mod_type=c["mod_type"]
                if mod_type=="rectangular" or mod_type=="square_asymmetric":  #corrected adding sq asym 2/7/10
                    #Need to randomize search of all parameters (for nonEuclidean,non Gaussian
                    #temporary help.  At least reandomize blocks of searches.
                    if 1==0:
                        nibble_e(c,obLL, re,ce,rx,cx,e_step,improved) #Yipe, this assumed square
                    else:
                        print "dwvC103 line 1927"    
                        if random.random()>.5:    



                            nibble_re(c,obLL, re,ce,rx,cx,e_step,improved)



                            
                            nibble_ce(c,obLL, re,ce,rx,cx,e_step,improved)


                

                            
                        else:    
                            nibble_ce(c,obLL, re,ce,rx,cx,e_step,improved)
                            nibble_re(c,obLL, re,ce,rx,cx,e_step,improved)
                elif c["mod_type"]=="square_symmetric":
                    #debug
                    #errx=full_eval_err02(c,obLL,re,ce,rx,cx,mod_form,d_start)
                    #print "\nNew Starting error:  ",comma_form(errx)
                    #raw_input("debugging for CA too large at 1535")
                    nibble_re_identical_to_ce_sq_sym(c,obLL, re,ce,rx,cx,e_step,improved)
                #debug
                #maxe_diff=0
                #for iii in range(size(re)):
                #    e_diff=abs(re[iii]-ce[iii])
                #    if e_diff>maxe_diff: maxe_diff=e_diff
                #print "1532 max difference of re versus ce",maxe_diff
                #raw_input("1532 ")
                    

                #err2=full_eval_err(c,obLL,re,ce,rx,cx)
                err2=full_eval_err02(c,obLL,re,ce,rx,cx,mod_form,d_start)
                #print "1954 err2:",err2
                if err2>=err1:
                    e_step*=.5
                else:
                    e_step*=1.05
                err1=err2


                #do coordinates

                #or do  whole dimension, one dim at a time
                #2/1/09  This may be the reason I am getting Euclidean  solutions, Atten 2
                #more than expected.  If there is a large scale correction necessary, one will
                #surround the other, absorbing the scale corrections.  That helps initially,
                #but it moves toward solutions with rows distributed on one line with columns
                #expanded on another line at right angles to the first.
                #Euclidean, atten 2 solutions are not affected since, for those scales are
                #easily corrected and are corrected, adding a pc rotation in the bargain.
                mod_type=c["mod_type"]
                if 1==1:
                    nibble_x02(c,obLL, re,ce,rx,cx,x_step,improved)  #2/14/10 removd -- this may be why shuffle did not work

                else:
                    dim_set=range(c["ndim"])
                    #random.shuffle(dim_set)
                    for dim in dim_set: #xrange(c["ndim"]):
                        #raw_input(mod_type+" at 1547")    
                        if mod_type=="rectangular":
                            #see note on nibble_ce -- half fix of bigger problem is random here
                            if random.random()>.5:    
                                nibble_dimension_of_rx(c,obLL,dim, re,ce,rx,cx,x_step,improved)
                                nibble_dimension_of_cx(c,obLL,dim, re,ce,rx,cx,x_step,improved)
                            else:    
                                nibble_dimension_of_cx(c,obLL,dim, re,ce,rx,cx,x_step,improved)
                                nibble_dimension_of_rx(c,obLL,dim, re,ce,rx,cx,x_step,improved)
                        elif mod_type=="square_symmetric":
                            cx=rx    
                            nibble_dimension_of_rx_identical_to_cx_sq_sym(c,obLL,dim, re,ce,rx,cx,x_step,improved)
                        elif mod_type=="square_asymmetric":
                            #print "debug 1560",mod_type    
                            cx=rx    
                            nibble_dimension_of_rx_identical_to_cx_sq_asym(c,obLL,dim, re,ce,rx,cx,x_step,improved)

                        else:
                            raw_input("mod_type <"+mod_type+"> not recognized.")
                            sys.exit()

                #err2=full_eval_err(c,obLL,re,ce,rx,cx)
                err2=full_eval_err02(c,obLL,re,ce,rx,cx,mod_form,d_start)
                #print "294 err2:",err2
                if err2>=err1:
                    x_step*=.5
                else:
                    x_step*=1.05
                err1=err2
                
                if err2<1e-6:  break
                if e_step<1e-10 and x_step<1e-10:  break


                if opt_attenuation and (not c["inside_a_semi-start"] or c["continuation_or_startup"]=="continuation"):  #Can't use nibble_vector (because if I embed it in a vector it isn't interpreted as itself)
                    #print "debug at line 1807, opt_attenuation",opt_attenuation

                    c["attenuation_power"]+=attenuation_step
                    err_right=full_eval_err02(c,obLL,re,ce,rx,cx,mod_form,d_start)

                    if err_right<err2:
                        err2=err_right
                        attenuation_step*=1.05
                    else:
                        c["attenuation_power"]-=2*attenuation_step
                        err_left=full_eval_err02(c,obLL,re,ce,rx,cx,mod_form,d_start)
                        if err_left<err2:
                            err2=err_left
                            attenuation_step*=1.05
                        else:
                            c["attenuation_power"]+=attenuation_step
                            attenuation_step*=.5

                #print "2035 err2",err2,full_eval_err02(c,obLL,re,ce,rx,cx,mod_form,d_start)

                if opt_minkowski and (not c["inside_a_semi-start"] or c["continuation_or_startup"]=="continuation"):

                    c["minkowski_power"]+=minkowski_step
                    err_right=full_eval_err02(c,obLL,re,ce,rx,cx,mod_form,d_start)

                    if err_right<err2:
                        err2=err_right
                        minkowski_step*=1.05
                    else:
                        c["minkowski_power"]-=2*minkowski_step

                        err_left=full_eval_err02(c,obLL,re,ce,rx,cx,mod_form,d_start)
                        if err_left<err2:
                            err2=err_left
                            minkowski_step*=1.05
                        else:
                            c["minkowski_power"]+=minkowski_step
                            minkowski_step*=.5
                #print "2057 err2",err2,full_eval_err02(c,obLL,re,ce,rx,cx,mod_form,d_start)



                #print err2,"1830"
                if isnan(err2):  print "'nan' at 1830"

                #pasted (initially from dwvB052.py
                #if opt_d_start:  #Wow!  This didn't work either.  Apparently 'if opt_d_start' merely tests whether or not it has a value, any value
                #Aah, should have been obvious: opt_d_start was coming through as string rather than Boolean
                #raw_input(""+str(opt_d_start))
                if opt_d_start==True:
                    #raw_input("opt_d_start at 1921")    
                    if not c["inside_a_semi-start"] or c["continuation_or_startup"]=="continuation":    
                        #do optimize d_start
                        c["d_start"]+=d_start_step
                        err_right=full_eval_err02(c,obLL,re,ce,rx,cx,mod_form,c["d_start"])
                        if err_right<err2 and not isnan(err_right):
                            err2=err_right
                            d_start_step*=1.05
                        else:
                            c["d_start"]-=2*d_start_step

                            err_left=full_eval_err02(c,obLL,re,ce,rx,cx,mod_form,c["d_start"])
                            if err_left<err2 and not isnan(err_left):
                                err2=err_left
                                d_start_step*=1.05
                            else:
                                c["d_start"]+=d_start_step
                                d_start_step*=.5
##                #debug
##                errb=full_eval_err02(c,obLL,re,ce,rx,cx,mod_form,d_start)
##                when_uphill.append(["2678",errb])

                ###print "after d_start  2838",full_eval_err02(c,obLL,re,ce,rx,cx,mod_form,d_start)    


                #force print of detail            
                #full_eval_err02_check(c,obLL,re,ce,rx,cx,mod_form,d_start)
        
                #print "2097 err2",err2,full_eval_err02(c,obLL,re,ce,rx,cx,mod_form,c["d_start"]),c["d_start"]



                #end paste
                header_not_yet_used="npass     full_pass #   err1                      time     attntn pwr       Mink pwr   filed err   d_start   form data"
                #                    .........xxxxxxxxx.................xxxxxxxxxxxxxxxxxxx...............xxxxxxxxxxxxxxx                
                            
                c['current_error']=err2    
                line=str(int(npass))+" full_pass #"+str(full_pass+1)+", err1= "+comma_form(err2)+", "+time.ctime()[:19]+", "
                line+="attntn pwr "+str(c["attenuation_power"])+", "+"Mink pwr "+str(c["minkowski_power"])
                line+=note+' filed err '+str(least_err)+", d_start "+str(d_start)
                line+=" Form "+c["mod_form"]
                print line #,npass,n_opt_iter
                print header_not_yet_used
                line="%9i"%(npass)+"%9i"%(full_pass+1)+"%17s "%(comma_form(err1))+time.ctime()[:19]
                line+="%15s"%(str(c["attenuation_power"]))+"%15s"%(str(c["minkowski_power"]))
                line+=note+' '+str(least_err)+" "+str(d_start)
                line+=" "+c["mod_form"]
                line+=" best among previous scans %6.2f  "%c["best_of_scanned"]
                print "dwvC103 line 2131"
                truncated_file_name=c["root"]  #get the name of the data file, truncating path (Path is printed after "backing off" print to screen
                wt=truncated_file_name.rfind("/")
                truncated_file_name=truncated_file_name[wt+1:]
                line+=" "+truncated_file_name
                print line #,npass,n_opt_iter
        ##        try:
        ##            self.print_text_window(line+"\n",self.text_window)
        ##        except:
        ##            print line
                    #self.print_text_window(line+"\n",self.text_window)

                #raw_input("try to forget canvas")
                #try:
                #        #canvas=""
                #        #print "succeeded?"
                #except:
                #        pass
                #if npass<64 or npass%10==0:
                        #it is not garbage coollecint on this -- or something keeps holding memory
                #rectangle_driver006inprocess.rectangle_driver_setup_mat006(c['nrow'],c['ncol'],c['ndim'],rx,cx,
                #                obLL,rlab,clab,"temp_file",c)

##                #debug: find out where rx is departing from cx (on the map, rx is staying near 0)
##                same=True        
##                for ii in range(size(rx,0)):
##                        for dd in range(size(rx,1)):
##                                if rx[ii,dd]!=cx[ii,dd]: same=False
##                if not same:
##                        raw_input("rx != cx at 1741")


                pairs_to_draw=[]
                if c['ndim']==1:
                        pairs_to_draw=[[0,0]]  #drawn on screen DURING the run
                else:
                        pairs_to_draw=[[0,1]]
                c['pairs_to_draw']=pairs_to_draw     
                c['swap_row_labels']="sic"  #options:  False, name (default), sic, major_sic,minor_sic   
                rectangle_driver007inprocess.rectangle_driver_setup_mat006(c['nrow'],c['ncol'],c['ndim'],rx,cx,
                                obLL,rlab,clab,c['root'],c)
                #rectangle_stock_plot007.rectangle_driver_setup_mat006(c['nrow'],c['ncol'],c['ndim'],rx,cx,
                #                obLL,rlab,clab,c['root'],c)
                


##                for pi in range(len(pid_list)):
##                        print "killing pid:",pid_list[pi]
##                        os.kill(pid_list[pi],signal.SIGKILL)
##                        del pid_list[pi]
##                        raw_input("did something get told to stop?")
##                newpid=os.fork()
##                if newpid==0: #child
##                        #raw_input( "child calling graphics: "+str(newpid)) 
##                        rectangle_driver006inprocess.rectangle_driver_setup_mat006(c['nrow'],c['ncol'],c['ndim'],rx,cx,
##                                obLL,rlab,clab,"temp_file",c)
##                elif newpid!=0: #parent
##                        pid_list.append(newpid)
    print "dwvC103 line 2188"                    
    #print "for debugging only at end of opt",   full_eval_err02(c,obLL,re,ce,rx,cx,c["mod_form"])          
    return npass, re,ce,rx,cx
                


def nibble_attenuation_parameter(err_center,c,obLL,re,ce,rx,cx,attenuation_step):
            raw_input("in nibble_attenuation at 1919")
            mod_form=c["mod_form"]
    
            attenuation_power=c["attenuation_power"]
            #err_center=full_eval_err02(c,obLL,re,ce,rx,cx)

            attenuation_power+=attenuation_step
            c["attenuation_power"]=attenuation_power
            err_right=full_eval_err02(c,obLL,re,ce,rx,cx,mod_form)

            if err_right<err_center:
                err_center=err_right
                attenuation_step*=1.05
            else:
                attenuation_power-=2*attenuation_step
                c["attenuation_power"]=attenuation_power  #pass user controlled parameter (even though this has been given to the program to control)
                err_left=full_eval_err02(c,obLL,re,ce,rx,cx,mod_form)

                if err_left<err_center:
                    err_center=err_left
                    attenuation_step*=1.05
                else:
                    attenuation_power+=attenuation_step
                    c["attenuation_power"]=attenuation_power  #pass user controlled parameter (even though this has been given to the program to control)
                    attenuation_step*=.5

def nibble_minkowski_paramter(err_center,c,obLL,re,ce,rx,cx,minkowski_step):        
            mod_form=c["mod_form"]

            minkowski_power=c["minkowski_power"]
            #err_center=full_eval_err02(c,obLL,re,ce,rx,cx)

            print c["minkowski_power"]
            raw_input("1425 in nibble_mi")


            minkowski_power+=minkowski_step
            c["minkowski_power"]=minkowski_power
            err_right=full_eval_err02(c,obLL,re,ce,rx,cx,mod_form)

            if err_right<err_center:
                err_center=err_right
                minkowski_step*=1.05
            else:
                minkowski_power-=2*minkowski_step
                c["minkowski_power"]=minkowski_power
                
                err_left=full_eval_err02(c,obLL,re,ce,rx,cx,mod_form)
                if err_left<err_center:
                    err_center=err_left
                    minkowski_step*=1.05
                else:
                    minkowski_power+=minkowski_step
                    c["minkowski_power"]=minkowski_power
                    minkowski_step*=.5

def comma_form(x):

    try:    
        x2=float(x)
    
        a=str(x2)
        b=a.index(".")
        c=a[:b]
        d=a[b:]
        e=""

        count=0
        while len(c)>0:
            e=c[-1]+e
            c=c[:len(c)-1]
            count+=1
            if count%3==0 and len(c)>0: e=","+e
        return e+d    
    except:
         print
         print "error at 1808 in comma_form"
         print "x",x
         print "x2",x2
         return str(x)

def interface_to_spread_sheet(c,obLL,rm,cm,rx,cx,rlab,clab,err):
        c["error in main program"]=err
        c["rm"]=rm
        c["cm"]=cm
        c["rx"]=rx
        c["cx"]=cx
        c["rlab"]=rlab
        c["clab"]=clab

        print "debug sheet_title and data_file  Where are they coming from?"
        ck=c.keys()
        ck.sort()
        for item in ck:
                print item,"\t",c[item]
        #raw_input("look for sheet_title and or data_file")        
        
        #This will add things to the command dictionary c (so that
        #they need be added only once
        if not "sheet_title" in c:
                #data_file=c["data_file"]  #can't find where this gets in to c (and sometimes it doesn't)
                #root seems to be the same thing:
                #data_file=c["data_file"]
                data_file=c["root"]
                where_slash=data_file.rfind("/")
                c["sheet_title"]=data_file[where_slash+1:]
                c["observed_data"]=obLL
                where_suffix=data_file.rfind(".")
                c["spread_sheet_file_name"]=data_file[:where_suffix]+".slk" #a sylk file for spread sheet
        sst=dwv_spread_sheet_generator(c)
        return sst                                         
    

def outstuff1(c,re,ce,rx,cx,rlab,clab,obLL,obLL_rsum,obLL_csum,obLL_sum,best_of_scanned=False):
    #sometime this stopped working for p model, the old one, while it works
        #for i the new one.   Kludge new computations that check for
        #total error and suture to the old code

    nrow=c["nrow"];ncol=c["ncol"];ndim=c["ndim"];mod_type=c["mod_type"];use_diagonal=c["use_diagonal"]
    minkowski_power=c["minkowski_power"];attenuation_power=c["attenuation_power"]
    erf=c["erf"]
    root=c["root"]
    use_diagonal=c["use_diagonal"]
    mod_type=c["mod_type"]
    mod_form=c["mod_form"]
    d_start=c["d_start"]

    if not best_of_scanned:    
        outf=open(root+"a","w")
    else:
        outf=open(root+"aa","w")    
           
    #ndim=rx.shape[1]
    #err=full_eval_err02(c,obLL,re,ce,rx,cx,mod_form,d_start)
    err,fitted_values,error_components=full_eval_err02_FixPrintout(c,obLL,re,ce,rx,cx,mod_form,d_start)
    #evLL=full_evLL(c,re,ce,rx,cx,mod_form,d_start)
    evLL=fitted_values
    #raw_input("evLL is of type "+str(type(evLL)))
    #Weird:  it was an array, even though some of the references use list of lists notation [i][j]

    #parameters useful for output
    #eventually, when debugged, move to a function & send to a clean output file in .csv
    d_start=c["d_start"]  #bypass input 1/21/12
    nrow=c["nrow"];ncol=c["ncol"];mod_type=c["mod_type"];use_diagonal=c["use_diagonal"]
    minkowski_power=c["minkowski_power"];attenuation_power=c["attenuation_power"]
    erf=c["erf"];omission_value=c["omission_value"]


    #outf.write( "2368 first check of debugging.  These are fitted values\n")
    #outf.write( "obLL is of type"+str(type(obLL))+"\n" )   OK obLL is really an array not a list of lists
    for rr in range(nrow):
        outf.write(str(fitted_values[rr,:])+"\n")    
    for rr in range(nrow):
        outf.write(str(error_components[rr,:])+"\n")
    outf.write("debug first 10 rows of error")
    outf.write(str(error_components[:10,:]))
    outf.write("sums of row errors\n"  )
    err_line=clab[0]
    for cc in range(ncol):
        err_line+=","+clab[cc]
    err_line+="\n"
    
    for rr in range(nrow):
        err_line+=rlab[rr]
        err_this_line=0.
        
        if mod_type=="square_symmetric":
            for col in arange(rr):  #show everything for which means double counting error
                if int(obLL[rr,col])!=omission_value:    
                    err_this_line+=error_components[rr,col]
            if use_diagonal:
                if int(obLL[rr,rr])!=omission_value:
                    err_this_line+=error_components[rr,rr]
            for col in arange(rr,ncol):  #show everything for which means double counting error
                if int(obLL[rr,col])!=omission_value:    
                    err_this_line+=error_components[col,rr] ### fill-in by symmetr
                   

        else:
            for col in arange(ncol):
                if int(obLL[rr,col])!=omission_value:
                    if not (rr==col  and  (not use_diagonal)):    
                        err_this_line +=error_components[rr,col]
        err_line+=",    "+str(err_this_line)+"\n"
    outf.write(err_line)    
        


             
    outf.write("TO BE DEBUGGED:  sums of column errors\n")    
    for cc in range(ncol):
        outf.write(str(sum(error_components[:cc]))+"\n")
    #DO IT for .csv below   an 2a.csv and an 2aa.csv
        #ACTUALLY it should be working but is not:  the missing data cell's errors get a 0 from numpy
    """
def full_eval_err02_FixPrintout(c,ob,re,ce,rx,cx,mod_form,d_start):
    #output to file is coming out wrong on power model, OK on i
    #because it is getting the total error right from full_eval_err02
    #just give the working routine more output.

    #print c["root"],c["mod_type"]
    #raw_input("check root")

    d_start=c["d_start"]  #bypass input 1/21/12
    nrow=c["nrow"];ncol=c["ncol"];mod_type=c["mod_type"];use_diagonal=c["use_diagonal"]
    minkowski_power=c["minkowski_power"];attenuation_power=c["attenuation_power"]
    erf=c["erf"];omission_value=c["omission_value"]

    error_component=zeros((nrow,ncol),float)	#new

    evrc=get_fitted_table_of_values(re,ce,rx,cx,attenuation_power,minkowski_power,mod_form,d_start) #rxi is a vector of length ndim, ditto for cxi

    error=0.
    if mod_type=="square_symmetric":
        if use_diagonal:
            for row in arange(nrow):
                for col in arange(row+1):
                    if int(ob[row,col])!=omission_value:    
			error_component[row,col]=erf(ob[row,col],evrc[row,col])
                        error+=error_component[row,col]
        else:
            for row in arange(nrow):
                for col in arange(row):
                    if int(ob[row,col])!=omission_value:    
                        error_component[row,col]=erf(ob[row,col],evrc[row,col])
			error+=error_component[row,col]

    else:
        if use_diagonal:
            for row in arange(nrow):
                for col in arange(ncol):
                    if int(ob[row,col])!=omission_value:   
			error_component[row,col]= erf(ob[row,col],evrc[row,col])
                        error+=error_component[row,col]
        else:            
            for row in arange(nrow):
                for col in arange(ncol):
                    if row!=col:     
                        if int(ob[row,col])!=omission_value: 
			    error_component[row,col]=	erf(ob[row,col],evrc[row,col])   
                            error+=error_component[row,col]
    return error,evrc,error_component

        """

    #spread sheet output
    interface_to_spread_sheet(c,obLL,2**(re),2**(ce),rx,cx,rlab,clab,err)

    #-------  Machine readable output --------

    write_vector_or_array(outf,nrow,ndim,rx,"row_coordinates")
    write_vector_or_array(outf,ncol,ndim,cx,"col_coordinates")
    write_vector_or_array(outf,nrow,1,2**(re),"row_multipliers")
    write_vector_or_array(outf,ncol,1,2**(ce),"col_multipliers")
    write_vector_or_array(outf,nrow,1,re,"row_effects")
    write_vector_or_array(outf,ncol,1,ce,"col_effects")

    outf.write("scale_factor_multipliers\n")  #not presently used,but in the FORTRAN
    outf.write("1 ,\n1.00 ,\n")

    outf.write("coefficients_of_polynomial_starting_at_1\n1,\n"+str(attenuation_power)+"\n")

    outf.write("error\n"+str(err)+"\n")
    #raw_input("debug at 1899, err"+str(err))
                       
    outf.write("Minkowski parameter\n1,\n1,\n"+str(minkowski_power)+"\n")
    outf.write("minkowski_power\n1,\n1,\n"+str(minkowski_power)+"\n")
    outf.write("attenuation_power\n1,\n1,\n"+str(attenuation_power)+"\n")
    outf.write("d_start\n1,\n1,\n"+str(d_start)+"\n")
    outf.write("mod_form\n1,\n1,\n"+mod_form+"\n")
    outf.write("mod_type\n1,\n1,\n"+mod_type+"\n")
    outf.write("mod_form\n1,\n1,\n"+mod_form+"\n")
    outf.write("ndim\n1,\n1,\n"+str(ndim)+"\n")
    outf.write("use_diagonal\n1,\n1,\n"+str(use_diagonal)+"\n")

                
    #-------- prepare various indices of 'centrality' for experimentation Johannes & Bruce
    
    # Want data and its row sums and column sums (used as 'rank' version of 1 centrality)
    # Want error wrt traditional null model, for inspection, and its row and col sums as 1st order centrality
    # Want error wrt fitted model, dimensional centrality, dim+1 centrality
    # For the moment I want to look at these, particularly for Johannes and Bruce Duncan's texts

    
    #ob_rsum=ob.sum(1); ob_csum=ob.sum(0); ob_sum=ob_rsum.sum()
    
    
    #err_table_wrt_rcnull=zeros((nrow,ncol),float)
    #err_table_wrt_model=zeros((nrow,ncol),float)
    err_table_wrt_rcnull=[]
    err_table_wrt_model=[]
    for row in arange(nrow):
        #print "debug hi hi hi row",row
        #Hmmm this apparently goes back to lists of lists (before numpy was available or working
        err_table_wrt_rcnull.append([0.])  # avoiding the cumulative memory eating array routines
        err_table_wrt_model.append([0.])  # avoiding the cumulative memory eating array routines
        for col in arange(ncol-1):
            err_table_wrt_rcnull[row].append(0.)  # avoiding the cumulative memory eating array routines
            err_table_wrt_model[row].append(0.)  # avoiding the cumulative memory eating array routines
    for row in arange(nrow):
        for col in arange(ncol):
            use_flag=True
            if row==col:
                if not(use_diagonal):
                    use_flag=False
            else:
                if mod_type=="square_symmetric" and col>row:
                    use_flag=False
            if use_flag:        
                null_expectation=(obLL_rsum[row]*obLL_csum[col])/float(obLL_sum)
                err_table_wrt_rcnull[row][col]=erf(obLL[row][col],null_expectation)
                #err_table_wrt_model[row][col]=erf(obLL[row][col],evLL[row][col])
                err_table_wrt_model[row][col]=error_components[row,col]
            else:
                err_table_wrt_rcnull[row][col]=0.
                err_table_wrt_model[row][col]=0.

    #working with vectors and therefore without easy sums
    err_wrt_rcnull_rsum=[]
    err_wrt_model_rsum=[]
    for row in arange(nrow):
        err_wrt_rcnull_rsum.append(0)
        err_wrt_model_rsum.append(0)
        
    err_wrt_rcnull_csum=[]
    err_wrt_model_csum=[]
    for col in arange(ncol):
        err_wrt_rcnull_csum.append(0)
        err_wrt_model_csum.append(0)

    for row in arange(nrow):
        if mod_type=="square_symmetric" and use_diagonal:
            col_span=row+1
        elif mod_type=="square_symmetric":
            col_span=row
        else:
            col_span=ncol
        for col in arange(col_span):
            enullrc=err_table_wrt_rcnull[row][col]
            #emodrc=err_table_wrt_model[row][col]
            emodrc=error_components[row,col]
            err_wrt_rcnull_rsum[row]+=enullrc
            err_wrt_model_rsum[row]+=emodrc
            err_wrt_rcnull_csum[col]+=enullrc
            err_wrt_model_csum[col]+=emodrc

                                    
    #err_wrt_rcnull_rsum=err_table_wrt_rcnull.sum(1)
    #err_wrt_rcnull_csum=err_table_wrt_rcnull.sum(0)

    #err_wrt_model_rsum=err_table_wrt_model.sum(1)
    #err_wrt_model_csum=err_table_wrt_model.sum(0)


    #--------  human & Excel readable row by row and column by column --------

    outf.write("""
Coordinates, sums, sums of errors with respect to standard row/column null model
sums of errors with respect to dimensional solution.
""")
    outf.write(coord_output1(nrow,ndim,rlab,re,rx,
                                   obLL_rsum,
                                   err_wrt_rcnull_rsum,
                                   err_wrt_model_rsum,
                                   err,mod_type) )
    
    if mod_type=="rectangular" or mod_type=="square_asymmetric":
        outf.write(coord_output1(ncol,ndim,clab,ce,cx,
                                   obLL_csum,
                                   err_wrt_rcnull_csum,
                                   err_wrt_model_csum,
                                   err,mod_type) )
    outf.write("check debugging to line 2508\n")    

    #------  Human & Excel readable Tables -----------

    outf.write("""
Output with tabs -- suitable for Excel.
Table shows observed values with:
    Coordinates,
    sums,
    sums of errors with respect to standard row/column null model
    and sums of errors with respect to dimensional solution.
\n""")
    outf.write( tab_out2(nrow,ncol,ndim,rlab,clab,re,ce,rx,cx,obLL,
            obLL_rsum,obLL_csum,
            err_wrt_rcnull_rsum,err_wrt_rcnull_csum,
            err_wrt_model_rsum,err_wrt_model_csum,
            err,mod_type,"begin observed") )

#Kludge -- it is not showing the predicted values.  Take one of the other outputs
    #impose evLL
    outf.write("""
Output with tabs -- suitable for Excel.
Table shows kludged predicted values plus stuff to be cleaned up
Plus:
    Coordinates,
    sums,
    sums of errors with respect to standard row/column null model
    and sums of errors with respect to dimensional solution.
\n""")
    #print "debug err_table_wrt_model"
    #print err_table_wrt_model
    outf.write( tab_out2(nrow,ncol,ndim,rlab,clab,re,ce,rx,cx,evLL,
            obLL_rsum,obLL_csum,
            err_wrt_rcnull_rsum,err_wrt_rcnull_csum,
            err_wrt_model_rsum,err_wrt_model_csum,
            err,mod_type,"Begin kludged predicted wrt model") )

    
    outf.write("""
Output with tabs -- suitable for Excel.
Table shows DEVIATIONS from STANDARD NULL MODEL  (NULL=(row sum)*(column sum)/total.)
Plus:
    Coordinates,
    sums,
    sums of errors with respect to standard row/column null model
    and sums of errors with respect to dimensional solution.
\n""")

    
    outf.write( tab_out2(nrow,ncol,ndim,rlab,clab,re,ce,rx,cx,err_table_wrt_rcnull,
            obLL_rsum,obLL_csum,
            err_wrt_rcnull_rsum,err_wrt_rcnull_csum,
            err_wrt_model_rsum,err_wrt_model_csum,
            err,mod_type,"begin errors compared to standard rc-null") )
    
    outf.write("""
Output with tabs -- suitable for Excel.
Table shows DEVIATIONS from FITTED MODEL.
Plus:
    Coordinates,
    sums,
    sums of errors with respect to standard row/column null model
    and sums of errors with respect to dimensional solution.
\n""")
    #print "debug err_table_wrt_model"
    #print err_table_wrt_model
    outf.write( tab_out2(nrow,ncol,ndim,rlab,clab,re,ce,rx,cx,err_table_wrt_model,
            obLL_rsum,obLL_csum,
            err_wrt_rcnull_rsum,err_wrt_rcnull_csum,
            err_wrt_model_rsum,err_wrt_model_csum,
            err,mod_type,"Begin Errors wrt model") )



    
    
    outf.close()
     
def write_vector_or_array(outf,nrow,ndim,rx,message):
    eol="\n"
    outf.write(str(message)+eol)
    outf.write(str(nrow)+eol)
    outf.write(str(ndim)+eol)
    for row in arange(nrow):
        #print "ndim",ndim,type(ndim)    
        try:
            for dim in arange(ndim):
                outf.write(str(rx[row,dim])+","+eol)
        except:
            for dim in arange(ndim):
                outf.write(str(rx[row])+","+eol)


def tab_out2(nrow,ncol,ndim,rlab,clab,re,ce,rx,cx,obLL,
            obLL_rsum,obLL_csum,
            err_wrt_rcnull_rsum,err_wrt_rcnull_csum,
            err_wrt_model_rsum,err_wrt_model_csum,
            err,mod_type,sum_label):
    line=""
    line+=sum_label+"\n"
    #Column labels
    for col in arange(ncol):
        line+="\t%s "%(clab[col][:5])
    for dim in arange(ndim):
        line+="\t    "
    line+="\t    \t        Err  \tErr\tName\n"
    
    for col in arange(ncol):
            line+="\t%s "%(clab[col][5:10])
    
    for dim in arange(ndim):
        line+="\t  Dim"+str(dim)+"        "
            
    line+="\t    Sum"
    line+="\t    to null "
    line+="\t    to model"
    line+="\t  Name"    
    line+="\n"
    #rows    
    for row in arange(nrow):            
        for col in arange(ncol):
            #print "debugging aab row,col,type of obLL",row,col,obLL[row][col],type(obLL[row][col])
            #print obLL[row][col],type(   obLL[row][col]) 
            line+="\t%6.1f"%(obLL[row][col]) 
        for dim in arange(ndim):    
            line+="\t%8.3f"%rx[row,dim]
        line+="\t%8.3f"%(obLL_rsum[row])    
        line+="\t%8.3f"%(err_wrt_rcnull_rsum[row])    
        line+="\t%8.3f"%(err_wrt_model_rsum[row])
        line+="\t"+rlab[row]
        line+="\n"
    #column coefficients    
    for dim in arange(ndim):
        for col in arange(ncol):
            line+="\t%8.3f"%cx[col,dim]
        line+="\n"
    for col in arange(ncol):
        line+="\t%8.3f"%obLL_csum[col]
    line+="\n"
    for col in arange(ncol):
        line+="\t%8.3f"%err_wrt_rcnull_csum[col]
    line+="\n"
    for col in arange(ncol):
        line+="\t%8.3f"%err_wrt_model_csum[col]
    line+="\n"
    for col in arange(ncol):
        line+="\t%s"%clab[col]
    line+="\n"
    
    
    line+="\n\n"    
    return line


def coord_output1(nrow,ndim,rlab,re,rx,
                  obLL_rsum,
                  err_wrt_rcnull_rsum,
                  err_wrt_model_rsum,
                  err,mod_type):    
    line= " error="+str(err)+"\n"
 
    #two-line labels:       
    line= "\n                          "
    for d in arange(ndim):
        line+="        "
    line+="               Err      Err"
    line+="\n Item (   Mult ) log2(Mult)"
    for d in arange(ndim):
        line+="  Dim %1i "%(d)
    line+="     R Sum "
    line+="   to null "
    line+=" to model"
    line+="  Name"    
    line += "\n"
    
    for row in arange(nrow):
        line += "%5i "%(row+1)              #number, from 1
        line += "(%8.3f)"%(2**(re[row]))  #row multiplier
        line += " %8.3f "%(re[row])       #row effect
        for d in arange(ndim):
            line += "%8.3f"%(rx[row,d])     #coordinates
            
        line += "  "

        line += "%10.3f"%(obLL_rsum[row])      #rank (sum)
        #print type(err_wrt_rcnull_rsum[row]),err_wrt_rcnull_rsum[row]
        line += "%10.3f"%(err_wrt_rcnull_rsum[row])  #err wrt traditional null:  first order centrality
        line += "%10.3f  "%(err_wrt_model_rsum[row])    #err wrt model:  dimensional centrality
        
        line += rlab[row]+"\n"        #label

    return line

##                    
##def read_param_file(fname):
##    inf=open(fname,"r")
##    lines=inf.readlines()
##    inf.close()
##    try:
##        tag="row_coordinates"        
##        rx=read_array_from_tag(tag,lines)
##        tag="col_coordinates"
##        cx=read_array_from_tag(tag,lines)
##        tag="row_effects"
##        re=read_vector_from_tag(tag,lines)
##        tag="col_effects"
##        ce=read_vector_from_tag(tag,lines)
##        tag="minkowski_power"
##        minkowski_power=read_constant_from_tag(tag,lines)
##        tag="attenuation_power"
##        attenuation_power=read_constant_from_tag(tag,lines)
##    except:
##        raw_input("Unable to read file")
##        
##
##    return re,ce,rx,cx,minkowski_power,attenuation_power
##    

def read_array_from_tag(tag,lines):
    found=False
    for i in range(len(lines)):
        if tag in lines[i]:
            found=True
            j=i
            j+=1
            
            nrow=int(lines[j])
            j+=1

            ndim=int(lines[j])
            j+=1

            rx=zeros((nrow,ndim),float)
            for row in range(nrow):
                for dim in range(ndim):
                    s=lines[j].strip()
                    if "," in s:  s=s[0:len(s)-1]
                    rx[row,dim]=float(s)
                    j+=1
            break
    if not found:  print "error, tag ",tag,"not found"
    return rx

def read_vector_from_tag(tag,lines):
    found=False
    for i in range(len(lines)):
        if tag in lines[i]:
            found=True
            j=i
            j+=1
            
            nrow=int(lines[j])
            j+=1

            ndim=int(lines[j])
            j+=1

            re=zeros((nrow),float)
            for row in range(nrow):
                s=lines[j].strip()
                if "," in s:  s=s[0:len(s)-1]
                re[row]=float(s)
                j+=1
            break
    if not found:  print "error, tag ",tag,"not found"
    return re

def read_non_array_float_constant_from_tag(tag,lines):
    found=False
    for i in range(len(lines)):
        if tag in lines[i]:
            found=True
            j=i+0
            j+=1
            s=lines[j].strip()
            if "," in s:  s=s[0:len(s)-1]
            constant=float(s)
            break  #break the loop.  Do not search further.
    if not found:  print "error, tag ",tag,"not found in 'read_non_array_float_constant_from_tag'"
    return constant
            

def read_constant_from_tag(tag,lines):
    found=False
    for i in range(len(lines)):
        if tag in lines[i]:
            found=True
            #print "line 2687, found tag ",tag
            j=i+0
            j+=1

            s=lines[j].strip()
            #print "2692, lines[j] & s:  ",lines[j], s
            if "," in s:  s=s[0:len(s)-1]
            nrow=int(s)
            j+=1

            s=lines[j].strip()
            if "," in s:  s=s[0:len(s)-1]
            ndim=int(s)
            j+=1

            rx=zeros((nrow,ndim),float)
            s=lines[j].strip()
            if "," in s:  s=s[0:len(s)-1]
            c=float(s)
            break
    if not found:  print "error, tag ",tag,"not found"
    return c

def read_string_from_tag(tag,lines):
    found=False
    for i in range(len(lines)):
        if tag in lines[i]:
            found=True
            j=i
            j+=1

            s=lines[j].strip()
            if "," in s:  s=s[0:len(s)-1]
            nrow=int(s)
            j+=1

            s=lines[j].strip()
            if "," in s:  s=s[0:len(s)-1]
            ndim=int(s)
            j+=1

            rx=zeros((nrow,ndim),float)
            s=lines[j].strip()
            if "," in s:  s=s[0:len(s)-1]
            c=str(s)
            break
    if not found:  print "error, tag ",tag,"not found"
    return c

                        

           
def small_show(c,nrow,ncol,obLL,rlab,clab,re,ce,rx,cx):
    #small display of observed and expected.  Useful during runs to judge fit directly (visually)
    #for row in arange(min(nrow,5)):  #Don't want too much on the screen, like 1700 rows.  Do same for columns

    #Decide how many:
    if nrow<=12:
        row_show=range(nrow)
        row_split=-99           
    else:
        row_show=range(5)+range(nrow-5,nrow)
        row_split=nrow-5

    if ncol<=12:
        col_show=range(ncol)
        col_split=-99
    else:
        col_show=range(5)+range(ncol-5,ncol)
        col_split=ncol-5
        
    #and show them
    line=" "*15 #prepare for abbreviated column labels
    max_label_length=0
    for col in col_show:
        line+="%-15s"%clab[col][0:7]
        if len(clab[col].strip())>max_label_length:  max_label_length=len(clab[col].strip())
    line+="\n"           
    if max_label_length>7:
        for col in col_show:
            line+="%-15s"%clab[col][7:14]
    line+="\n"           
        
    for row in row_show:  
        if row==row_split:
            line="...\n\n"
        else:
            line=""      
        line+="%-15s"%rlab[row][0:15]
            
        for col in col_show:
            #if col==col_show:  line+=" ... "
            if col==col_split:  line+=" ... "
            line+="%8.1f"%(obLL[row][col])
        print line
        line="               "
        for col in col_show:
            if col==col_split:  line+=" ... "
              #def get_fitted_value(rei,cej,rxi,cxj,attenuation_power,minkowski_power): #rxi is a vector of length ndim, ditto for cxi
            #evrc=get_fitted_value2(re[row],ce[col],rx[row,:],cx[col,:],attenuation_power,minkowski_power)
            evrc=get_fitted_value(re[row],ce[col],rx[row,:],cx[col,:],c["attenuation_power"],
                                  c["minkowski_power"],c["mod_form"],c["d_start"])
            line+="%8.1f"%(evrc)
        print line
        print
    print
                       

def read_array_from_tag(tag,lines):
    found=False
    for i in range(len(lines)):
        if tag in lines[i]:
            found=True
            j=i
            j+=1
            
            nrow=int(lines[j])
            j+=1

            ndim=int(lines[j])
            j+=1

            rx=zeros((nrow,ndim),float)
            for row in range(nrow):
                for dim in range(ndim):
                    s=lines[j].strip()
                    if "," in s:  s=s[0:len(s)-1]
                    rx[row,dim]=float(s)
                    j+=1
            break
    if not found:  print "error, tag ",tag,"not found"
    return rx                    
def read_vector_from_tag(tag,lines):    
    found=False
    for i in range(len(lines)):
        if tag in lines[i]:
            found=True
            j=i
            j+=1
            
            nrow=int(lines[j])
            j+=1

            ndim=int(lines[j])
            j+=1

            re=zeros((nrow),float)
            for row in range(nrow):
                s=lines[j].strip()
                if "," in s:  s=s[0:len(s)-1]
                re[row]=float(s)
                j+=1
            break
    if not found:  print "error, tag ",tag,"not found"
    return re

                    
def read_param_file02(c,fname):
    """
    outf.write("mod_form\n1,\n1,\n"+mod_form+"\n")
    outf.write("mod_type\n1,\n1,\n"+mod_type"\n")
    outf.write("mod_form\n1,\n1,\n"+mod_form+"\n")
    outf.write("ndim\n1,\n1,\n"+str(ndim)+"\n")
    outf.write("use_diagonal\n1,\n1,\n"+str(use_diagonal)+"\n")

"""
    inf=open(fname,"r")
    lines=inf.readlines()
    inf.close()
    pause_to_check_continuation=False
    if 1==1: #try:
        tag="row_coordinates"        
        rx=read_array_from_tag(tag,lines)
        print "row_coodinates read"
        tag="col_coordinates"
        cx=read_array_from_tag(tag,lines)
        print "col_coordinates read"
        tag="row_effects"
        re=read_vector_from_tag(tag,lines)
        print "re (row effects = log2 of row multipliers read"
        tag="col_effects"
        ce=read_vector_from_tag(tag,lines)
        print "ce (col effects = log2 of col multipliers) read."
        
        tag="minkowski_power"
        try:    
            minkowski_power=read_constant_from_tag(tag,lines)
            print "minkowski_power read",minkowski_power
        except:
            minkowski_power=c["minkowski_power"]
            print "minkowski_power not retrieved."
            pause_to_check_continuation=True            
            
        tag="attenuation_power"
        try:
            attenuation_power=read_constant_from_tag(tag,lines)
            print "attenuation_power read",attenuation_power
        except:
            attenuation_power=c["attenuation_power"]
            print "attenuation_power not retrieved."
            pause_to_check_continuation=True            
            
        tag="error"
        #Note originally I filed even single numbers as arrays (for simplicity).
        #Somewhere I forgot, so error is just a single floating point number
        try:
            error=read_non_array_float_constant_from_tag(tag,lines)
            print "error has been read, error=",error
        except:
            print "old error not retrieved."
            pause_to_check_continuation=True            
            
        tag="d_start"
        try:
            print "2938",read_constant_from_tag(tag,lines)
            d_start=read_constant_from_tag(tag,lines)
            print "d_start read",d_start
        except:
            d_start=c["d_start"]
            print "d_start not retrieved."
            pause_to_check_continuation=True
            raw_input("2945 trouble retrieving d_start")
            
        tag="mod_form"
        try:
            mod_form=read_string_from_tag(tag,lines)
            print "mod_form read",mod_form
        except:
            mod_form=c["mod_form"]
            print "mod_form not retrieved."
            pause_to_check_continuation=True            
            
        tag="mod_type"
        try:
            mod_type=read_string_from_tag(tag,lines)
            print "mod_type read", mod_type
        except:
            mod_type=c["mod_type"]
            print "mod_type not retrieved."
            pause_to_check_continuation=True            
            
        tag="use_diagonal"
        try:
            use_diagonal=read_string_from_tag(tag,lines)
            print "mod_type read", mod_type
        except:
            use_diagonal=c["use_diagonal"]
            print "use_diagonal not retrieved."
            pause_to_check_continuation=True            

        ndim=shape(rx)[1]  #ndim as number of columns in array rx
        print "ndim computed",ndim
        
    #except:
    #    raw_input("Unable to read file")
        
    if pause_to_check_continuation:
        raw_input("check comments above regarding retrieval and continuation from file.  Press anything to continue.")    
    stored_parameters={}
    stored_parameters["re"]=re
    stored_parameters["ce"]=ce
    stored_parameters["rx"]=rx
    stored_parameters["cx"]=cx
    stored_parameters["minkowski_power"]=minkowski_power
    stored_parameters["attenuation_power"]=attenuation_power
    stored_parameters["error"]=error
    stored_parameters["d_start"]=d_start
    stored_parameters["mod_form"]=mod_form
    stored_parameters["mod_type"]=mod_type
    stored_parameters["use_diagonal"]=use_diagonal
    stored_parameters["ndim"]=ndim

    #return re,ce,rx,cx,minkowski_power,attenuation_power,error,d_start,mod_form,mod_type,ndim,use_diagonal
    return stored_parameters

def drive_gram_schmidt(c,nrow,ncol,ndim,rx,cx):
    for dim in arange(ndim):
        rm=sum(rx[0:,dim])/float(nrow)
        rx[0:,dim]-=rm
        junk,rxs=gram_schmidt(nrow,ndim,rx)
        rx=rxs; del rxs,rm
        if c["mod_type"]=="rectangular":
            for dim in arange(ndim):
                cm=sum(cx[0:,dim])/float(ncol)
                cx[0:,dim]-=cm
                junk,cxs=gram_schmidt(ncol,ndim,cx)
                cx=cxs; del cxs,cm
    return rx,cx                

   
def do_passes(self,npass_original,
              c,rlab,clab,obLL,obLL_rsum,obLL_csum,obLL_total,
              re_original,ce_original,rx_original,cx_original,
              n_passes_in_opt,note,best_err):

    mod_form=c["mod_form"]
    d_start=float(c["d_start"])
        
    npass=npass_original+0.    
    re=re_original[:];ce=ce_original[:];rx=rx_original[:,:];cx=cx_original[:,:]    
    pass_re=re; pass_ce=ce
    pass_rx=rx; pass_cx=cx


    
##    k=c.keys()
##    k.sort()
##    for ki in k:
##            print ki,c[ki]
##    raw_input("")        
  
    # I am getting errors that have nothing logical to do with changes.  Guess at
    # illogical storage.  Call the entries here  ...original.  Work with copies
    # return copies

    max_pass=c["max_pass"] #10000  #a pass is one cycle inside opt.  Opt itself calls for multiple passes
    #raw_input("max_pass"+str(max_pass))
    #gram-schmidtt orthogonalizations, if any, are done after one pass through opt.
    #opt itself resets the step parameters so that they themselves do not get trapped in a local minimimum
    #for k in c:
    #        print k,c[k]
    #print
    pid_list=[]

##   #seems to duplicate stuff near top of opt.
##    nr=size(rx,0) #;nc=size(cx,0)
##    for ii in xrange(nr):
##        rx[ii,0]=round(rx[ii,0],2)
##        re[ii]=round(re[ii],2)            
    #rx[:,0]=round(rx[:,0],1);cx[:,0]=round(cx[:,0],1);re=round(re,1);ce=round(ce,1)

    #debug
    #errx=full_eval_err02(c,obLL,re,ce,rx,cx,mod_form,d_start)
    #print "\nNew Starting error:  ",comma_form(errx)
    #raw_input("debugging for CA too large at 2637")


    while npass<max_pass: #int(c['max_passes_for_run']): #max_pass:
        #print "3046  use_stand=",c["use_stand"]
        #raw_input("3047")
        if c["use_stand"]:
            res,ces,rxs,cxs=standardize_parameters(re,ce,rx,cx,c["mod_type"],c["minkowski_power"])
            re=res;ce=ces;rx=rxs;cx=cxs;del res,ces,rxs,cxs

            

        if c["mod_type"]=="square_symmetric":
            ce[:]=re[:];rx[:,:]=cx[:,:]  #make sure it knows these are the same object in each case
 
        if c["mod_type"]=="square_asymmetric":
            rx[:,:]=cx[:,:]

        err1=full_eval_err02(c,obLL,re,ce,rx,cx,mod_form,d_start)


        #n_passes_in_opt=32 #32 (3 for speed during debugging)
        # below:  There is an optx (it examines powers)
        #Take a look (graph):
        #Graphics Set up for running when I've already got an array (bypassing a file)
        #import rectangle_driver006inprocess
        c['pause_between_drawings']=True

##        raw_input( "ready to fork")
##        #Trying to close the graphics, Tk window inorder to reopen it
##        for p in pid_list:
##                print "killing  pid",p
##                os.kill(p,signal.SIGKILL)
##        newpid=os.fork()
##        if newpid==0: #child
##                rectangle_driver006inprocess.rectangle_driver_setup_mat006(c['nrow'],c['ncol'],c['ndim'],rx,cx,
##                        obLL,rlab,clab,"temp_file",c)
##                tk().quit()
##        else:  #parent
##                pid_list.append(newpid)
##                raw_input("continuing main program")
        #print "debug circa 2030", size(rx,0),size(rx,1),size(cx,0),size(cx,1)
        #raw_input("")


        
        npass,re,ce,rx,cx=opt(self,npass,c,obLL,re,ce,rx,cx,rlab,clab,n_passes_in_opt,note,best_err)  #it does not update this without return (though it updates everything else)
        d_start=c["d_start"] #kludge
        print "3104 d_start=",d_start,"c version:",c["d_start"]
        err=full_eval_err02(c,obLL,re,ce,rx,cx,mod_form,d_start)
        print "debug at 3098: err=",err," err1=",err1," best_of_scanned=",c["best_of_scanned"]
        #raw_input("3099")
        if err<err1:
                err1=err
                pass_re=re; pass_ce=ce;
                pass_rx=rx; pass_cx=cx
                outstuff1(c,pass_re,pass_ce,pass_rx,pass_cx,rlab,clab,obLL,obLL_rsum,obLL_csum,obLL_total)
                if err<c["best_of_scanned"]:
                        outstuff1(c,pass_re,pass_ce,pass_rx,pass_cx,rlab,clab,obLL,obLL_rsum,obLL_csum,obLL_total,best_of_scanned=True)
                        
                small_show(c,c["nrow"],c["ncol"],obLL,rlab,clab,re,ce,rx,cx)

##                print "debugging at 2813:"
##                c_keys=c.keys()
##                c_keys.sort()
##                for ck in c_keys:
##                        print
##                        print ck,"\t",c[ck]
##                raw_input("2819")
##                #sst=interface_to_spread_sheet(c,obLL,2**re,2**ce,rx,cx,rlab,clab,err)                                 
        if err1<best_err:
                best_err=err1
    #raw_input("debug at 2557, leaving do_passes "+str(err1)  )          
    return npass,pass_re,pass_ce,pass_rx,pass_cx

        
def connected():
    print "connected"
    
#def check_and_read_face_list_of_lists(c):
def check_and_read_face_array(c):
    #print "*"*40
    #qraw_input("******")
    try:    
        #nrow,ncol,obLL,rlab,clab=read_face_list_of_lists(c["root"])
        nrow,ncol,ob,rlab,clab=read_face_array(c["root"])
    except:
        print
        print "CHECK c above that raised exception"

        print "c['root']"
        print c
        print "error reading file "+c["root"]
        print "opening whereami to test directory"
        print "length of root=",len(c["root"])
        tt=open("WhereAmI","w")
        tt.write("Written by dwv when it has trouble locating a file.\n")
        tt.write("This may help.  If the program was looking in the wrong\n")
        tt.write("then whatever directory you found this in is the directory\n")
        tt.write("it looked in.\n")
        tt.write(time.ctime()+"\n")
                 
        tt.close()
        nrow,ncol,obLL,rlab,clab=read_face_list_of_lists(c["root"])
        
    lines=""    
    #check consistency
    ok=True
    if "nrow" in c:  #if nrow specified in template, check.  Otherwise use what was found
        if nrow!=int(c["nrow"]):
            print "Inconsistency at 3172:"    
            print "nrow"
            print nrow,type(nrow)
            print "c['nrow']"
            print c["nrow"],type(c["nrow"])
            lines+="Inconsistency:  template nrow = "+c["nrow"]+"\n"
            lines+="                file shows nrow = "+str(nrow)+"\n"
            lines+="Please stop program and edit one or the other, or \n"
            lines+="change the choice of data files (the 'root')\n\n"
            ok=False
            raw_input("check nrow")
    else:
        c["nrow"]=nrow
        ok=True

    if "ncol" in c: #if nrow specified in template, check.  Otherwise use what was found   
        if ncol!=int(c["ncol"]):
            lines+="Inconsistency:  template ncol = "+str(c["ncol"])+"\n"
            lines+="ncol is "+str(ncol)
            lines+="                file shows ncol = "+str(ncol)+"\n"
            lines+="Please stop program and edit one or the other, or \n"
            lines+="change the choice of data files (the 'root')\n\n"
            ok=False
            print lines
            raw_input("check ncol")
    else:
        c["ncol"]=ncol
        ok=True
    return nrow,ncol,ob,rlab,clab,ok,lines   

def set_commands():
    #Used to check holding random number constant
    #random.seed(3)
    #print "random 10,100:",random.uniform(10,11)
    #print raw_input("2nd random")

    #run_choice=3
    #run_choice=9  #test used for changing file output
    run_choice=9        

    c={} #controls
    #default values of some controls
    c["attenuation_power"]=1.5    #even for Kolb's 3x3, attenuation power 1 noticeably better than 2, by about 10%
    c["minkowski_power"]=1.8
    c["use_stand"]=True
    c["use_diagonal"]=True
    c["nlayer"]=1  #for now
    c["erf"]=chi_square
    c["continuation_or_startup"]="startup"
    c["min_percent_change_per_32_iterations"]=1 #1 for debugging .0001
    c["max_passes_for_run"]=1000 #1000 for debugging 10000
            
    if run_choice==1:
        root = "UseNamCC"; mod_type="square_symmetric";ndim=2
    elif run_choice==2:    
        root = "Glass7x7.txt";mod_type="square_asymmetric"
        ndim=1
    elif run_choice==3:
        root = "price_table"
        mod_type="rectangular"
        ###root = "SP1005Yrs";mod_type="rectangular"
        #minkowski_power=2.1; attenuation_power=1.8  #about 26.85
        #minkowski_power=2.5; attenuation_power=2.5  #21.86  19.93
        root="price_tableSP1005YRB"
        #minkowski_power=2.5; attenuation_power=2.5  #135
        #minkowski_power=2.5; attenuation_power=2.0  #149 few
        #minkowski_power=2.5; attenuation_power=3.0  #152 few
        #minkowski_power=2.1; attenuation_power=2.5  #138 few
        #minkowski_power=2.7 ; attenuation_power=2.5  #137 few
        #minkowski_power=1.8 ; attenuation_power=2.5  #137 few
        #minkowski_power=2.1 ; attenuation_power=1.7  #128 few
        #minkowski_power=2.1 ; attenuation_power=1.5  #181 few
        #minkowski_power=2.0 ; attenuation_power=1.7  #205 few
        minkowski_power=2.2 ; attenuation_power=1.7; use_stand=True  #97.903 #14272
        minkowski_power=2.2 ; attenuation_power=2; use_stand=True  #103.2695 at 12226
        minkowski_power=2.2 ; attenuation_power=1.5; use_stand=True  #103.5745 #11047

        ndim=2
    elif run_choice==4:
        root = "SevenH1";mod_type="rectangular"
        ndim=2
    elif run_choice==5:
        root = "SevenH1";mod_type="rectangular"
        minkowski_power=1;attenuation_power=2
        ndim=2
    elif run_choice==6:  #Netflix
        c["root"] = "f100x100"; c["mod_type"]="square_symmetric"
        c["ndim"]=2
        #minkowski_power=2; attenuation_power=2
        #about 107406
        #minkowski_power=2; attenuation_power=1.5
        #about  85557
        #minkowski_power=2; attenuation_power=1.0
        #about  54500
        #minkowski_power=1.5; attenuation_power=1.0
        #about  55950
        #minkowski_power=3; attenuation_power=1.0
        #about 222335
        #minkowski_power=1.1; attenuation_power=1.0
        #about  56235
        #minkowski_power=2; attenuation_power=.8 
        #about  41055
        #minkowski_power=1.75; attenuation_power=.8 
        #about  41669
        #minkowski_power=2.1; attenuation_power=.8 
        #about  39650
        #minkowski_power=2.1; attenuation_power=.7 
        #about  33280
        #minkowski_power=2.1; attenuation_power=.6
        #about  27000
        c[minkowski_power]=2.1; c[attenuation_power]=.4
        #about  16188
        ## Probably an error:  It is using the diagonal and these
        ## great a strong peak at distance 0.
        #minkowski_power=2.1; attenuation_power=.4; use_diagonal=False
        # that 16188 was after half an hour.  Now, after about 5 minutes 12,761.  Just to check I'd like
        # less than half the 16188
        # looks stuck at 11244 and a very different map.  This one is dense in  4 corners.  The old one
        # was distributed smoothly.  Try without standardization.
        #use_stand=False
        #That did it:  Now down below 7800 and dropping in only 26 steps.  So, I'm doing too much standardizing
        c[use_stand]=True
        #No.  I eliminated it for 32 runs of opt.  It behaves beautifully.  But when it does standardize
        # it does not recover.  So try more frequently
        # Tried sgtand after each set.  Still can't recover
        c[use_stand]=False
        # Ah I should turn off across diagonal stuff in eval of row or column of symmetrical table --
        # it leaves off cells.  That would be OK for a full evaluation, not for a partial one/
        #  But something is still driving the return to opt off track, even with the standardization off.  
        c[use_stand]=True
        # two days and nights lost to error in logic for use of diagonal -- looking for the wrong thing
        #minkowski_power=2.1; attenuation_power=.4
        #@31  6594
        #minkowski_power=2.1; attenuation_power=.7; use_diagonal=False
        #@31  5682
        #minkowski_power=2.1; attenuation_power=1.0; use_diagonal=False
        #@31  5206
        #minkowski_power=2.1; attenuation_power=2.; use_diagonal=False
        #@31  5290
        #minkowski_power=2.1; attenuation_power=1.5; use_diagonal=False
        #@31  5368  unlikely
        #minkowski_power=1.5; attenuation_power=1.0; use_diagonal=False
        #@31  5861
        #minkowski_power=2.5; attenuation_power=1.0; use_diagonal=False
        #@31  5302
        #minkowski_power=2.0; attenuation_power=1.0; use_diagonal=False
        #@31  5391  @272 5054
        #minkowski_power=2.0; attenuation_power=2.0; use_diagonal=False
        #@31  5184  @149 5136 steady
        #minkowski_power=2.0; attenuation_power=1.5; use_diagonal=False
        #@31  5144  @104 5071 
        #minkowski_power=1.8; attenuation_power=1.5; use_diagonal=False
        #@31  5305  @104 5083 
        #minkowski_power=2.2; attenuation_power=1.5; use_diagonal=False
        #@31  5139
        #minkowski_power=2.4; attenuation_power=1.5; use_diagonal=False
        #@31  5247
        c["minkowski_power"]=2.2; c["attenuation_power"]=1.5;
        c["use_diagonal"]=False
        #@31  5242  @256  5065  @1175 5060.1985
        
    elif run_choice==7:
        c["root"] = "SevenH1test";c["mod_type"]="rectangular"  #use for getting parameters printed to file
        c["minkowski_power"]=1;c["attenuation_power"]=2
        c["ndim"]=2
        c["continuation_or_startup"]="continuation"
    elif run_choice==9:
        c["root"] = "SevenH2.txt";c["mod_type"]="rectangular"  #use for getting parameters printed to file
        c["minkowski_power"]=1;c["attenuation_power"]=2
        c["ndim"]=2
        c["continuation_or_startup"]="startup"
        
    elif run_choice==71:
        c["root"] = "SevenH1test10";c["mod_type"]="rectangular"  #use for getting parameters printed to file
        c["minkowski_power"]=1;c["attenuation_power"]=2
        c["ndim"]=2
        c["continuation_or_startup"]="startup"
    elif run_choice==8:
        c["root"] = "Gregg1";c["mod_type"]="rectangular"  #use for getting parameters printed to file
        c["minkowski_power"]=1;c["attenuation_power"]=2
        c["ndim"]=2
        c["continuation_or_startup"]="startup"


        
        root="Gregg1"; mod_type="rectangular"
        minkowski_power=1; attenuation_power=2.5
        ndim=2
        
        
    else:
        print "data_set not specified.  Please stop, type it directly into code **here**, and run again"
        print "Enter code comparable to what you see in the 'elif' examples above this line in the code."


        raw_input("stop")

    # set up is complete.  Now run it
    return c
        
            
def dwv_main(self,c): #had it been written in anticipation -- this would be 'main'
    mod_form=c["mod_form"]
    d_start=c["d_start"]
    #opt_minkowski=c["opt_minkowski"]
    #opt_attenuation=c["opt_attenuation"]
    #some clean-up
    if c["mod_type"]=='rectangular' and c["use_diagonal"]==False:
            print "\nYour setup specified"
            print "    rectangular model"
            print "and it specified"
            print "    use_diagonal=False"
            print "\nThe rectangular table does not have a diagonal."
            print "Please correct your setup file."
            print "-- The program is changing the setup to"
            print "    c['use_diagonal']=True "
            print "If you really do not want to use these cells"
            print "use the omission value."
            raw_input(" -- Press any key to continue --")
    #more clean-up        
    if c["mod_form"].upper() in ["C","CAUCHY","CAUCHY_FORM"]:
            print "mod_form  ",c["mod_form"],type(c["mod_form"])
            print "d_start   ",c["d_start"],type(c["d_start"])
            print "opt_d_start",c["opt_d_start"],type(c["opt_d_start"])
            #raw_input("3222")
            if c["d_start"]!=0 or c["opt_d_start"]:
                    print "Your controls elect Cauchy (not 'started_Cauchy')"
                    print "but you are either using a non-zero 'd_start'"
                    print "or allowing the program to optimize d_start"
                    print "This is inconsistent.  The program will set"
                    print "d_start to 0 and it will not be allowed to "
                    print "optimize d_start."
                    print "If you want to use d_start, then change the"
                    print "SETUP file to mod_form started_cauchy"
                    raw_input("Press any key to continue.")
                    c["d_start"]=0
                    c["opt_d_start"]=False
    #random.seed(3)
    #nrow,ncol,obLL,rlab,clab,ok,lines=check_and_read_face_list_of_lists(c)
    nrow,ncol,ob,rlab,clab,ok,lines=check_and_read_face_array(c)
    c["rlab"]=rlab
    c["clab"]=clab
    if c['erf']=="chi_square":
        c['erf']=chi_square  #could not do this in the GUI where chi_square was not yet defined (actually, it was def by inclusion)
    else:
        print "\a\a\a UNDEFINED error function received from script"
    #print "debug top of dwv_main, trying to print to text_window"
    #self.print_text_window("top of dwv_main, debugging",self.text_window)
    #sleep(10)
    #restore check on nrow & ncol in file as compared to values from the
    #template (that have been passed with c -- if there is a GUI to pass
    #them by inserting them into c.
        
    #obLL_rsum,obLL_csum,obLL_total=list_sums(nrow,ncol,ob)  #needed for output.  Compute here; compute only once.
    ob_rsum=sum(ob,1); ob_csum=sum(ob,0); ob_total=sum(ob_csum)                             
    

#Make the semi-starts do what the ordinary stuff does wrt using or not
    #using orthogonalization.

    #pack these things into procedures.  Pass them things like
    #'print_text_window' that allows them to communicate to the
    #GUI.  Use things that trigger events in the GUI (that in
    #turn can initiate graphics and whatever.
    #Use the 'if __main__!= "__main__:'  gizzmo so that, when
    #it is run free-standing it does not try to communicate with
    #something that is not there.  I want as few things as possible
    #to be duplicated (but with variants) in what were separate
    #programs.
    #output of coordinates and other parameters will be through files
    #that the stand alone dwv wrote and will continue to write 

    #graft the free-standing program with the buttons of the GUI (not with the template but the button on the GUI)
    do_startup=False
    try:
        if c["continuation_or_startup"]=="startup" or self.continuation_or_startup_flat=="startup":
            do_startup=True
    except:
        if c["continuation_or_startup"]=="continuation":
            do_startup=False
    #raw_input(do_startup)
        
    #if c["continuation_or_startup"]=="startup":

    note=""    
    if do_startup:
        #reset the button
        try:
            self.v3.select()
        except:
            pass


        if 'n_semi_starts' in c:
            n_semi_starts=c['n_semi_starts']
        else:    
            n_semi_starts=10 #5 #5 #10 #20 #3 #10
        various_startups=[]
        half_of_semi_start=128 #32 #16
        c['inside_a_semi-start']=False
        
        
        best_err=1.e100
        
        for nss in range(n_semi_starts):
##            if nss<2:
##                half_of_semi_start=128
##            else:
##                half_of_semi_start=32
            c['inside_a_semi-start']=True    
                

            line="\nSemi_start #"+str(nss+1)+"\n"
            #raw_input(line)
            #time.sleep(5)
            try:
                self.print_text_window(line+"\n",self.text_window)
            except:
                print line
                #self.print_text_window(line+"\n",self.text_window)
 

            print "Trial startup #"+str(nss+1)+ "starting without orthogonalization"
            re,ce,rx,cx=start_dwv_from_ob(ob,c)
            
            #Over-ride for first and second tries:
            if nss==0:
                nrow=c['nrow']
                half=nrow/2.
                rx[0,0]=-.5
                hstep=1./nrow
                for ii in range(1,nrow):
                    rx[ii,0]=rx[ii-1,0]+hstep
                cx[0,0]=-.5    
                hstep=1./ncol
                for ii in range(1,ncol):
                    cx[ii,0]=cx[ii-1,0]+hstep
                err0=full_eval_err02(c,ob,re,ce,rx,cx,mod_form,d_start)
                #raw_input("3019 err0 "+str(err0))
                hstep=1.1
                #print "rx",rx
                #print "cx",cx
                #raw_input("3024")
                 
                rx*=hstep
                cx*=hstep
                err_right=full_eval_err02(c,ob,re,ce,rx,cx,mod_form,d_start)
                if err_right<err0:
                    #raw_input("3023 right "+str(err_right))
                    while err_right<err0:
                        #print "Expanding ",err_right   
                        err0=err_right    
                        rx*=hstep
                        cx*=hstep
                        err_right=full_eval_err02(c,ob,re,ce,rx,cx,mod_form,d_start)
                        #print "right ",err_right
                    rx/=hstep
                    cx/=hstep
                    #raw_input("3030 right "+str(err0))
                else:
                   rx/=2*hstep
                   cx/=2*hstep
                   err_left=full_eval_err02(c,ob,re,ce,rx,cx,mod_form,d_start)
                   if err_left<err0:
                        #print "Contracting " ,err_left   
                        rx/=hstep
                        cx/=hstep                        
                        err_left=full_eval_err02(c,ob,re,ce,rx,cx,mod_form,d_start)
                        while err_left<err0:
                            err0=err_left    
                            rx/=hstep
                            cx/=hstep
                            err_left=full_eval_err02(c,ob,re,ce,rx,cx,mod_form,d_start)
                        #raw_input("3042 "+str(err_left))
                   rx*=hstep
                   cx*=hstep
                        
            if nss==1:
                nrow=c['nrow']
                half=nrow/2.
                rx[0,0]=-.5
                hstep=1./nrow
                for ii in range(1,nrow):
                    rx[ii,0]=rx[ii-1,0]+hstep
                cx[0,0]=.5    
                hstep=1./ncol
                for ii in range(1,ncol):
                    cx[ii,0]=cx[ii-1,0]-hstep  #try reversing the sign
                err0=full_eval_err02(c,ob,re,ce,rx,cx,mod_form,d_start)
                #print "rx",rx
                #print "cx",cx
                #raw_input("3069")
                
                
                hstep=1.1
                rx*=hstep
                cx*=hstep
                err_right=full_eval_err02(c,ob,re,ce,rx,cx,mod_form,d_start)
                if err_right<err0:
                    #raw_input("3023 right "+str(err_right))
                    while err_right<err0:
                        #print "Expanding ",err_right   
                        err0=err_right    
                        rx*=hstep
                        cx*=hstep
                        err_right=full_eval_err02(c,ob,re,ce,rx,cx,mod_form,d_start)
                        #print "right ",err_right
                    rx/=hstep
                    cx/=hstep
                    #raw_input("3030 right "+str(err0))
                else:
                        
                   rx/=2*hstep
                   cx/=2*hstep
                   err_left=full_eval_err02(c,ob,re,ce,rx,cx,mod_form,d_start)
                   if err_left<err0:
                        #print "Contracting " ,err_left   
                        rx/=hstep
                        cx/=hstep                        
                        err_left=full_eval_err02(c,ob,re,ce,rx,cx,mod_form,d_start)
                        while err_left<err0:
                            err0=err_left    
                            rx/=hstep
                            cx/=hstep
                            err_left=full_eval_err02(c,ob,re,ce,rx,cx,mod_form,d_start)
                        #raw_input("3042 "+str(err_left))
                   rx*=hstep
                   cx*=hstep
            #half_of_semi_start=32
             
                        

                    
                
            err1=full_eval_err02(c,ob,re,ce,rx,cx,mod_form,d_start)




            
            print "\nNew Starting error:  ",comma_form(err1)
            quick_view5(ob,re,ce,rx,cx,rlab,clab)
            npass=0
            #semi_start_err=full_eval_err02(c,ob,re,ce,rx,cx,mod_form)
            
##            if nss==0:  #Beginning first pass.  These are the values to beat.
##                least_err=err1
##                semi_start_best_re=re;semi_start_best_ce=ce;semi_start_best_rx=rx;semi_start_best_cx=cx
##                outstuff1(c,re,ce,rx,cx,rlab,clab,ob,ob_rsum,ob_csum,ob_total)
##                note="  Previous Least Error ="+comma_form(best_err)
           
            c["use_stand"]=False  #Have to check this for possible re-instatement.
            #c["use_stand"]=True  #Dec 2011, restoring continuation.  This seems consistent with other uses of use_stand
            # Nope, apparently not:  the standardizer doesn't have nrow.  It needs it.  That means it never ran.
            
            if nss>0:  #Useful to have on screen, even though it does it again below
                print "\nPreliminary Results from Multiple Startups ("+str(n_semi_starts)+" requested): "
                various_startups.sort()
                various_startups.reverse()
                ssf=open(c["root"]+"strt","w")
                count=len(various_startups)
                if len(various_startups)<=10:
                    abbreviate=False
                else:
                    abbreviate=True    
                for ss in various_startups:
                    if count==5 and len(various_startups)>10: print    
                    if not abbreviate or count>len(various_startups)-5 or count<=5:    
                        print "%4i: "%(count),comma_form(ss),"  "
                    count-=1
                    ssf.write(comma_form(ss)+"\n")
                ssf.close()    
            #raw_input("debug, check startups at 3002")
        
            npass=0

            #    First half

            #half-start without gram-schmidt
            npasses_in_opt=half_of_semi_start ##32 (3 for speed during debugging)
            c["max_pass"]=half_of_semi_start
            #raw_input("BAA npass"+str(npass))

            #debug
            #errx=full_eval_err02(c,ob,re,ce,rx,cx,mod_form,d_start)
            #print "\nNew Starting error:  ",comma_form(errx)
            #raw_input("debugging for CA too large at 3078")

            #print "3634 use_stand=",c["use_stand"]
            #raw_input("3635")
            
            npass,new_re,new_ce,new_rx,new_cx=do_passes(self,npass,c,rlab,clab,ob,ob_rsum,ob_csum,ob_total,
                                        re,ce,rx,cx,npasses_in_opt,note,best_err)
            d_start=c["d_start"] #kludge (it all should be in c)    

            

            semi_start_err=full_eval_err02(c,ob,new_re,new_ce,new_rx,new_cx,mod_form,d_start)
            if semi_start_err<best_err:
                    best_err=semi_start_err
                    best_re=re; best_ce=ce; best_rx=rx; best_cx=cx
            if semi_start_err<err1:
                    err1=semi_start_err
                    re=new_re; ce=new_ce; rx=new_rx; cx=new_cx
                    
            #print "2936 err after do_passes 1:  ", err1
            #raw_input("2936")



            #    Second half  (Breaking it into halves introduces a standardization at the beginning of each half
            #                  (It appears that imposing a gram_schmidt orthogonzlization and rounding was not paying off
            
        
            ##complete semi-start with one gram-schmidt, then continue without more
            #print "\nBacking off with gram-schmidt orthogonalization and continuing the start up.\n"
            #drive_gram_schmidt(c,nrow,ncol,c["ndim"],rx,cx)
##            print "\nBacking off with rounding"
##            rx=round_array(rx,4)
##            cx=round_array(cx,4)

            c["max_pass"]*=2
            #raw_input("AAA"+str(c["max_pass"]))
            #raw_input("BAB npass"+str(npass))

            npass,new_re,new_ce,new_rx,new_cx=do_passes(self,npass,c,rlab,clab,ob,ob_rsum,ob_csum,ob_total,
                                        re,ce,rx,cx,npasses_in_opt,note,best_err)
            #raw_input("returned from do_passes") 
            #Book keeping before either more semi-starts or letting it run        
            semi_start_err=full_eval_err02(c,ob,new_re,new_ce,new_rx,new_cx,mod_form,d_start)


            if semi_start_err<best_err:
                    best_err=semi_start_err
                    best_re=new_re; best_ce=new_ce; best_rx=new_rx; best_cx=new_cx
                    outstuff1(c,re,ce,rx,cx,rlab,clab,ob,ob_rsum,ob_csum,ob_total)
            if semi_start_err<err1:
                    err1=semi_start_err
                    re=new_re; ce=new_ce; rx=new_rx; cx=new_cx

            #print "err after do_passes 2 @2782"
            various_startups.append(err1)
            line= "error, this 'semi-start'="+comma_form(err1)  +" Previous Least Error ="+ str(best_err)+"\n"
            print line
            if nss>0:
                print "\nMultiple startups: "
                various_startups.sort()
                various_startups.reverse()
                ssf=open(c["root"]+"strt","w")
                count=0
                for ss in various_startups:
                    count+=1
                    print count," ",comma_form(ss),"  "
                    ssf.write(comma_form(ss)+"\n")
                ssf.close()    
            print "\n"

            

            note="  Current Best Error ="+comma_form(best_err)
            line+=note
            #print line
        err=best_err
        re=best_re;ce=best_ce;rx=best_rx;cx=best_cx
        note=""

    elif c["continuation_or_startup"]=="continuation":

        """
    stored_parameters={}
    stored_parameters["re"]=re
    stored_parameters["ce"]=ce
    stored_parameters["rx"]=rx
    stored_parameters["cx"]=cx
    stored_parameters["minkowski_power"]=minkowski_power
    stored_parameters["attenuation_power"]=attenuation_power
    stored_parameters["error"]=re
    stored_parameters["d_start"]=re
    stored_parameters["mod_form"]=re
    stored_parameters["mod_type"]=re
    stored_parameters["use_diagonal"]=use_diagonal
    stored_parameters["ndim"]=ndim

"""
        stored_parameters=read_param_file02(c,c["root"]+"a")

        re=stored_parameters["re"]+0.
        ce=stored_parameters["ce"]+0.
        rx=stored_parameters["rx"]+0.
        cx=stored_parameters["cx"]+0.
        best_re=stored_parameters["re"]+0.
        best_ce=stored_parameters["ce"]+0.
        best_rx=stored_parameters["rx"]+0.
        best_cx=stored_parameters["cx"]+0.


        #compare stored parameters to the present control file"
        if c['ndim']!=stored_parameters["ndim"]:
            print "ndim ",c["ndim"],"in SETUP does not match ndim,",stored_parameters["ndim"]," stored."
            print "Options to be programmed.  Currently the stored 'ndim' will be used."
            c["ndim"]=stored_parameters["ndim"]
            
        if c['minkowski_power']!=stored_parameters["minkowski_power"]:
            print "minkowski_power",c["minkowski_power"],"in SETUP does not match minkowski_power,",stored_parameters["minkowski_power"]," stored."
            print "Options to be programmed.  Currently the stored 'minkowski_power' will be used."
            c["minkowski_power"]=stored_parameters["minkowski_power"]
            
        if c['attenuation_power']!=stored_parameters["attenuation_power"]:
            print "attenuation_power",c["attenuation_power"],"in SETUP does not match attenuation_power,",stored_parameters["attenuation_power"]," stored."
            print "Options to be programmed.  Currently the stored 'attenuation_power' will be used."
            c["attenuation_power"]=stored_parameters["attenuation_power"]

        print "3734",c["d_start"],type(c["d_start"])
        print "3735",stored_parameters["d_start"],type(c["d_start"])  ##### figure it out:  this is re, not d_start #######################
        if c['d_start']!=stored_parameters["d_start"]:
            print "d_start",c["d_start"],"in SETUP does not match d_start,",stored_parameters["d_start"]," stored."
            print "Options to be programmed.  Currently the stored 'd_start' will be used."
            c["d_start"]=stored_parameters["d_start"]
        #raw_input("debug recovery of d_start at 3784")            
        if c['use_diagonal']!=stored_parameters["use_diagonal"]:
            print "use_diagonal",c["use_diagonal"],"in SETUP does not match use_diagonal,",stored_parameters["use_diagonal"]," stored."
            print "Options to be programmed.  Currently the stored 'use_diagonal' will be used."
            c["minkowski_power"]=stored_parameters["minkowski_power"]

            
        best_err=full_eval_err02(c,ob,re,ce,rx,cx,c["mod_form"],c["d_start"])

        print "continuation run, see old 'run_choice' in code" #, run_choice
        c["use_stand"]=False  #Have to check this for possible re-instatement.

        try:
            print "imported minkowski_power & attenuation_power",
            print stored_parameters["minkowski_power"],stored_parameters["attenuation_power"]
        except:
            print "minkowski_power and/or attenuation_power not imported."    
        print "compare to current SETUP file:  minkowski_power:",c["minkowski_power"],c["attenuation_power"]

        try:
            print "imported d_start",
            print stored_parameters["d_start"]
        except:
            print "d_start not imported."    
        print "compare to current SETUP file:  d_start:",c["d_start"]



        print "      mod_form",c["mod_form"]," d_start",c["d_start"]
        print "evaluating using the parameters as now set inside the program:, best_err=",best_err," versus ",stored_parameters["error"],"as stored"
        raw_input("3583:  Continue?")

        print "\nprinting spread_sheet"
        #spread sheet output
        print "\n contents of c"
        ck=c.keys()
        ck.sort()
        for com in ck:
            print com,c[com]
        print "where are the labels?"    
        interface_to_spread_sheet(c,ob,2**(re),2**(ce),rx,cx,c["rlab"],c["clab"],best_err)

        raw_input( "After retrieval:  Press any key to continue.")
            
        note=""
        #n_passes_in_opt=64
        npass=0
    else:
        raw_input("uninterpretable value in c['continuation_or_startup']")

    #Now, having tried several start-ups or having continued from a file, let it run
    c["max_pass"]=c["max_passes_for_run"] #100000
    half_of_semi_start=32
    n_passes_in_opt=32 #64
    #n_passes_in_opt=c["n_passes_in_opt"]
    c['inside_a_semi-start']=False
    #print "3601  n_passes_in_opt",n_passes_in_opt
    #raw_input("3602")
    npass,re,ce,rx,cx=do_passes(self,npass,c,rlab,clab,ob,ob_rsum,ob_csum,ob_total,
                                best_re,best_ce,best_rx,best_cx,n_passes_in_opt,note,best_err)
    d_start=c["d_start"] #kludge (the error fcn should take it directly from c)
    least_err=full_eval_err02(c,ob,re,ce,rx,cx,mod_form,d_start)
    return [least_err,c,re,ce,rx,cx]

def round_array(ar,r):  #should be a matrix function.  But I can't find it
        nrow=size(ar,0)
        ndim=size(ar,1)
        for row in range(nrow):
                for dim in range(ndim):
                        ar[row,dim]=round(ar[row,dim],r)
        return ar                


#fn="SevenH1Test_Template.txt"
def read_template_in_dwv(fn):  #was in dwvGui011.  Change name and put here.
    inf=open(fn,"r")
    lines=inf.readlines()
    print len(lines), " lines in template ",fn
    command_dictionary={}

    few_lines=[]
    for i in range(len(lines)):
        line=lines[i]
        x=line.find("#")
        if x>=0:  line=line[:x]
        if len(line.strip())>0:  few_lines.append(line.strip())

#    print "few_lines  debug"
#    print few_lines
#    raw_input("")
    for line in few_lines:
        e=line.index("=")
        command=line[:e].strip()
        values=line[e+1:].strip()
        command_dictionary[command]=values

    # a little ad hoc cleanup
    command_dictionary['nrow']=int(command_dictionary['nrow'])
    command_dictionary['ncol']=int(command_dictionary['ncol'])
    command_dictionary['ndim']=int(command_dictionary['ndim'])
    command_dictionary['mod_type']=command_dictionary['mod_type'].lower()
    command_dictionary['use_diagonal']=bool(command_dictionary['use_diagonal'])
    command_dictionary['use_stand']=bool(command_dictionary['use_stand'])
    command_dictionary['erf']=command_dictionary['erf'].lower()
    command_dictionary['minkowski_power']=float(command_dictionary['minkowski_power'])
    command_dictionary['attenuation_power']=float(command_dictionary['attenuation_power'])
    command_dictionary['nlayer']=int(command_dictionary['nlayer'])
    command_dictionary['error']=float(command_dictionary['error'])
    if command_dictionary["erf"]!="chi_square":
        print_text_window("undefined error function.  (allow only 'chi_square' so far)")   

    return command_dictionary

                
def set_commands02():  #Adapted from dvgui011.py
    if 1==1: #This is a default template.  The correct one is specified below it.
       default_field_value_dictionary={"template":"sevenH1test_template",
                                      "root":"Brianxtab22x9_01",
                                      "error":10e30,
                                      "minkowski_power":5,
                                      "attenuation_power":2,
                                      
                                      "ndim":2,
                                      "nrow":0,
                                      "ncol":0,
                                      "mod_type":"rectangular",
                                      "use_diagonal":True,
                                      
                                      "erf":chi_square,
                                      "use_stand":False,
                                      "nlayer":1,
                                      "continuation_or_startup":"startup",
                                      "max_passes_for_run":10000, #1000 for debugging 10000
                                      "n_semi_starts":5}  
    else:
        default_field_value_dictionary={"template":"test_3X4_template",
                                      "root":"Test_3X4.txt",
                                      "error":10e30,
                                      "minkowski_power":2,
                                      "attenuation_power":2,
                                      
                                      "ndim":1,
                                      "nrow":3,
                                      "ncol":4,
                                      "mod_type":"rectangular",
                                      "use_diagonal":True,
                                      
                                      "erf":chi_square,
                                      "use_stand":False,
                                      "nlayer":1,
                                      "continuation_or_startup":"startup"}
                                      



    use_title="Navigate to a Template file (not a data file). It will specify the data file & instructions."
    #use_title+="(E.g. "+fn+")"
    #fn=askopenfilename(title=use_title)  #NOT COMPATIBLE With running from IDLE
    #fn="Cardinal_33x43_template.txt"
    #fn="facemat1_185x20_template.txt"
    #fn="Allstate_template.txt"         # CHANGE HERE to change templates and, therefore, files
    #fn="wordXdoccopyfacemat"           # CHANGE HERE to change templates and, therefore, files
    #fn="Friends_9x9_template.txt"
    fn="goldfarb1template.txt"
    fn="brian1template.txt"
    template_field_value_dictionary=read_template_in_dwv(fn)
    #print "template...: ",template_field_value_dictionary
    #raw_input("")
    #print template_field_value_dictionary
    items=template_field_value_dictionary.keys()
    items.sort()
    print
    print "summary of commands from template"
    #print "incoming attenuation and minkowski",attenuation_power,minkowski_power
    for item in items:
        print "%-20s"%(item+":")+str(template_field_value_dictionary[item])
    raw_input("review")
    current_field_value_dictionary=template_field_value_dictionary
    for item in default_field_value_dictionary:
        if not item in current_field_value_dictionary:  #If NOT over-ridden by the template
            try:
                self.current_field_value_dictionary[item]=default_field_value_dictionary[item]
            except:
                current_field_value_dictionary[item]=default_field_value_dictionary[item]
    return current_field_value_dictionary

#receives arguments that were otherwise read from a template by set_commands02()
def dwv_entry(root="data_beginnings3mat",
         nrow=71,
         ncol=100,
         ndim=2,
         mod_type="rectangular",
         attenuation_power=4,
         minkowski_power=4,
         use_stand=False,
         use_diagonal=True,
         nlayer=1,
         erf=chi_square,
         continuation_or_startup="startup",
         max_passes_for_run=1000,
         clean_up=True,
         suppress_print_of_row_labels=False,
         n_semi_starts=5,
         icons=True,
         draw_lines=True,
         nudge_columns_toward_labelled_sequence_during_startup=False,     
         draw_column_sequence=False,
         last_column_gt_first_column=False,     
         row_heights="False",
         font=("Helvetica",12,"normal"),
         omission_value=-999,
         mod_form="p", #power normal, as of 2010, the standard for DwV (One letter:  It is checked frequently.)
         d_start=False,
         opt_minkowski=False,
         opt_attenuation=False,
         opt_d_start=False,
         best_of_scanned=888888888.8):  

        #raw_input("debug 3317 in dwvB040")        
        #raw_input("n_semi_starts kludged to "+str(n_semi_starts))
        current_field_value_dictionary={}
        current_field_value_dictionary["root"]=root
        current_field_value_dictionary["nrow"]=nrow
        current_field_value_dictionary["ncol"]=ncol
        current_field_value_dictionary["ndim"]=ndim
        current_field_value_dictionary["mod_type"]=mod_type
        current_field_value_dictionary["attenuation_power"]=float(attenuation_power)
        current_field_value_dictionary["requested_attenuation_power"]=float(attenuation_power)
        current_field_value_dictionary["minkowski_power"]=minkowski_power
        current_field_value_dictionary["requested_minkowski_power"]=minkowski_power
        current_field_value_dictionary["use_stand"]=use_stand
        current_field_value_dictionary["use_diagonal"]=use_diagonal
        current_field_value_dictionary["nlayer"]=nlayer
        current_field_value_dictionary["erf"]=erf
        current_field_value_dictionary["continuation_or_startup"]=continuation_or_startup        
        current_field_value_dictionary["max_passes_for_run"]=max_passes_for_run #1000 for debugging 10000
        current_field_value_dictionary["clean_up"]=clean_up #1000 for debugging 10000
        current_field_value_dictionary["suppress_print_of_row_labels"]=suppress_print_of_row_labels
        current_field_value_dictionary["n_semi_starts"]=n_semi_starts
        current_field_value_dictionary["use_diagonal"]=use_diagonal
        current_field_value_dictionary['icons']=icons
        current_field_value_dictionary['draw_lines']=draw_lines
        current_field_value_dictionary['nudge_columns_toward_labelled_sequence_during_startup']=nudge_columns_toward_labelled_sequence_during_startup
        current_field_value_dictionary['draw_column_sequence']=draw_column_sequence
        current_field_value_dictionary['last_column_gt_first_column']=last_column_gt_first_column
        current_field_value_dictionary['font']=font
        current_field_value_dictionary['row_heights']=row_heights
        current_field_value_dictionary['omission_value']=int(omission_value)
        current_field_value_dictionary['mod_form']=mod_form
        current_field_value_dictionary['d_start']=d_start
        current_field_value_dictionary['opt_attenuation']=opt_attenuation
        current_field_value_dictionary['opt_minkowski']=opt_minkowski
        current_field_value_dictionary['opt_d_start']=opt_d_start
        current_field_value_dictionary['best_of_scanned']=best_of_scanned
        current_field_value_dictionary['color_from_bracket']=False
        
        #print "4003 use_stand",current_field_value_dictionary["use_stand"]
        #raw_input("4004")
        #print type(opt_d_start),opt_d_start
        #print type(opt_minkowski)
        #raw_input("debug at 3595")
                
        [least_err,c,re,ce,rx,cx]=dwv_main("",current_field_value_dictionary)
        return [least_err,c,re,ce,rx,cx]


# ===========================================================================================================

if __name__=="__main__":

    #c=set_commands()
    print "calling set_commands02"
    raw_input("")
    current_field_value_dictionary=set_commands02()  #switch to use of template 071025
    print current_field_value_dictionary    
    dwv_main("",current_field_value_dictionary)  #calling from GUI:  main(self,c)
    

