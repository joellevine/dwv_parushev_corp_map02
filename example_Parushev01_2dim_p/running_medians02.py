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

#02:  Add Tukey's end point smoothing

from numpy import *

def running_medians(x_original):  #repeated running medians of 3
    #inorder to impose something like time sequencing of linear models
    #smooth column coordinates with running medians of 3, computed
    #in order of date
    #print "running medians, incoming",x_original
    x=x_original[:]  #copy it
    #print "x",x
    n=size(x)
    #print "\nn=",n," type=",type(n),"\n"
    x2=zeros((n),float)    

    change=True
    while change==True:
        change=False       #make end point a simple average with its adjacent point.
        #"copy on" end point during smoothing
        x2[0]=x[0]
        x2[n-1]=x[n-1]
        
        for i in range(1,n-1):  #leave out the end points
            t0=x[i-1]
            t1=x[i]
            t2=x[i+1]
            lis=[t0,t1,t2]
            lis.sort()
            x2[i]=lis[1]
            if x2[i]!=x[i]:  change=True
        #print "in running_medians:"
        #print x[:]
        #print x2[:]
        x=x2[:]
        #print x

    #Deal with the end points
    x2[0]=end_point_smooth(x2[2],x2[1],x2[0])
    x2[n-1]=end_point_smooth(x2[n-3],x2[n-2],x2[n-1])
    
                           
    return x2

def end_point_smooth(next_but_one_to_end,next_to_end,true_end):
    #Tukey's end point smooth is the median of 3 values
    # 1) the true end
    # 2) the smoothed value for the next-to-end point
    # 3) the extrapolated value, extrapolated from next but one to next to end

    # assuming equal spaceing on some "x" variable, while smoothing the y, e.g.,
    # assuming these values come from equally spaced dates. the extrapolation is simple

    extrapolated= next_to_end + (next_to_end-next_but_one_to_end)

    lis=[extrapolated,next_to_end,true_end]
    lis.sort()
    return lis[1]


 

                             

if __name__=="__main__":
    a=array([3,1,4,5,7,9,7,5,4,1,3])
    print running_medians(a)
                 
            
