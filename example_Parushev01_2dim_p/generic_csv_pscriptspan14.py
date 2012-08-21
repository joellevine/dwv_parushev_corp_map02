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

# generic_csv_pscriptspan08.py  try multiprocessing  or maybe just os
#Known bugs:
# 1/2/12
# In some instances it is not filing its current best file or best spread sheet.
# I'v only seen this when I was doing a debugging run with a single semi-start
# and only 2 iterations.  When I reset the number of iterations to 2000 it disappeared.



#05  Add Correspondence Analysis option NOT CURRENTLY IMPLIMENTED

#print "left with at least two problems -- fix nibble_e"
#print "why is the line of output keeping track != 972 (972 is lawyer but also stalls out -- gets too large on new pass"#


#! /usr/bin/python
#================================================D

# The 'program' in this python file begins near the
# middle of this file.  (The top of the file supplies
# specifications required by the program.)

#==============================================



from tkFileDialog import askopenfilename
import sys,os,time,shutil

#The following python code can hide output directed
#to the screen.  It is intended to assist web/navigator-
#based use.  It is presumed that the web page version
#will provide substitutes for this discourse.

#out_junk=open('screen_discard',"w")
#sys.stdout=out_junk

#To turn it on again, the python code would be (with double under-scores)
#sys.stdout=__stdout__

use_log_price_change=False #unless over-ridden by setup

def read_faceA(fn):
    inf=open(fn)
    lines=inf.readlines()

 
    nrow=int(lines[0])
    ncol=int(lines[1])
    where=1
    
    a=zeros((nrow,ncol),float)
    rlab=[]
    clab=[]

    for i in xrange(nrow):
        where+=1
        stuff=lines[where].strip()
        stuff=stuff.split(",")
        a[i,:]=array(stuff)[:]
    for i in xrange(nrow):
        where+=1
        rlab.append(lines[where].strip())
    for j in xrange(ncol):
        where+=1
        clab.append(lines[where].strip())

    return a,rlab,clab       
                    
             
def read_setup_commands():
    ans="N"
    while ans!="Y":
        if debugging_run:
            #fn="/Users/joellevine/names/Eric Warren/DwV_and_Goldfarb Group 080826/DwV_and_Goldfarb/Goldfarb080822/run080823/setup_goldfarb.txt"
            fn="/Users/joellevine/Desktop/joellevine/Applications/DwVApplications 111210linfcn/Data_ProjectsJL/generic_csv_dwv_folder Greenacre1/HtWt1D/generic_csv_setup.txt"
        else:        
            fn=askopenfilename(title="Navigate to appropriate __setup.txt file.",initialdir=os.getcwd())
        if "SETUP" not in fn.upper():
            print "Are you sure?  The file you named,"+fn+" does not include the word 'setup'."
            print "Yes (continue) or No (try again)"
            ans=raw_input("Y or N").strip().upper()[0]
            if ans=="Y": break
        else:
            ans="Y"
        
            


    inf=open(fn,"rg")
    lines=inf.readlines()

    usable_lines=[]
    for lin in lines:
        a=lin.strip()
        if len(a)>0 and "=" in a:        
            if a[0]!="#":
                i= a.find("#")
                if i>0:  a=a[:i]                
                usable_lines.append(a)

        
    setup_commands={}            
    for lin in usable_lines:
        i=lin.find("=")
        setup_commands[lin[:i].strip()]=lin[i+1:].strip()
    s=fn.rfind("/")    
    setup_commands["folder_containing_setup"]=fn[:s].strip()

    #New special case:  For 'emphasis' the set up file has a text names separated by commas.
    #I want a list.
    if "emphasis" in setup_commands:
        lisstr=setup_commands['emphasis']
        setup_commands['emphasis']=lisstr.split(",")
        

##    if "run_name" not in setup_commands:
##        run_name=setup_commands["data_table"]
##        i=run_name.find(".csv")
##        setup_commands["run_name"]=run_name[:i].strip()

    ke=setup_commands.keys()
    ke.sort()

    print "Specified by setup file:  "+fn
    for k in ke:
        print "    "+str(k)+"="+str(setup_commands[k])
    print
    return setup_commands


def get_dwv_folder():

    #The dwv_folder is the current library of dwv_software
    #Because I do not know its absolute address, I need to find it                          


    
    initialdir=os.getcwd()
    
        #If we are running on export the dwv (and drawing)
        #should be right here in the same folder
    if os.path.exists(initialdir+"/dwvC107.py"):
        dwv_folder=initialdir
    else:    
        #print "Keeping track  cwd is <"+initialdir+">"
        if "/Applications/DwVApp" not in initialdir:
            print "\n\nProblem coordinating file structures."
            print "search string not present in name of initial directory"
            raw_input("Needs attention\n\n")
        where=initialdir.find("/DwVApp")
        dwv_folder=initialdir[:where]+"/DwVApplications 120619linfcn/software"
    

    
    #raw_input("")
    #raw_input("dir:"+dwv_folder)

    #dwv_folder="/Users/joellevine/Applications/DwVApplications 081112/software"

    #print initialdir
    #print dwv_folder
    #raw_input("in pscript, working on path")
    return dwv_folder

def create_output_folder(c_dict):
    print "find current folder where data are"
    data_file=c_dict["data_table"]
    print "\ndata_file",data_file,"\n"
    
    where=data_file.rfind("/")
    data_dir=data_file[0:where]
    data_root=data_file[where+1:]
    print "\ndata_file",data_file,"\n"
    print "\ndata_dir",data_dir,"\n"
    print "\ndata_root",data_root,"\n"

    #build a folder corresponding to the model, and the values or starting
    #values of data_file (without suffix), ndim, minkowski, attenuation, use_diagonal
    #nudge,

    #e.g.
    #glass7X7_i_2d_M1.5_a1.5_s.2
    
    f="mod_form_"+c_dict["mod_form"]
    f+="_"+str(c_dict["ndim"])+"dim"
    #print "f=",f
    copy_number=1
    new_dir_root=data_dir+"/"+f
    new_dir=new_dir_root+"_job_"+str(copy_number)
    #print "\nnew_dir",new_dir
    while os.path.exists(new_dir):
        print "this exists already:  ",new_dir
        print
        copy_number+=1
        #print "copy_number",copy_number
        new_dir=new_dir_root+"_job_"+str(copy_number)
        #raw_input("is it ready to make anything?")
    #raw_input( "\nready to make:  "+new_dir   ) 
    os.makedirs(new_dir)
    print "\nmaking new directory",new_dir
    #print
    #print "\n existing data file:  ",data_file
    #print "\nnew_dir",new_dir
    new_data_file=new_dir+'/'+data_root
    #print
    #print "new_data_file"
    #print new_data_file
    #raw_input("\nis that what I wanted?")
    shutil.copy(data_file, new_data_file)
    #raw_input("\n Did the file get copied into the subfolder?")
    

    """
shutil.copy(src, dst)
Copy the file src to the file or directory dst.
If dst is a directory, a file with the same basename
as src is created (or overwritten) in the directory
specified. Permission bits are copied. src and dst are
path names given as strings.

should I copy the data file in this routine (Let dwv print a file version of
c_dict into the directory.  HOw do I do a continuation run?  Do I want
to have a command to turn on or turn off the use of sub directories -- when I tell
it to continue and identify the data file and solution in a subdirectory?
If so, I should copy the SETUP file in there too.

"""
    return new_data_file  #embed into cdict of a child process    
        
    

def decode_users_instructions(fn):
    inf=open(fn,"r")
    lines=inf.readlines()
    keepers=[]
    for line in lines:
        lin=line.strip()
        if len(lin)>0:
            if lin[0]!="#":
                if lin.find("#")>0: #get rid of any comments
                    wh=lin.find("#")
                    lin=lin[:wh].strip()
                keepers.append(lin)

    command_dictionary={}
    for keeper in keepers:
        w=keeper.find("=")
        if w<0:
            print "\nCan not read command, no equal sign, in:"
            print keeper
            print
        else:
            command=keeper[:w].strip().lower()
            v=keeper[w+1:].strip().lower()
            if v.upper()=="TRUE":v="True"
            try:
                v2=float(v)
                v=v2
            except:
                pass
            command_dictionary[command]=v
    return command_dictionary
    
        
#==============================================================
#
#     Begin Program
#
#==============================================================

print
print "="*20+time.ctime()+"="*20
print 

########
#    Select "do mode" #####
########

#to do list:
print
ans=""
while ans!=1 and ans!=2:
    ans=int(raw_input( "Complete run, '1', or Graphics from previous run, '2'?  Enter 1 or 2:  "))
    print "ans",ans,type(ans)
    if ans==1:
        print "a"
        job="complete"
    if ans==2:
        print "b"
        job="graphics_only"
    print "ans",ans,"job",job    
        
print "stock_pscript currently specifies: ",job
if job=="complete":
	do_extract_change=False

	do_coordinate_extraction=True
	#do_coordinate_extraction=False

	do_graphics=True
	debugging_run=False
else:  #graphics only
	do_extract_change=True

	#do_coordinate_extraction=True
	do_coordinate_extraction=False

	do_graphics=True
	debugging_run=False


#Find setup file, read it, and identify the folder it is in
c_dict=read_setup_commands()

#Find the principal software
#print "debug  calling get_dwv_folder"
#raw_input("debug")
dwv_folder=get_dwv_folder()


#Allow the program to access that software
###### --  Somehow I changed code on the unix such
###### --  that it became platform independent
sys.path.append(dwv_folder+"/"+"dwv_software_080822"+"/"+"dwv_software_reserved")
#sys.path.append(dwv_folder+"/"+"dwv_software_080822"+"/"+"dwv_stk_software_reserved")

#print "path appended with",dwv_folder+"/"+"dwv_software_080822"+"/"+"dwv_software_reserved"
#raw_input("check path")
#print

use_TextData=False
use_csv=True
# not written:  use_face_format

if use_TextData:
    import TextData_mat05   
    if do_coordinate_extraction:  #Data format for a special application.
        mat_file_name,nrow,ncol=TextData_mat05.TextData_mat04(add_constant_plus=False)
        #mat_file_name,nrow,ncol=TextData_mat04.TextData_mat04(add_constant_plus=False)
        c_dict['data_table']=mat_file_name
        c_dict['nrow']=nrow #str(nrow)
        c_dict['ncol']=ncol #str(ncol)
    else:
        mat_file_name=askopenfilename(title="To continue from previous solution,Navigate to face-format rootmatrix.txt file.",initialdir=os.getcwd())
        print "Received:  ",mat_file_name
        #because the program wrote the file, I can assume a standard format for its name
        #I can extract nrow and ncol from that name:
        dt=mat_file_name.rfind(".txt")
        piece=mat_file_name[:dt]
        rt=piece
        xx=piece.rfind("x")
        ncol=int(piece[xx+1:])
        piece=piece[:xx]
        u=piece.rfind("_")
        nrow=int(piece[u+1:])
        print "inferred:  nrow=",nrow," ncol=",ncol
        c_dict['data_table']=mat_file_name
        c_dict['run_name']=rt
        c_dict['nrow']=nrow
        c_dict['ncol']=ncol

if use_csv:
    if do_coordinate_extraction:
        if debugging_run:
            c_dict['data_table']="/Users/joellevine/Desktop/joellevine/Applications/DwVApplications 091030linfcn/Data_ProjectsJL/generic_csv_dwv_folder Greenacre1/HtWt1D/HtWt4 32x11for htwtcorrelation.csv"
        else:    
            c_dict['data_table']=askopenfilename(title="Navigate to a .csv file (Usually from an Excel file using SAVE AS .csv)",
                                              initialdir=os.getcwd())
            #raw_input("284 "+str(c_dict['data_table']))   #debugging
        if ".csv" not in c_dict['data_table']:
            raw_input("Are you sure of the name:  text '.csv' is not part of the name.  Press RETURN to continue regardless")
    else:
        mat_file_name=askopenfilename(title="To continue from previous solution,Navigate to face-format rootmatrix.txt file.",initialdir=os.getcwd())
        print "Received:  ",mat_file_name
        #because the program wrote the file, I can assume a standard format for its name
        #I can extract nrow and ncol from that name:
        dt=mat_file_name.rfind(".txt")
        piece=mat_file_name[:dt]
        rt=piece
        xx=piece.rfind("x")
        ncol=int(piece[xx+1:])
        piece=piece[:xx]
        u=piece.rfind("_")
        nrow=int(piece[u+1:])
        print "inferred:  nrow=",nrow," ncol=",ncol
        c_dict['data_table']=mat_file_name
        c_dict['run_name']=rt
        c_dict['nrow']=nrow
        c_dict['ncol']=ncol
        

##print "debug c_dict"
##print c_dict
##raw_input("")
if 'draw_lines' in c_dict:
    if c_dict['draw_lines']=="False":
        c_dict['draw_lines']=False
else:
    c_dict['draw_lines']=True

if "draw_column_sequence" not in c_dict:
    c_dict["draw_column_sequence"]=False
    
if c_dict['max_passes_for_run']:
    c_dict['max_passes_for_run']=int(c_dict['max_passes_for_run']) #Kludge should be in decode
else:
    c_dict['max_passes_for_run']=1000
    
if 'minkowski_power' in c_dict:
    try:
        num=float(c_dict["minkowski_power"])
        c_dict['minkowski_power']=num
        c_dict['minkowski_start_list']=[num]
        minkowski_start_list=[num]
    except:
        try:
            num_tuple=eval(c_dict["minkowski_power"])
            c_dict['minkowski_power']=num_tuple
            minkowski_power_start_list=num_tuple
        except:    
            print "unreadable entry for minkowski power:"
            print "A number or a comma-separated set of numbers was expected "
            print c_dict['minkowski_power'],type(c_dict['minkowski_power'])
            raw_input("stopped at 374") 
else:    
    c_dict['minkowski_power']=1
    c_dict['minkowski_power_start_list']=[1]

if 'attenuation_power' in c_dict:
    try:
        num=float(c_dict["attenuation_power"])
        c_dict['attenuation_power']=num
        c_dict['attenuation_power_start_list']=[num]
        attenuation_start_list=[num]
    except:
        try:
            num_tuple=eval(c_dict["attenuation_power"])
            c_dict['attenuation_power']=num_tuple
            attenuation_power_start_list=num_tuple
        except:    
            print "unreadable entry for attenuation power:"
            print "A number or a comma-separated set of numbers was expected "
            print c_dict['attenuation_power'],type(c_dict['attenuation_power'])
            raw_input("stopped at 392")
else:            
    c_dict['attenuation_power']=1
    c_dict['attenuation_power_start_list']=[1]

print "current contents of command dictionary c_dict"
ite=c_dict.keys()
ite.sort()
for ite in c_dict:
    print "Control: ",ite,"\t",c_dict[ite]
#raw_input("")
    
if 'd_start' in c_dict:
    #print "392",c_dict['d_start'],type(c_dict['d_start'])
    #raw_input("")
                       
    try:
        num=float(c_dict["d_start"])
        c_dict['d_start']=num
        c_dict['d_start_start_list']=[num]
        d_start_start_list=[num]
    except:
        try:
            num_tuple=eval(c_dict["d_start"])
            c_dict['d_start']=num_tuple
            d_start_start_list=num_tuple
        except:    
            print "unreadable entry for d_start:"
            print "A number or a comma-separated set of numbers was expected "
            print c_dict['d_start'],type(c_dict['d_start'])
            raw_input("stopped at 419")
            
else:    
    c_dict['d_start']=0
    c_dict['d_start_start_list']=[0]

if 'n_semi_starts' in c_dict:
    c_dict['n_semi_starts']=int(c_dict['n_semi_starts'])

comment=""
if "nrow" not in c_dict:
    comment="Please specify the number of rows, 'nrow', in the setup file\n"
else:
    c_dict['nrow']=int(c_dict['nrow'])    
if "ncol" not in c_dict:
    comment+="Please specify the number of columns, 'ncol' in the setup file"
else:
    c_dict['ncol']=int(c_dict['ncol'])    
if len(comment)>0:
    print
    print comment
    raw_input("(Press 'return' to exit from the program.)")
    sys.exit()

if "ndim" in c_dict:
    c_dict["ndim"]=int(c_dict["ndim"])
else:
    c_dict["ndim"]=2

if "use_diagonal" in c_dict:
    if c_dict['use_diagonal'].upper()=="False".upper():
        c_dict['use_diagonal']=False
    else:
        c_dict['use_diagonal']=True
else:
    c_dict['use_diagonal']=True

if "last_column_gt_first_column" in c_dict:        
    if c_dict['last_column_gt_first_column'].upper()=="False".upper():
        c_dict['last_column_gt_first_column']=False
    else:
        c_dict['last_column_gt_first_column']=True
else:
    c_dict['last_column_gt_first_column']=False

if "nudge_columns_toward_labelled_sequence" in c_dict:
    if c_dict['nudge_columns_toward_labelled_sequence_during_startup'].upper()=="True".upper():
        c_dict['nudge_columns_toward_labelled_sequence_during_startup']=True
    else:    
        c_dict['nudge_columns_toward_labelled_sequence_during_startup']=False
else:        
    c_dict['nudge_columns_toward_labelled_sequence_during_startup']=False

if "omission_value" in c_dict:
    omission_value=c_dict["omission_value"]
else:
    omission_value=""
    c_dict["omission_value"]=omission_value

if "mod_form" in c_dict:
    mod_form=c_dict["mod_form"]
else:
    mod_form="p"  #standard dwv powered_normal
    c_dict["mod_form"]=mod_form

if "continuation_or_startup" in c_dict:
    continuation_or_startup=c_dict["continuation_or_startup"]
else:
    print "\n continuation_or_startup command was omitted from the SETUP fiie"
    print "Program will assume continuation_or_startup=startup"
    continuation_or_startup="startup"
    c_dict["continuation_or_startup"]="startup"

##for ite in c_dict:
##    print "478",ite,c_dict[ite]
##raw_input("479")    
##if "d_start" in c_dict:
##    d_start=float(c_dict["d_start"])
##else:
##    d_start=False  #standard dwv powered_normal
##    c_dict["d_start"]=float(d_start)

if "opt_attenuation" in c_dict:        
    if c_dict['opt_attenuation'].upper()=="False".upper():
        c_dict['opt_attenuation']=False
    else:
        c_dict['opt_attenuation']=True
else:
    c_dict['opt_attenuation']=False
    
if "opt_minkowski" in c_dict:        
    if c_dict['opt_minkowski'].upper()=="False".upper():
        c_dict['opt_minkowski']=False
    else:
        c_dict['opt_minkowski']=True
else:
    c_dict['opt_minkowski']=False
        
if "opt_d_start" in c_dict:        
    if c_dict['opt_d_start'].upper()=="False".upper():
        c_dict['opt_d_start']=False
    else:
        c_dict['opt_d_start']=True
else:
    c_dict['opt_d_start']=False
    

#for data table in csv format, it must be read, converted to face
#format, and filed as text file.

#print "in pscript, c_dict['draw_column_sequence']=",c_dict['draw_column_sequence']
#raw_input("check at aba in csv_pscript")

        
from read_csv_lines import *
if do_coordinate_extraction:
#raw_input("aaa")
    c_dict['data_table']=csv_face(c_dict['data_table'])
    #if use_change_as_primary_data:
    #    c_dict['data_table']=column_to_column_change(d_dict['data_table'])
    #    this reduces ncol by 1 (if it is already set.)
    #    need new output which is simply predicted change (for each stock) on last
    #    or project next day of squence

if use_log_price_change:
    if do_extract_change:  #not as primary data but as marker for rising
        # and falling most-recent prices.

        # Try moving most of this into the set-up file.
        
        if use_log_price_change:
            from ln_price_change import *
        #move the next two lines to set-up file/Users/joellevine/Applications/DwVApplications 090210HanMiss3/Data_ProjectsJL/SP-500 510 7584 post export02/category lists/dividend paying/CleanEdgeEnergyIdxComponents.txt
        early_yyyymmdd="20090424"  #'by hand', select from table_dates
        current_yyyymmdd=  "20090724"         #  ditto

        if current_yyyymmdd<=early_yyyymmdd:
            print "probable error:  The 'early' date is later than the 'late' date"
            raw_input("check early late specifications in _pscript.py file")

        print
        print "Programmed in _pscript to use "
        print "current_yyyymmdd=",current_yyyymmdd
        print "early_yyyymmdd=",early_yyyymmdd
        print
        ln_price_change=ln_price_change(early_yyyymmdd,current_yyyymmdd,c_dict['data_table'])
else:
    ln_price_change=False

if do_coordinate_extraction:

    #dwv034 was being used for single runs, 035 for batch run of simple corporate
    #maps.  It had already been organized for a simple call, sending "" (null recognized
    #as "self", presumably related to the previous coordinateion with a GUI,
    #plus a dictionary of commands

    mod_type=c_dict['mod_type']

    #import dwvB041  #even if not using dwv, I'm using 'check_and_read_face_array' -- should pull into separate module
    if mod_type.upper()!="CORRESPONDENCE ANALYSIS" and mod_type.upper()!="CORRESPONDENCE_ANALYSIS":
        # Compute Coordinates
        #import dwvB036
        #import dwvB037Shuffling2
        #print "debug path at 515:"
        #for ite in sys.path:
        #    print ite
        #import dwvC103 #101 fixes a d_start bug;dropping back to B041, and renaming it C100
        import dwvC107 #101 fixes a d_start bug;dropping back to B041, and renaming it C100
        # dwvC103 was probably created but never changed.  For safety
        # experiment in C104:  file output in folders corresponding
        # to starting configuration.
        #import dwvC103 #101 fixes a d_start bug;dropping back to B041, and renaming it C100
        import dwvC107 #101 fixes a d_start bug;dropping back to B041, and renaming it C100
        #import dwvB042display
        # Graphics -- import graphics now.  During the process of computing
        # coordinates, dwv can entertain by showing them and updating them on the screen.
        import rectangle_driver007inprocess
        #import rectangle_stock_plot007  #replacement in process, specifically for stocks (on generic plot stuff), allows swapping labels

        #import rectangle_driver006wocanvasglobal

        if "omission_value" not in c_dict:
            if "omission_code" in c_dict:
                print
                print "Check setup for spelling.  The program uses"
                print " 'omission_value' .  Your file uses the incorrect name"
                print " 'omission_code'"

        #dwvB037Shuffling2.dwv_entry(root=c_dict["data_table"],
        #raw_input(c_dict["mod_form"])
        collected_results=[]

        #Two ways to start the loop:
    ##    for item in [[2,2]]:
    ##        minkowski,attenuation=item
    ##        if 1==1:



        if type(c_dict['minkowski_power'])==float or type(c_dict['attenuation_power'])==int:
            c_dict['minkowski_power']=[c_dict['minkowski_power']] #make it a list of one item
        minkowski_value_list=list(c_dict['minkowski_power'])
        c_dict['minkowski_value_list']=minkowski_value_list #for consistency of making things available

        if 0 in minkowski_value_list or 0. in minkowski_value_list:
            print "The SETUP file includes an unacceptable zero among the minkowski values."
            print minkowski_value_list
            print "Please correct the SETUP file."            
            test_value=1./0

            
        if type(c_dict['attenuation_power'])==float or type(c_dict['attenuation_power'])==int:
            c_dict['attenuation_power']=[c_dict['attenuation_power']] #make it a list of one item
        attenuation_power_list=c_dict["attenuation_power"] #attenuation power will be rewritten in a loop   
        c_dict['attenuation_power_list']=attenuation_power_list 

        if 0 in attenuation_power_list or 0. in attenuation_power_list:
            print "The SETUP file includes an unacceptable zero among the attenuation power values."
            print attenuation_power_list
            print "Please correct the SETUP file."            
            test_value=1./0


        if type(c_dict['d_start'])==float or type(c_dict['d_start'])==int:
            c_dict['d_start']=[c_dict['d_start']] #make it a list of one item
        d_start_list=c_dict['d_start'] #often this was only a number.  Make it a list of length 1
        c_dict['d_start_list']=d_start_list
        
   
        best_of_scanned=999999999.999  #keep track in order to save (and re-start) least error output among those scaned
        
        for minkowski in minkowski_value_list: #[2]: #,2.25,2.5]:
            #for attenuation in [4,5,6,8,10]:
            for attenuation in attenuation_power_list: # [.97,.98,.99,1.01,1.02,1.03,1]:
            #for attenuation in [1.22]:
                #Should build a copy of c_dict so that it
                #can be refreshed during a restart.
                c_dict['minkowski_power']=minkowski
                c_dict['attenuation_power']=attenuation
                print "generic line 728"
                for d_start in d_start_list: #[0]: #.75,1,1.25,1.5,1.75,2]:
                    c_dict['d_start']=d_start
                    saved_data_table_name=c_dict["data_table"]+""
                    new_data_table=create_output_folder(c_dict)

##                    for kk in range(2):
##                        print kk
##                        os.system("python do_something.py")
##                    raw_input("line 737 is anything running")    

                    

                    ### restore this immediately after calling the fcn
                    c_dict["data_table"]=new_data_table
                    ### restore this immediately after calling the fcn
                    print "generic line 737"

                    
                    # dwvC103.dwv_entry(root=c_dict["data_table"],
                              
                    [least_err2,c,re,ce,rx,cx]=  \
                     dwvC107.dwv_entry(root=c_dict["data_table"],
                      nrow=c_dict["nrow"],
                      ncol=c_dict["ncol"],
                      ndim=c_dict["ndim"],
                      mod_type=c_dict["mod_type"], #"rectangular",
                      attenuation_power=c_dict['attenuation_power'],
                      minkowski_power=c_dict['minkowski_power'],
                      use_stand=False,
                      nlayer=1,
                      erf="chi_square",
                      continuation_or_startup=c_dict["continuation_or_startup"], #"startup", #"continuation",
                      max_passes_for_run=c_dict['max_passes_for_run'],
                      use_diagonal=c_dict['use_diagonal'],
                      draw_lines=c_dict['draw_lines'],
                      icons=False,
                      nudge_columns_toward_labelled_sequence_during_startup=c_dict['nudge_columns_toward_labelled_sequence_during_startup'],                   
                      row_heights=ln_price_change, #get          
                      draw_column_sequence=c_dict['draw_column_sequence'], #) #,
                      last_column_gt_first_column=c_dict['last_column_gt_first_column'],                   
                      font=("Times",10),
                      n_semi_starts=int(c_dict["n_semi_starts"]),   #Tkinter default font-tuple is ("Helvetica", 12, "normal")
                      omission_value=c_dict["omission_value"],
                      mod_form=c_dict["mod_form"],
                      d_start=float(c_dict["d_start"]),
                      opt_attenuation=c_dict["opt_attenuation"],
                      opt_minkowski=c_dict["opt_minkowski"],
                      opt_d_start=c_dict["opt_d_start"],
                      best_of_scanned=best_of_scanned)


                    ### restoring
                    c_dict["data_table"]=saved_data_table_name
                    ### restoring
        

                    if least_err2<best_of_scanned:  best_of_scanned=least_err2  #should have used c (which returns the best_of_scanned)
                    
                    collected_results.append([minkowski,attenuation,d_start,least_err2,c,re,ce,rx,cx])
                    #take a peek:
                    print "."*80
                    peek=open(c_dict["data_table"]+"_scan.txt","w")
                    line=""
                    for item in collected_results:
                        line +="Start: minkowski: %6.2f    attenuation %6.2f  d_start %6.3f  Reach:  error %12.2f"%(item[0],item[1],item[2],item[3])
                        line +="minkowski:  %6.2f    attenuation  %6.2f"%(minkowski,attenuation)
                        line +="  best_of_scanned:  %6.2f"%(best_of_scanned)
                        line +="\n"
                        
                        #line="minkowski:  "+str(item[0])+"  attenuation:  "+str(item[1])+"  error:  "+str(item[2])
                    print line
                    peek.write(line)
                    peek.close()
                    print "."*80
                    #raw_input("should have file in 'span'")
                    
    elif mod_type.upper()=="CORRESPONDENCE ANALYSIS" or mod_type.upper()=="CORRESPONDENCE_ANALYSIS":
        import correspondence_analysis005a
        #print c_dict['data_table']
        ob,rlab,clab=read_faceA(c_dict['data_table'])
        print "..............."
        print c_dict['data_table']
        print "---------------"
        outf=open(c_dict['data_table']+"a","w")
        nrow=len(rlab)
        obLL=[]
        for row in xrange(nrow):
            obLL.append(list(ob[row,:]))
        #print obLL
        standard_coordinates_of_rows,\
           standard_coordinates_of_columns,\
           singular_values,\
           array_chi_by_dim,\
           chi_by_dim_lines=\
               correspondence_analysis005a.correspondence_analysis01(obLL,rlab=rlab,clab=clab)
        rx=standard_coordinates_of_rows
        cx=standard_coordinates_of_columns
        line=""  #mimic the 'a' file that is read by the graphics
        line+="row_coordinates\n"  #I don't like having a non specific output
        line+=str(len(rlab))+"\n"
        line+="2\n"
        for ri in xrange(len(rlab)):
            for di in xrange(2):
                line+=str(rx[ri,di])+",\n"
        line+="col_coordinates\n"  #I don't like having a non specific output
        line+=str(len(clab))+"\n"
        line+="2\n"
        for cj in xrange(len(clab)):
            for di in xrange(2):
                line+=str(cx[cj,di])+",\n"
        outf.write(line)
        outf.close()
                  
                                   #that overwrites other output, but today
        for item in chi_by_dim_lines:  #is not the day to modify the graphics program to be more clever
               print item           #about file opening
        #print 'erf',c['erf']    
        #raw_input("601")

        
#    if c_dict['erf']=="chi_square":
#
#        raw_input("debug at 568")
        

    else:
        print "\nmod_type= <"+str(mod_type).upper()+">  mod_type not recognized at line 571."
        print "Please check the specification of mod_type in the setup file."
        raw_input("Press any key to exit")
        exit()
            

if do_graphics:

    print "\n\ninvoking filed graphics "+">"*30+"\n"

    # Graphics  rectangle_driver007inprocess.py
    #import rectangle_driver007inprocess #add option to draw level curve contours
    import rectangle_stock_plot007 #replacement specifically for stocks (on generic plot stuff), allows swapping labels
    #import rectangle_driver006inprocess
    #import rectangle_driver006wocanvasglobal
    #raw_input("pscript_AAA")
    if 'run_name' in c_dict: #['run_name']!="":
            #print "pscript_aaa1"
            #mat_file_name=run_folder+"/"+c_dict['run_name']+"mat"
            mat_file_name=c_dict['run_name']+"mat"
    else:
            #print "pscript_aaa2"
            #mat_file_name=fname+"mat"
            mat_file_name="mat"

    pairs_to_draw=[]
    if c_dict['ndim']==1:
        pairs_to_draw=[[0,0]]  #drawn on screen DURING the run
    else:
        pairs_to_draw=[[0,1]]

    #Standard:
    c_dict['swap_row_labels']=False
    #stk
    #c_dict['swap_row_labels']="combined"  #options:  Default:  name; Other:  False, sic, major_sic,minor_sic,combined   
    #c_dict['swap_row_labels']="name"  #options:  Default:  name; Other:  False, sic, major_sic,minor_sic,combined   
    #c_dict['swap_row_labels']="major_sic_name"  #options:  Default:  name; Other:  False, sic, major_sic,minor_sic,combined,major_sic_name   
    #print "c_dict:"
    #print c_dict
    #print "pscript aaa3 ready to call rectangle_stock_plot007"
    #( "calling rectangle at 424 in pscript")
    rectangle_stock_plot007.rectangle_driver_entry(c_dict,root=c_dict['data_table'],
                text_color_file_name="MHMH colors.txt",
                color_from_bracket=False,  #(search for colors within text enclosed in <  and > brackets
                color_from_name=True,   #(search for colors associated with a direct match to the name)
                square_table=False,
                icons=False,
                draw_lines=c_dict["draw_lines"],
                line_color='grey',         #Change to suit.  Follow color guide at top of this program file. 
                display_ndim=2,
                pairs_to_draw=pairs_to_draw, #[[0,1]],    #Select pairs of dimensions to be plotted (i.e., not all pairs)
                                            #of commands
                pause_between_drawings=c_dict["pause_between_drawings"],
                clean_up=False,
                row_heights=ln_price_change, #if false, get graphics to ignore
                draw_column_sequence=False,
                #font=("height", 1) )   #Tkinter default font-tuple is ("Helvetica", 12, "normal")
                font=("Times",12) )
                                                        
    print "\n\nGraphics filing complete  "+"<"*30+"\n"


#On a Linux/Unix machine this should translate the .ps file to a .jpg file
#I haven't tested it.  (On Mac/Unix -- the required program runs but does not wor.
#It appears to be unable to find its body parts.  They may not be installed.

try:
    command="convert "+matfile_name+".ps "+matfile_name+".jpg"
    os.system(command)
except:
    pass
    
raw_input("Press RETURN to exit and clear graphics from the screen.")

# Could do campaign speeches (& coverage, talking heads in real time
# with Seth style fequency changes and Bruce Duncan/student software.

#have something pick up the matrix and rewrite it in csv format (or make it
#an optional additional output from wordcount

#can modify Goldfarb form for whole texts (by document, by paragraph, by folder,ArithmeticError
#by document labelled with folder and document.

#could also do a subset extractor, planned for corps but usable elsewhere
# ... similar connected subset extractor.
#could also do a cross-tab, attribute thing, for Brian or Michigan

#dwvBxxx(mat_name,ndim,attenuation,metric

#rectangle graphics mat_name
#huge graphics (intended for pdf enlargement  (This stuff could replace templates

#graphics file_conversion jpg,sgv,eps,pdf,ai

