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

#need principle components axes for Euclidean space.
from numpy import *
from random import *
from gram_schmidt02 import *
#from RandomArray import *

def pc(nrow,ncol,x_original):
    #For vectors of nrow elements in ncol dimensions, compute
    #the variance maximizing principal components.

    #Use the mean corrected version

    #Use power method


    #covariance_matrix=zeros((ncol,ncol),float)

    #Rotate about means as center.

    x=matrix(x_original)
    means=sum(x,0)/float(nrow)

    #print "data",
    #print x

    #print "means",means

    x2=x[:nrow,:ncol]-means[:ncol]
    x2=matrix(x2)
    #print "data re-centered at means"
    #print x2

    covariance=(transpose(x2)*x2)/float(nrow)
    #print "covariance"
    #print covariance

    #Find eigen structure:

    rz=zeros((ncol,ncol),float)
    for i in xrange(ncol):
        for j in xrange(ncol):
            rz[i,j]=random()
    #print "random"
    #print rz


    #make columns of rz unit-length vectors

    u=unitize(rz)
    #print "random matrix, unitized"
    #print u
  


    

    #Move rz toward the eigen matrix
    u=matrix(u)
    covariance=matrix(covariance)
    check1=u[:,:] #copy
    more=True
    tolerance=.00001
    for i in xrange(100):
        more=False
        u=covariance*u
        u,b,l=gram_schmidt(ncol,ncol,u)
        u=unitize(u)
        max_diff=0
        #tried a matrix/array routine for max of diff.  Couldn't get it to work
        for i2 in range(ncol):
            for j2 in range(ncol):
                #print i2,j2,abs(check1[i2,j2]-u[i2,j2])
                if abs(check1[i2,j2]-u[i2,j2])>tolerance:
                    more=True
                    break
            if more==True:
                    break                
        check1=u[:,:]
        if not more:
            break
        
    a=x2*u
    #print a

    #change signs (if necessary) for positive skew

    a=positive_skew(a)
    
    return a
    


    #Do quick approximations using the 8th power.
    #Then hone it on the first

##    #The eigenvectors of c2 are eigenvectors of c itself (with different eigen values)    
##
##    rz2=rz*c2
##    rz2=unitize(ncol,rz)
##    rz2=rz2*covariance  #gets the eigenvectors shrunk or stretched to their eigen values
##
##    eigen_values=lengths(rz2)
##    
##    #re-order by eigen values
##    eigen_matrix,eigen_values=re_order(rz2,eigen_values)
##
##    #coordinates to the orthonormal basis
##    z=x*eigen_matrix
##
      #choose sign such that skew is positive 
##    return z

def unitize(mat):
    nrow=size(mat,0)
    ncol=size(mat,1)

    #print "mat"
    #print mat

    a=array(mat) #allow me to do simple multiplication
    a=a**2 #a*a   #for the array, this comes out as cell by cell squaring.
    s=sum(a,0)

    #s=s**.5
    s**=.5
    a=matrix(a)
    s=matrix(s)
##    print "a"
##    print a
##    print "s"
##    print s
    b=mat[:nrow,:ncol]/s[:ncol]
##    print "unitized?"
##    print b
    return b

def positive_skew(x):
    nrow=size(x,0)
    ncol=size(x,1)

    means=sum(x,0)/float(nrow)

    m=array(x[:,:])
    means=array(means)
    #print "means"
    #print means
    
    #mean corrected
    m=m-means
    
    #cubes
    m=m*m*m
    #close enough to skew:
    s=sum(m,0)

    x2=x[:,:] #copy for return
    for i in xrange(ncol):
        if s[i]<0:
            x2[:,i]=-x2[:,i]
    return x2        
             

def lengths_matrix(m):
    m=matrix(m)
    
    
if __name__=="__main__":
    #build test from Green, Mathematical Tools for Applied Data Analysis.

    seed(1)
    data=matrix([[1,1],
                 [2,1],
                 [2,2],
                 [3,2],
                 [5,4],
                 [5,6],
                 [6,5],
                 [7,4],
                 [10,8],
                 [11,7],
                 [11,9],
                 [12,10]])

    #same 12 data points on principal component axes:
    print "test data"
    print data
    z=pc(12,2,data)
    
    print "z"
    print z
    

    

    

    

    
    
