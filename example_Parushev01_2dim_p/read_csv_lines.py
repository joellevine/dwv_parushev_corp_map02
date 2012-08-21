from numpy import *
import csv  #new for style 2
#print "*()"*30


def read_csv_lines(fn):  #from brian_text01.py
    try:
        reader=csv.reader(open(fn,"rU"))
    except:
        print "read_csv_lines fault on csv.reader  open"
    try:    
        lines=[]
        lines.extend(reader)
    except:
        print "read_csv_lines fault on extend"
    return lines
##def read_csv_lines(fn):  #from brian_text01.py
##    reader=csv.reader(open(fn,"rU"))
##    lines=[]
##    lines.extend(reader)
##    return lines

def csv_face(fn,nrow="",ncol=""):
    print "csv_face "*4
    intended_nrow=nrow  #compare these to what is found
    intended_ncol=ncol
    
    lines=read_csv_lines(fn)
##    print "lines (initiall)"
##    for lin in lines:
##        print lin
##    print     
    
    blank_and_col_labels=lines[0] #column 0 should be blank
    ncol=len(lines[0])-1
    print "ncol=",ncol
    clab=blank_and_col_labels[1:]
    print clab
    row_labels_and_row_data=[]
    last_line=False
    for i in range(1,len(lines)):
        #read until a line has a blank 0 column (no row label)
        #or until it says it is a blank line
        #raw_input(str(len(lines)))
        #print "***",i,len(lines)
        #print lines[i]

        try:
            cz=lines[i][0].strip()  #first column of this csv line
            if cz!="" and cz.upper()!="blank line".upper():
                row_labels_and_row_data.append(lines[i])
                last_line=i
                #for item in row_labels_and_row_data:
                #    print i,item
            else:
                last_line=i-1
                break
        except:
            last_line=i-1
            break
    if last_line==False:
        print "Error reading from file,",fn
        print "Error,   len(lines)=",len(lines)
        print "Error,  data were not read.  Current value of list 'lines'"
        print "at 52:  read from file is :"
        print lines
        raw_input("reading error in read_csv_lines.py")
            
##    print "lines"    
##    print lines
##    print "blank and col labels"
##    print blank_and_col_labels
    #print "row labels and row data"
    #print row_labels_and_row_data
    nrow=last_line
    print "nrow=",nrow,"ncol=",ncol

    if intended_nrow and intended_ncol:
        if nrow!=intended_nrow or ncol!=intended_ncol:
            print "The numbers of rows and columns specified in"
            print "the setup file,",intended_nrow,"and",intended_ncol
            print "do not match what has been interpreted to be in the file"
            print "found",nrow,"and",ncol
            print "Please fix either the setup or the csv file."
            raw_input("(Press Return to exit)")
            sys.exit()
    
    #copy notes, if any, from the end of the file
    notes=""
    print "debug"
##    for i in range(len(lines)):
##        print i,lines[i]
    print "last_line",last_line
    try:
        for i in range(last_line+1,len(lines)):
            notes+=lines[i][0].strip()+"\n"
    except:
        pass

    if len(notes)>0:
        print "Notes from end of data file:"
        if len(notes.strip())>0:
            print notes
        else:
            " none"
        

    w=fn.find(".csv")
    if w<=0:
        print "File problems with file <"+fn+">"
        print "The file must be in csv format (comma separated value format)"
        print "and it's name must use '.csv' as the last 4 characters of"
        print "the name"
        raw_input("(Press 'return' to exit)")
        sys.exit()
    else:
        outfn=fn[:w]+".txt"

    outf=open(outfn,"w")
    eol="\n"
    stuff=""
    stuff+=str(nrow)+eol
    stuff+=str(ncol)+eol
    for row in xrange(len(row_labels_and_row_data)):
        r=row_labels_and_row_data[row]
        s=str(r[1]).strip()   #first number is in 2nd position (after a row label)
        for j in xrange(1,ncol):
            s+=","+str(r[j+1])
        stuff+=s+eol
    for i in xrange(nrow):
        stuff+=row_labels_and_row_data[i][0]+eol
    for j in xrange(ncol):
        stuff+=blank_and_col_labels[j+1]+eol
    outf.write(stuff)
    outf.close
    return outfn

def csv_face02(fn,nrow="",ncol=""):

    #02:  work a little more on figuring out nrow NOT IMPLEMENTED
    intended_nrow=nrow  #compare these to what is found
    intended_ncol=ncol
    
    lines=read_csv_lines(fn)
##    print "lines (initiall)"
##    for lin in lines:
##        print lin
##    print     
    
    blank_and_col_labels=lines[0] #column 0 should be blank
    ncol=len(lines[0])-1
    print "ncol=",ncol
    clab=blank_and_col_labels[1:]
    print clab
    row_labels_and_row_data=[]
    for i in range(1,len(lines)):

        #read until a line does not usefull split into ncol pieces
        #read until a line has a blank 0 column (no row label)
        #or until it says it is a blank line
        #raw_input(str(len(lines)))
        #print "***",i,len(lines)
        #print lines[i]

        try:    
            cz=lines[i][0].strip()  #first column of this csv line
            pieces=cz.split(",")
            
            if cz!="" and cz.upper()!="blank line".upper():
                row_labels_and_row_data.append(lines[i])
                last_line=i
                #for item in row_labels_and_row_data:
                #    print i,item
            else:
                last_line=i-1
                break
        except:
            last_line=i-1
            break
##    print "lines"    
##    print lines
##    print "blank and col labels"
##    print blank_and_col_labels
    #print "row labels and row data"
    #print row_labels_and_row_data
    nrow=last_line
    print "nrow=",nrow,"ncol=",ncol

    if intended_nrow and intended_ncol:
        if nrow!=intended_nrow or ncol!=intended_ncol:
            print "The numbers of rows and columns specified in"
            print "the setup file,",intended_nrow,"and",intended_ncol
            print "do not match what has been interpreted to be in the file"
            print "found",nrow,"and",ncol
            print "Please fix either the setup or the csv file."
            raw_input("(Press Return to exit)")
            sys.exit()
    
    #copy notes, if any, from the end of the file
    notes=""    
    for i in range(last_line+1,len(lines)):
        notes+=lines[i][0].strip()+"\n"
    print "Notes A:"
    print notes
        

    w=fn.find(".csv")
    if w<=0:
        print "File problems with file <"+fn+">"
        print "The file must be in csv format (comma separated value format)"
        print "and it's name must use '.csv' as the last 4 characters of"
        print "the name"
        raw_input("(Press 'return' to exit)")
        sys.exit()
    else:
        outfn=fn[:w]+".txt"

    outf=open(outfn,"w")
    eol="\n"
    stuff=""
    stuff+=str(nrow)+eol
    stuff+=str(ncol)+eol
    for row in xrange(len(row_labels_and_row_data)):
        r=row_labels_and_row_data[row]
        s=str(r[1]).strip()   #first number is in 2nd position (after a row label)
        for j in xrange(1,ncol):
            s+=","+str(r[j+1])
        stuff+=s+eol
    for i in xrange(nrow):
        stuff+=row_labels_and_row_data[i][0]+eol
    for j in xrange(ncol):
        stuff+=blank_and_col_labels[j+1]+eol
    outf.write(stuff)
    outf.close
    return outfn
    

def face_column_speed_ratios(fn):
    nrow,ncol,data,rlab,clab=read_face_array(fn)
    new_clab=[]
    #Due to pre-screening, all these entries should be prices, no zeroes
    #no missing data.  Assume columns are dated, in order.  Speed ratio is column
    #to column ratio.

    ratio_data=zeros((nrow,ncol-1),float)

    for col in xrange(1,ncol):
        new_clab.append(clab[col]+"-"+clab[col-1])
        for row in xrange (nrow):
            ratio_data[row,col-1]=data[row,col]/data[row,col-1]

    if "." in fn:
        i = fn.index(".")
        outfn=fn[:i]+"r"+fn[i:]
    else:    
        outfn=fn+"r"
    outf=open(outfn,"w")
    eol="\n"
    line=str(nrow)+eol
    line+=str(ncol-1)+eol
    for row in range(nrow):
        line+=str(ratio_data[row,0])
        for col in range(1,ncol-1):
            line+=","+str(ratio_data[row,col])
        line+=eol
    for row in rlab:
        line+=str(row)+eol
    for col in new_clab:
        line+=str(col)+eol
    outf.write(line)    
    outf.close()              
    return outfn   

            

def read_face_array(root):
        print "in 'read_face_array', root=",root
        inf=open(root,"r")
        stuff=inf.readlines()
        print "debug.  It has length ",len(stuff)
        if len(stuff)==1:
                #print stuff
                stuff=stuff[0].split("\r")
        for i in range(len(stuff)):
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

