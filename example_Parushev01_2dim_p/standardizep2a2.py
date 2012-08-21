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

#standardizep2a2.py
from numpy import *

def standardizep2a2(original_rx,original_cx,attenuation,minkowski):
    if attenuation !=2 or minkowski!=2:
        print "Inappropriate ttempt to use standardization -- bypassed"
        print "(Approriate only for Euclidean space and squared attenuation)"

    else:
        rx,cx=standardize_variance(original_rx,original_cx)
    return rx,cx

def standardize_variance(original_rx,original_cx):
    rx=original_rx[:,:]
    cx=original_cx[:,:]

    rx=mean_center(rx)
    cx=mean_center(cx)
    
    nrow=size(rx,0)
    ncol=size(cx,0)
    ndim=size(rx,1)

    rx,cx=same_sd(rx,cx)
    return rx,cx    


def same_sd(rx,cx):
    nrow=size(rx,0)
    ncol=size(cx,0)
    ndim=size(rx,1)

    rss=rx[0,:]**2
    css=cx[0,:]**2
    for row in range(1,nrow):
        rss+=rx[row,:]**2
    for row in range(1,ncol):    
        css+=cx[row,:]**2
    rss/=nrow
    css/=ncol
    rss**=.5  #standard deviations
    css**=.5  #

    #now, force a common sd in each dimension
    geomean=(rss*css)**.5

    x_correction=geomean/rss
    y_correction=geomean/css

    return rx*x_correction,cx*y_correction
    

def mean_center(rx):
    nrow=len(rx)
    su=sum(rx,0)
    su= su/nrow

    #for i in xrange(nrow):
    mx=rx[:,:]-su
        
    return mx    

# =================================================================================

if __name__=="__main__":
    random.seed(1)
    x=zeros((10,2),float)
    y=zeros((5,2),float)

    for i in range(10):
        for j in range(2):
            x[i,j]=random.random()
    for i in range(5):
        for j in range(2):
            y[i,j]=10*random.random()
    print x
    print
    print y
    x,y= standardizep2a2(x,y,2,2)
    print "standardized"
    print x
    print
    print y
    
            
        
