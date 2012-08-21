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

#order column vectors by variance

from numpy import *
 
def order_column_vectors_by_variance(matrix_original,labels=False):
    arr=array(matrix_original)

    nrow=size(arr,0)
    ndim=size(arr,1)

    means=sum(arr,0)/float(nrow)

    mean_corrected=arr[:nrow,:ndim]-means[:ndim]

    squares=mean_corrected*mean_corrected #for arrays, this is element by element squaring

    #something is going wrong, presumably a collapsed variance.
    #except that should come out as zero and work anyway

    #New Code
    variances=zeros((ndim),float)
    for dim in xrange(ndim):
        variances[dim]=sum(squares[:,dim])
        if variances[dim]>0:  variances/=float(nrow)

    #Old Code    
    #variances=sum(squares,0)/float(nrow)

    sort_list=[]

    for dim in xrange(ndim):
        sort_list.append([variances[dim],arr[:nrow,dim],dim])
##    print "debug module order_column_vectors"
##    print sort_list
##    raw_input("35 in file order_")

    try:  #breaks down when all variances are zero
        sort_list.sort(reverse=True)
    except:
        junk=1    

    #print sort_list

    #rewrite arr:

    rlab=[]
    brr=zeros((nrow,ndim),float) #2nd copy such that the rewrite does not confused
    for dim in xrange(ndim):
        #print dim,sort_list[dim]
        brr[:nrow,dim]=sort_list[dim][1]
        if labels: rlab.append(labels[sort_list[dim][2]])

    if labels:
        return brr,rlab
    else:
        return brr

#----------------------------------------------

if __name__=="__main__":
    m=zeros((5,3),float)

    for row in xrange(5):
        for dim in xrange(3):
            m[row,dim]=row*dim
    print m        
    m=order_column_vectors_by_variance(m)
    print 
    print m
        
                         
    
    
