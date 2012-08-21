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

# gram-schmidt orthogonalization

# NOT orthonormal basis (orthogonal, with each vector
# having unit length

#try:
#	from numpy import *
#	numpac="numpy"
#except:
#	from Numeric import *
#	numpc="Numeric"
from numpy import zeros


def gram_schmidt(nrow,ncol,array):

    basis=zeros((nrow,ncol),float)       #orthogonal and normal (unit vectors) or sd=1
    components=zeros((nrow,ncol),float)  #orthogonal remainders
    for row in xrange(nrow):
        for col in xrange(ncol):
            components[row,col]=1*array[row,col]   

    for col in xrange(1,ncol):  #each column after the first is made orthogonal to all predecessors
        for preceeding in xrange(col):
            #print "preceding",preceeding
            #print "removing projection onto ",preceeding,"from vector",col
            numerator=0.
            denominator=0.
            for row in xrange(nrow):
                crp=components[row,preceeding]
                numerator+=components[row,col]*crp
                denominator+=crp*crp
            for row in xrange(nrow):
                components[row,col]-=(numerator/denominator)*components[row,preceeding]


#     #also return a normalized form:

     #also return a  form to unit average lenth:
    length=zeros((ncol),float)
    for col in xrange(ncol):
        length[col]=0
        for row in xrange(nrow):
            length[col]+=components[row,col]**2
        length[col]**=.5
        for row in xrange(nrow):
            basis[row,col]=components[row,col]/(length[col]) #shorter
    return components,basis,length    
                
                
            
            
            
    
