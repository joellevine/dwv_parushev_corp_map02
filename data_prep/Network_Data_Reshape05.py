# -*- coding: utf-8 -*-


# Agenda
# print the connected sets to separate folders
# write a program that allows trimming according to numbers of non_zero columns of each row
# and number pf non_zero rows of each column
# Then have it drop a starter control file for DwV (or two, one for i one for p). Drop
# the current "Generic" .py file for DwV in there too.  (Continuation is still not working, may
# need to hide it for a while or announce that it is non-functional (so choose your number of runs
# for overdoing-- you can always interrupt.

# Also collect all the shortest paths of each length.  That should enable statistics
# on path length, min, max, average,  and on between-ness as paths disabled if it were gone.

# People can trim the csv files I'm leaving for things like affect that leaving out banks has
# on path length.

# Can do the same for corps or persons with highest chi-square -- Interesting to compare
# to brute force of dropping most-connected corporations.  (
# Probably need some conventional measures of centrality, for comparison to chi-square

# 04 Drop pc files of connected subsets into folders.  That way, after the initial
#    extraction of data, the program can be directed to start again on the pc from the full
#    data or the pc from subsets.

# 03 working for extracting pc table (person to corporation) and
#    for cc frequencies (full data) and pp frequencies( full data)
#    These are dropped into appropriately named folders and csv files

#    These files can be opened and analyzed with Excel

#This program takes Todors interlocks -- csv file, as used to collect data
#It creates a bunch of derived files

# written in Python 2.6 (should work with Python 2.7, not Python 3.x
# it imports the library numpy for python 2.6

# Todor's data file uses columns A though I
# These are
# 1 A ID#
# 2 B 2 Names	  
# 3 C relation#
# 4 D name of relation
# 4 E Corp #
# 5 F Corp
# 6 G Full name of Corporation
# 7 H Type of business
# 7 I Miscellaneous info

# The first row of his csv has labels.
# Remaining rows are entries for people, although a person with more than one link will
# have more than one row -- scattered somewhere else in the file (mingled in the data
# for people of different corporations.

# Starting with person and corporation, identified by having the same number (regardless of name)
#  (We should get to industry, type of business, but not yet

#Build these files
#1:   The person by corporation (unique id # for person and unique Corp #
#     Multiple rows for one person have been combine as have multiple columns for one corporation

#    For this file the original file has identified rows that belong
#    to the same person by checking their ID numbers

from numpy import *
import os
import copy

def info():
    print """
# written in Python 2.6 (should work with Python 2.7, not Python 3.x
# I am running it using IDLE (the IDLE that comes with Python 2.6)

# Todor's data file uses columns A though I
# These are
# 0 A ID#
# 1 B 2 Names	  
# 2 C relation#
# 3 D name of relation
# 4 E Corp #
# 5 F Corp
# 6 G Full name of Corporation
# 7 H Type of business
# 8 I Miscellaneous info

# Starting with person and corporation, identified by having the same number (regardless of name)
#  (We should get to industry / type of business, but not yet

IMPORTANT:  Before starting, open the original as an Excel file (not as a csv file).  As an Excel file, edit it to remove
all commas.  You can replace these commas by dashes.  Save this edited file and save it again as a new csv file

For now, type the name of this csv file into the code below as
fn="ChileNetwork no commas.csv"
and then save this program.

For now, I am including the type of business within the name

Network_Data_Reshape03.py  is working for extracting pc table (person to corporation) from the data
table and counting corp-corp links and person-person links on the full data

#    These are dropped into appropriately named folders and csv files

#    These files can be opened and analyzed with Excel

"""

def build_row_col_table(fn):
    inf = open(fn,"r")   #infile is the name, inside the program for the file accessed by fn
    lines=inf.readlines()  #read it

    if len(lines)==1:
        lines=lines[0].split("\n")
    if len(lines)==1:
        lines=lines[0].split("\r")


    #for i in range(100):
    #    print lines[i]
    #    
        
    print "confirm that this is correct:  The length of the file is ",len(lines)
    raw_input("Press RETURN to verify  if not correct -- get help")

    #collect data in dictionaries
    person_name_person_id={}
    person_id_person_name={}
    corp_name_corp_id={}
    corp_id_corp_name={}
    person_id_corp_id={}
    corp_id_type_of_business={}

    col_person_id=0 #location in each line, where the first column of the raw data is column 0
    col_person_name=1
    col_corp_id=4
    col_corp_name=6
    col_type_of_business=7
    
    for line in lines[1:]:
        special=False
        #if "INVERSION" in line.upper() and "CLAUDIO" in line.upper(): special=True
        #if "SANTAND" in line and "HUERT" in line.upper(): special=True
        #if "SANTAND" in line and "HUERT" in line.upper(): special=True
        if special:  raw_input("special"+str(special))
        line=line.strip()
        line=line.split(",")

        #extract info from this line
        person_id=    int(line[col_person_id])
        person_name=      line[col_person_name]
        corp_id=      int(line[col_corp_id])
        corp_name=      line[col_corp_name]
        type_of_business=line[col_type_of_business]
        #print corp_name, type_of_business

        if special:
            print "line132"
            print "person_id",person_id
            special_id=person_id
            print "person_name",person_name
            print "corp_id",corp_id
            print "corp_name",corp_name
            print "type_of_business",type_of_business

        #cut for debugging:
        if 1==1: #if corp_id<=4:

            #Bookkeeping
            #if person_name not in person_name_person_id:
            #    person_name_person_id[person_name]=person_id
            #if person_id not in person_id_person_name:
            #    person_id_person_name[person_id]=person_name

            #use ID not name.  a second name with the same ID should be ignored and replaced by the first
            if  person_id not in person_id_person_name:
                person_id_person_name[person_id]=person_name
                person_name_person_id[person_name]=person_id
                
            #if corp_name not in corp_name_corp_id:
            #    corp_name_corp_id[corp_name]=corp_id
            #if corp_id not in corp_id_corp_name:
            #    corp_id_corp_name[corp_id]=corp_name
            #print "debug at 158 corp_id's:,",corp_id_corp_name
            #raw_input("159")
            if corp_id not in corp_id_corp_name:
                corp_id_corp_name[corp_id]=corp_name
                corp_name_corp_id[corp_name]=corp_id

            if len(type_of_business.strip())>0:  #if present
                if corp_id not in corp_id_type_of_business:
                    corp_id_type_of_business[corp_id]=type_of_business
            if special:
                pppk=person_name_person_id.keys()
                pppk.sort()
                for ppp in pppk:
                    print ppp,person_name_person_id[ppp]
                #print person_name_person_id
                print
                print person_id_person_name
                print
                print corp_name_corp_id
                print corp_id_corp_name
                
            #record data 
            if person_id not in person_id_corp_id:
                person_id_corp_id[person_id]=[corp_id]
                if special:  print "**"
            else:
                person_id_corp_id[person_id].append(corp_id)
                if special:
                    print "=="
            if special:
                print "test id",type(special_id)
                print special_id
                print person_id_corp_id[special_id]
                print "8374260"
                print person_id_corp_id[8374260]
                raw_input("166")    




        npersons=len(person_id_person_name)
        #print "debug person_id_person_name  how many items?"
        #print person_id_person_name
        #print "npersons",npersons
        
        ncorps=len(corp_id_corp_name)
        #print "npersons,ncorps at 194",npersons,ncorps  #for debugging
        pc=zeros((npersons,ncorps),float)
        rlab=[]  #row (person) labels
        clab=[]  #col (corp) labels

        kp=person_name_person_id.keys()
        kp.sort()
        kc=corp_name_corp_id.keys()
        kc.sort()

        #print "debug number of person id's is:",len(kp)
        #print "debug number of corp id's is",len(kc)


        for pname in kp:
            rlab.append(pname)
        for cname in kc:
            clab.append(cname)
        clab_with_industry=[]    
        for i in range(len(clab)):  #append industry to name
            cname=clab[i]
            cid=corp_name_corp_id[cname]
            industry=corp_id_type_of_business[cid]
            clab_with_industry.append(cname+"<"+industry+">")
            
        
        #print "debug rlab",rlab    
        for pname in kp:
            #print "name",pname,"debug"
            row=rlab.index(pname)

            for cid in person_id_corp_id[person_name_person_id[pname]]:
                cname=corp_id_corp_name[cid]
                col=clab.index(cname)
                #print shape(pc) #debug    fn="ChileNetwork no commas.csv"

                #print "debug row,col",row,col
                pc[row,col]=1
    print len(rlab),"people"            
    print len(clab),"corporations"

    #for i in range(len(rlab)):
    #    print i,rlab[i]
    #print pc[358]
    #print pc[220]
    for j in range(len(clab)):
        print j,clab[j],
        if j%5==0:  print
    #print clab[5]
    #raw_input("after print of row of pc")
 
    return rlab,clab,clab_with_industry,pc

def csv_output(folder,fn,rlab,clab,a):
    if not os.path.exists(folder):
        #print "folder not present"
        os.makedirs(folder)
    line="x"
    for item in clab:
        line+=","+item
    line+="\n"
    for i in range(len(rlab)):
        line+=rlab[i]
        for j in range(len(clab)):
            line+=","+str(a[i,j])
        line+="\n"    
    outf=open(folder+"/"+fn,"w")
    outf.write(line)
    outf.close()

def convert_to_dict(pc):
    nrow=size(pc,0)
    ncol=size(pc,1)
    d={}
    for row in range(nrow):
        v=[]
        for col in range(ncol):
            if pc[row,col]>0:
                v.append(col)
        d[row]=v
    return d    

def sparse_multiply(pc_dict,cp_dict):
#pcp_dict=sparse_multiply(pc_dict,cp_dict)
    pcp_dict={}
    
    pck=pc_dict.keys()
    pck.sort()
    
    cpk=cp_dict.keys()
    cpk.sort()

    for p in pck:
        v=[]
        for c in pc_dict[p]:
            if c in cpk:
                v+=cp_dict[c]
            #print "type v",type(v)    
            v=list(set(v)) #remove duplicates    
        v.sort()        
        pcp_dict[p]=v
    return pcp_dict    
        
        
def build_cc_frequencies(a):
    t=transpose(a)
    return matrix(t)*matrix(a)
    
def extract_pc_subsets_from_pc(rlab,clab,pc):
    #Instead of using matrix multiplication, use dictionaries.  That allows
    #me to keep lists of multiple paths.  This could be more efficient than
    #matrix multiplication, though less convenient to program, because
    #these are "sparse matrices"

    unaccounted_persons=range(len(rlab))  #list of people not yet identified with a subset
    unaccounted_corps=range(len(clab))  #list of corps not yet identified with a subset

    #rewrite data as two matrices, one the transpose of the other
    pc_dict=convert_to_dict(pc)
    cp_dict=convert_to_dict(transpose(pc))

    #For now I'm only interested in connectivity.  That means there is no need
    #to keep track of the separate paths
    #compute pcp
    pcp_dict=sparse_multiply(pc_dict,cp_dict)
    cpc_dict=sparse_multiply(cp_dict,pc_dict)
    #print "debug pc_dict",pc_dict
    #print "debug cp_dict",cp_dict
    #raw_input("332")
    #Should use whichever one is smaller (less computation)
    #For now I am assuming it is the number of corporations
    
    power=0
    m=copy.deepcopy(cpc_dict)
    #print "debug initial m",m
    
    #print "DDD",type(m),type(cpc_dict)
    while power<len(clab):
        product=sparse_multiply(m,m)
        if power==0:
            power=1
        else:    
            power*=2
            
##        #Trim it
##        for ca in product.keys():
##            if ca in product[ca]:
##                ind=product[ca].index(ca)
##                del product[ca][ind]
        print "Power = ",power," multiplying..."        
        m=copy.deepcopy(product)
    #print "debug 350, product",product
    #collect
    connected_sets=[]

    #print "Atype product",type(product)

    while len(unaccounted_corps)>0:
        #collect corporations directly
        setc=list(set([unaccounted_corps[0]]))
        #print "setc",setc
        del unaccounted_corps[0]
        #print "Btype product",type(product)
        setc+=product[setc[0]]
        setc=list(set(setc)) #remove duplicates from list
        for item in setc:
            #print "item",item,type(item)
            #print "type unaccounted corps",type(unaccounted_corps)
            #print "unaccounted_corps",unaccounted_corps
            #print "item",item
            if item in unaccounted_corps:
                ind=unaccounted_corps.index(item)
                del unaccounted_corps[ind]
        #collect persons indirectly    
        setp=[]
        for c in setc:
            setp+=cp_dict[c]
        setp=list(set(setp)) #remove duplicates
        for item in setp:
            if item in unaccounted_persons:
                ind=unaccounted_persons.index(item)
                del unaccounted_persons[ind]
        connected_sets.append([len(setc),setp,setc])
        connected_sets.sort()
        connected_sets.reverse()

    for item in connected_sets:
        print "-"*80
        print "Number of Corprorations: ",len(item[2])
        for it in item[2]:
            print clab[it]," |  ",
        print
        print

        print "Number of People: ",len(item[1])
        for it in item[1]:
            print rlab[it]," |  ",
        print
        print
        #print len(item[2]),item[1]

    return connected_sets    
            






#------------------------------------

if __name__=="__main__":   #this line makes this whole file work as a program  (Otherwise it would
                           # act as a library for other programs
    info()
    fn="ChileNetwork no commas.csv"
    #fn="Levine_fudge.csv"
    rlab,clab,clab_with_industry,rctable=build_row_col_table(fn)
    first_out_fn=fn[:8]+"rclinks.csv"
    csv_output("fullpc",first_out_fn, rlab, clab_with_industry, rctable)
                           
    cc=build_cc_frequencies(rctable)
    full_table_cc_frequencies_fn=fn[:8]+"ccfreq.csv"
    csv_output("fullccfreq",full_table_cc_frequencies_fn, clab_with_industry, clab_with_industry, cc)
    pp=build_cc_frequencies(transpose(rctable))
    full_table_pp_frequencies_fn=fn[:8]+"ppfreq.csv"
    csv_output("fullppfreq",full_table_pp_frequencies_fn, rlab, rlab, pp)

    pp=build_cc_frequencies(transpose(rctable))
    connected_sets=extract_pc_subsets_from_pc(rlab,clab,rctable)

##    print "IMPOSSIBLE, for full data:  corporation 4 (in order) has no people -- so how did it get in the data  impossible"
##    print "The error is in the PC table:  it shows no people for this one corporation. "
##
##
##    print """  One problem with Levine_fudge:  rlab is getting the number of names, where the dictionary has the
##number of id numbers for people.  If there are different names for the same ID, these two get out of whack"""
