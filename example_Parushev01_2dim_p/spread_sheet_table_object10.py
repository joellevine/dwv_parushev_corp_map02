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


#Create an object representing locations of each table in my spread sheet
#Keep them more or less uniform.  methods will be used to put the table
#to the symbolic link file that is being created

# 07 isolate the "app" from the driver as DwV_spread_sheet_generator Dec 5, 2011
# 06 runs, Newtonian, no missing data, rectangular table.
#Joel Levine  Nov. 29, 2011

from numpy import *

class spread_sheet_sub_table(object):
    """One of several subtables of a spread sheet"""
    # Refer to template in Excel file spreadsheet_table_templaye.xlsx
    # Note, it seems to work with Open Office, not Excel (different header probably)

    sheet_title="unnamed"
    
    def __init__(self,parameters):
        self.parameters=parameters
        self.sst=""
        self.first_row=parameters["first_row"] ;first_row=self.first_row       
        self.sheet_title_at=(self.first_row,1)        
        self.subtitle_at=(first_row+2,1)
        
        self.ndim=parameters["ndim"]; ndim=self.ndim
        self.nrow=parameters["nrow"]; nrow=self.nrow
        self.ncol=parameters["ncol"]; ncol=self.ncol
        self.length=5+ndim+1+nrow+1+5+1+5

        self.rm=parameters["rm"]
        self.rx=parameters["rx"]
        self.rlab=parameters["rlab"]
        self.cm=parameters["cm"]
        self.cx=parameters["cx"]
        self.clab=parameters["clab"]
        self.observed_data=parameters["observed_data"]
        self.attenuation=parameters["attenuation_power"]
        self.minkowski=parameters["minkowski_power"]
        self.d_start=parameters["d_start"]
        self.mod_form=parameters["mod_form"]        
        
        self.rmheader_at=(first_row+5+ndim,1)
        self.rdim1header_at=(first_row+5+ndim,2)
        self.labelsheader_at=(first_row+6+ndim,3+ndim)
        self.csumsheader_at=(first_row+6+ndim+nrow+2,1+ndim+2)

        self.cmheader_at=(first_row+4,1+ndim+1)
        self.cdim1header_at=(first_row+5,1+ndim+1)

        self.rsumsheader_at=(first_row+8,3+ndim+ncol+2)
        
        self.chi_squareheader_at=(first_row+4+ndim+1+nrow+2,1)
        self.chi_square_at=(first_row+4+ndim+1+nrow+2,2)
        

        self.attenuationheader_at=(first_row+4+ndim+2+nrow+2,1)
        self.attenuation_at=      (first_row+4+ndim+2+nrow+2,2)
        
        self.minkowskiheader_at=(first_row+4+ndim+2+nrow+3,1)
        self.minkowski_at=(first_row+4+ndim+2+nrow+3,2)
        
        self.d_startheader_at=(first_row+4+ndim+2+nrow+4,1)
        self.d_start_at=(first_row+4+ndim+2+nrow+4,2)
        
        self.mod_formheader_at=(first_row+4+ndim+2+nrow+5,1)
        self.mod_form_at=(first_row+4+ndim+2+nrow+5,2)
##
##        #use same command names as in control file.  It will document the program
##        d_data_form_label_at=(first_row+5+ndim+nrow+2+3,1)
##        d_data_form_at=(first_row+5+ndim+nrow+2+3,2)

        #Data specific info
        
        self.start_rm_at=(first_row+6+ndim+1,1)  
        self.start_rx_at=(first_row+6+ndim+1,2)  
        self.start_rlab_at=(first_row+6+ndim+1,3+ndim)
        
        self.start_cm_at=(first_row+4,3+ndim+1)  
        self.start_cx_at=(first_row+5,3+ndim+1)  
        self.start_clab_at=(first_row+6+ndim,3+ndim+1)

        self.start_data_at=(first_row+6+ndim+1,1+ndim+3)
        self.start_csum_at=(first_row+5+ndim+2+nrow+1,1+ndim+3)
        self.start_rsum_at=(first_row+6+ndim+1,1+ndim+2+ncol+2)
        self.grandsum_at=(first_row+5+ndim+2+nrow+1,1+ndim+2+ncol+2)
        self.end_data_at=(self.start_data_at[0]+self.nrow-1,self.start_data_at[1]+self.ncol-1)

        self.length=5++ndim+2+nrow+2+2+3

    def spread_sheet_header(self,spread_sheet_software):
        #I only know the header for "OpenOffice".
        #For the moment, if an Excel is needed.  Open first inOpen Office and let it SAVE AS one of the Excel's
        self.sst="ID;PSCALC3\n"  #start the file; start sst

##    def set_first_row(self,first_row):  #different tables (within the spread sheet) have different first rows.
##        self.first_row=first_row
##        self.last_row=first_row+self.length-1

    def load_sheet_title(self,t):
        self.sheet_title=t
    def show_sheet_title(self):
        self.sst+='C;Y'+str(self.sheet_title_at[0])+';X'+str(self.sheet_title_at[1])+';K"'+self.sheet_title+'"\n'

    def load_subtitle(self,t):
        self.subtitle=t
    def show_subtitle(self):
        #Using "|" to break sub title into up to 4 lines.  This avoids creating a huge default width for Column A
        pieces=self.subtitle.split("|")
        for i in range(len(pieces)):
            piece=pieces[i]
            self.sst+='C;Y'+str(self.subtitle_at[0]+i)+';X'+str(self.subtitle_at[1])+';K"'+piece+'"\n'

    def show_csumsheader(self):
        self.sst+='C;Y'+str(self.csumsheader_at[0])+';X'+str(self.csumsheader_at[1])+';K"'+"Sums"+'"\n'

    def show_rmheader(self):
        self.sst+='C;Y'+str(self.rmheader_at[0])+';X'+str(self.rmheader_at[1])+';K"'+"Multiplier"+'"\n'
        
    def show_rdheader(self,dim):        
        self.sst+='C;Y'+str(self.rdim1header_at[0])+';X'+str(self.rdim1header_at[1]+dim)+';K"'+"Dim "+str(dim+1)+'"\n'
        
    def show_labelsheader(self):        
        self.sst+='C;Y'+str(self.labelsheader_at[0])+';X'+str(self.labelsheader_at[1])+';K"'+"Labels"+'"\n'
        
    def show_cmheader(self):        
        self.sst+='C;Y'+str(self.cmheader_at[0])+';X'+str(self.cmheader_at[1])+';K"'+"Multplr"+'"\n'
        
    def show_cdheader(self,dim):        
        self.sst+='C;Y'+str(self.cdim1header_at[0]+dim)+';X'+str(self.cdim1header_at[1])+';K"'+"Dim "+str(dim+1)+'"\n'

    def show_rsumsheader(self):
        self.sst+='C;Y'+str(self.rsumsheader_at[0])+';X'+str(self.rsumsheader_at[1])+';K"'+"Sums"+'"\n'
        
    def show_chi_squareheader(self):
        self.sst+='C;Y'+str(self.chi_squareheader_at[0])+';X'+str(self.chi_squareheader_at[1])+';K"'+"Chi Square"+'"\n'

## Skip this one        
##    def show_controlsheader(self):
##        self.sst+='C;Y'+str(self.controlsheader_at[0])+';X'+str(self.controlsheader_at[1])+';K"'+"Sums"+'"\n'
        
    def show_attenuationheader(self):
        self.sst+='C;Y'+str(self.attenuationheader_at[0])+';X'+str(self.attenuationheader_at[1])+';K"'+"Attenuation Power"+'"\n'
        
    def show_attenuation(self):
        self.sst+='C;Y'+str(self.attenuation_at[0])+';X'+str(self.attenuation_at[1])+';K'+str(self.attenuation)+'\n'

        
    def show_minkowskiheader(self):
        self.sst+='C;Y'+str(self.minkowskiheader_at[0])+';X'+str(self.minkowskiheader_at[1])+';K"'+"Minkowski Parameter"+'"\n'
        
    def show_minkowski(self):
        self.sst+='C;Y'+str(self.minkowski_at[0])+';X'+str(self.minkowski_at[1])+';K'+str(self.minkowski)+'\n'

        
    def show_d_startheader(self):
        self.sst+='C;Y'+str(self.d_startheader_at[0])+';X'+str(self.d_startheader_at[1])+';K"'+"d_start"+'"\n'

    def show_d_start(self):
        self.sst+='C;Y'+str(self.d_start_at[0])+';X'+str(self.d_start_at[1])+';K'+str(self.d_start)+'\n'


    def show_mod_formheader(self):
        self.sst+='C;Y'+str(self.mod_formheader_at[0])+';X'+str(self.mod_formheader_at[1])+';K"'+"mod_form"+'"\n'

    def show_mod_form(self):    
        self.sst+='C;Y'+str(self.mod_form_at[0])+';X'+str(self.mod_form_at[1])+';K"'+str(self.mod_form)+'"\n'

        
    def show_rm(self):
        rm=self.rm
        start_row,start_col=self.start_rm_at
        for i in range(self.nrow):
            self.sst+='C;Y'+str(start_row+i)+';X'+str(start_col)+';K'+str(rm[i])+'\n'
            
    def show_rlab(self):
        rlab=self.rlab
        start_row,start_col=self.start_rlab_at
        for i in range(self.nrow):
            self.sst+='C;Y'+str(start_row+i)+';X'+str(start_col)+';K"'+str(rlab[i])+'"\n'
            
    def show_rx(self):
        rx=self.rx
        start_row,start_col=self.start_rx_at
        for i in range(self.nrow):
            for d in range(self.ndim):
                self.sst+='C;Y'+str(start_row+i)+';X'+str(start_col+d)+';K'+str(rx[i,d])+'\n'
            

    def show_cm(self):
        cm=self.cm
        start_row,start_col=self.start_cm_at
        for j in range(self.ncol):
            self.sst+='C;Y'+str(start_row)+';X'+str(start_col+j)+';K'+str(cm[j])+'\n'
            
    def show_clab(self):
        clab=self.clab
        start_row,start_col=self.start_clab_at
        for j in range(self.ncol):
            self.sst+='C;Y'+str(start_row)+';X'+str(start_col+j)+';K"'+str(clab[j])+'"\n'
            
    def show_cx(self):
        cx=self.cx
        start_row,start_col=self.start_cx_at
        for j in range(self.ncol):
            for d in range(self.ndim):
                self.sst+='C;Y'+str(start_row+d)+';X'+str(start_col+j)+';K'+str(cx[j,d])+'\n'
            
    def show_observed(self):
        observed_data=self.observed_data
        start_row,start_col=self.start_data_at
        for i in range(self.nrow):
            for j in range(self.ncol):
                self.sst+='C;Y'+str(start_row+i)+';X'+str(start_col+j)+';K'+str(observed_data[i,j])+'\n'
                
    def cell_at(self,row,col):
        start_row,start_col=self.start_data_at
        at_row=start_row+row
        at_col=start_col+col
        return at_row,at_col

    def show_csum(self):
        start_row,start_col=self.start_csum_at
        data_start_row,data_start_col=self.start_data_at
        for j in range(self.ncol):
            fcn="sum("+number_letter(data_start_col+j)+str(data_start_row)
            fcn+=":"+number_letter(data_start_col+j)+str(data_start_row+self.nrow-1)+")"
            self.sst+='C;Y'+str(start_row)+';X'+str(start_col+j)+';E'+fcn+'\n'
            
    def show_rsum(self):
        start_row,start_col=self.start_rsum_at
        data_start_row,data_start_col=self.start_data_at
        for i in range(self.nrow):
            fcn="sum("+number_letter(data_start_col)+str(data_start_row+i)
            fcn+=":"+number_letter(data_start_col+self.ncol-1)+str(data_start_row+i)+")"
            self.sst+='C;Y'+str(start_row+i)+';X'+str(start_col)+';E'+fcn+'\n'
            
    def show_grandsum(self):
        start_row,start_col=self.grandsum_at
        data_start_row,data_start_col=self.start_data_at
        fcn="sum("+number_letter(data_start_col)+str(data_start_row)
        fcn+=":"+number_letter(data_start_col+self.ncol-1)+str(data_start_row+self.nrow-1)+")"
        self.sst+='C;Y'+str(start_row)+';X'+str(start_col)+';E'+fcn+'\n'

    def rm_row_at(self,row):          #stored normally
        rm_start_row,rm_start_col=self.start_rm_at
        at_row=rm_start_row+row
        at_col=rm_start_col
        return at_row,at_col

    def cm_col_at(self,col):          #store in spread sheet in transposed form
        cm_start_row,cm_start_col=self.start_cm_at
        at_row=cm_start_row
        at_col=cm_start_col+col
        return at_row,at_col
            
    def rx_rowdim_at(self,row,dim):   #stored normally
        #print 219,"row,dim",row,dim,"start_rx_at",self.start_rx_at
        #raw_input("220")
        rx_start_row,rx_start_col=self.start_rx_at
        at_row=rx_start_row+row
        at_col=rx_start_col+dim
        return at_row,at_col
    def cx_coldim_at(self,col,dim):    #stored on spread sheet in transposed form
        rx_start_row,rx_start_col=self.start_cx_at
        at_row=rx_start_row+dim
        at_col=rx_start_col+col
        return at_row,at_col
        

    def fitted_value_from(self,table1):  #instead of putting the data into sst (at data table),
        #use information from table 'table' to put formulas to the spread sheet (formulas in the location of the data table)
        #where numerical data were in a numerical array,  here get the formulas into a list of lists
        #Then modify the routine that writes the data table to sst to have it write items in the list of lists
        #to the same locations as the data table.  (in table[2] the table locations of data have become the table locations of formulas

        #build an empty list of lists as an array to formulas
        
        fitted_value=[]
        for row in range(self.nrow):
            row_list=[]
            for column in range(self.ncol):
                row_list.append([])
            fitted_value.append(row_list)

            
        #following dwvB052.py   function  def get_fitted_table_of_values

        for row in range(self.nrow):
            for col in range(self.ncol):
                pieces=[]
                d=""  #construct distance
                for dim in range(self.ndim):
                    diff=colrow(table1.rx_rowdim_at(row,dim))+"-"+colrow(table1.cx_coldim_at(col,dim))
                    abs_diff="ABS("+diff+")"
                    mink_abs_diff="("+abs_diff+")^"+colrow(table1.minkowski_at)
                    d+=mink_abs_diff
                    if dim<self.ndim-1:
                        d+="+"
                dm="("+d+")^(1./"+colrow(table1.minkowski_at)+")"  #distance
                started_d=colrow(table1.d_start_at)+"+"+dm             #started_distance
                asd="("+started_d+")^"+colrow(table1.attenuation_at)#attenuated (or 'power of') started distance
                if self.mod_form=="i": 
                    inv_asd="(1./"+asd+")"                               #inverse of power of started distance
                    fitted="abs("+colrow(table1.rm_row_at(row))+"*"+colrow(table1.cm_col_at(col))+")*"+inv_asd
                    fitted_value[row][col]=fitted
                    #this is easier to write.  check python model code carefully, Add d_start, invert, multiply
                #elif self.mod_form=="cauchy" or self.mod_form=="n_cauchy" or self.mod_form=="c":
                elif self.mod_form in ["cauchy","n_cauchy","c","started_pcauchy","started_p_cauchy"]:
                    inv_casd="(1./(1+"+asd+"))"                               #cauchy form denominator
                    fitted="abs("+colrow(table1.rm_row_at(row))+"*"+colrow(table1.cm_col_at(col))+")*"+inv_casd
                    fitted_value[row][col]=fitted
                elif self.mod_form == "p":
                    try:
                        if spread_sheet_p_warning:
                            continue
                    except:    
                        print "DwV spread sheet not yet implemented"
                        spread_sheet_p_warning=True
                        fitted_value[row][col]="x"
                else:
                    print "self.mod_form ",self.mod_form, "not recognized at line 294 in spread_sheet_table_object08.py"
                    fitted_value[row][col]="?"
                    #raw_input("line 295")   
                        
        return fitted_value

    def chi_square_form(self,table1,table2):
        #build an empty list of lists as an array to formulas
        value=[]
        for row in range(self.nrow):
            row_list=[]
            for column in range(self.ncol):
                row_list.append([])
            value.append(row_list)

        #chi_square;  Table1 is observed.  Table2 is fitted
        for row in range(self.nrow):
            for col in range(self.ncol):
                                
                obs=colrow(table1.cell_at(row,col))
                fit=colrow(table2.cell_at(row,col))
                diff=obs+"-"+fit
                sqd_diff="("+diff+")^2"
                chi="("+sqd_diff+")/("+fit+")"

                value[row][col]=chi
            
        # No need to write a formula for chi-square itself:  It is picked up by the
        # row sums and the grand sum.  But do it anyway
         
        chi_sum="sum("+colrow(self.start_data_at)+":"+colrow(self.end_data_at)+")"
        return value ,chi_sum
                
                           
    def show_table_of_formulas(self,text_as_list_of_lists):
        text=text_as_list_of_lists
        start_row,start_col=self.start_data_at
        #print "268",start_row,start_col,self.start_data_at,self.first_row
        #raw_input("269")
        for i in range(self.nrow):
            for j in range(self.ncol):
                self.sst+='C;Y'+str(start_row+i)+';X'+str(start_col+j)+';E'+str(text[i][j])+'\n'
                
    def show_chi_square(self,chi_square_formula):
        chi_square_row,chi_square_col=self.chi_square_at
        self.sst+='C;Y'+str(chi_square_row)+';X'+str(chi_square_col)+';E'+chi_square_formula+'\n'
        
        
def number_letter(n0):
    code=range(ord("A"),ord("Z")+1)
    #so count base 26 and convert

    """
    practice base 5
    1  2  3  4  5  6  7  8   9   10   11
    1  2  3  4  10 11 12 13 14   21   22

    0  1  2  3  4  10 11 12  13  14   20
    A  B  C  D  E  AA AB AC  AD  AE   BA
    """
    n=int(n0)+0  #secure copy

    base=26
    column_base=1

    digits=[]

    while n>0:
        v=(n-column_base)%(int(column_base*base))
        v/=column_base
        digits.append(v)
        n-= (v+1)*(column_base)
        column_base*=base
        
    digits.reverse()
    #print "n0 and digits",n0,digits,
    t=""
    for elt in digits:
        t+= chr(code[elt])
    return t   


def colrow((row,col)):  #write a locaton like "A2" for cell (2,1)
    return number_letter(col)+str(row)
        

def dwv_spread_sheet_generator(parameters):    
                                 
    #table_beginnings={1:1}
    table={}

    #  ##############
    #  TABLE 1: DATA TABLE, PARAMETERS, CHI-SQUARE ERROR
    #  ##############

    parameters["first_row"]=1
    

    table[1]=spread_sheet_sub_table(parameters)  #Instantiate (make an instance)
    #table[1].set_first_row(table_beginnings[1])
     
    table[1].spread_sheet_header("open_office_header")  #initialize text to be filed.
    #table[1].load_subtitle("Data")  #Table 1 is always parameters and data.
    #table[1].show_subtitle()  #Table 1 is always parameters and data.
    
    table[1].load_sheet_title("DwV SSheet (c)|Levine 2012")
    table[1].show_sheet_title()
    #use '|' to break title into up to 3 lines (Otherwise the spread gives Column A a huge margin
    table[1].load_subtitle("Data, Adjustable|Parameters,|and Chi-Square")
    table[1].show_subtitle()

    table[1].show_rmheader()
    for dim in range(parameters["ndim"]):
        table[1].show_rdheader(dim)
    #table[1].show_labelsheader()

    table[1].show_csumsheader()

    table[1].show_cmheader()
    for dim in range(parameters["ndim"]):
        table[1].show_cdheader(dim)
    table[1].show_rsumsheader()
    table[1].show_chi_squareheader()
    #skip table[1].show_controlsheader()
    table[1].show_attenuationheader()
    table[1].show_minkowskiheader()
    table[1].show_d_startheader()
    table[1].show_mod_formheader()

    #data specific
    table[1].show_rm()
    table[1].show_rx()
    table[1].show_rlab()
    table[1].show_cm()
    table[1].show_cx()
    table[1].show_clab()
    #table[1].show_data()
    table[1].show_observed()
    table[1].show_csum()
    table[1].show_rsum()
    table[1].show_grandsum()

    table[1].show_attenuation()
    table[1].show_minkowski()
    table[1].show_d_start()
    table[1].show_mod_form()
    

    #  ##############
    #  TABLE 2: fitted values
    #  ##############

    parameters['first_row']=table[1].first_row+table[1].length-1
    table[2]=spread_sheet_sub_table(parameters)  #Instantiate (make an instance)
    #use '|' to break title into up to 3 lines (Otherwise the spread gives Column A a huge margin
    table[2].load_subtitle("Fitted Values")
    table[2].show_subtitle()

    table[2].show_rlab()
    table[2].show_clab()
    #table[2].set_first_row(table[1].first_row+table[1].length-1)
    #print "table 2 first row is",table[2].first_row

    fitted_value=table[2].fitted_value_from(table[1])


    
##    for item1 in fitted_value:
##        for item2 in item1:
##            print item2
##        print

    table[2].show_table_of_formulas(fitted_value)    


    #  ##############
    #  TABLE 3: error / goodness-badness of fit
    #  ##############
   
    parameters['first_row']=table[1].first_row+2*(table[1].length)-1
    table[3]=spread_sheet_sub_table(parameters)  #Instantiate (make an instance)
    #use '|' to break title into up to 3 lines (Otherwise the spread gives Column A a huge margin
    table[3].load_subtitle("Goodness /|Badness|of Fit")
    table[3].show_subtitle()

    table[3].show_rlab()
    table[3].show_clab()
    table[3].show_csum()
    table[3].show_rsum()
    table[3].show_grandsum()

    table

    chi_values,chi_square_form=table[3].chi_square_form(table[1],table[2])
    table[3].show_table_of_formulas(chi_values)  #show the table, chi-square cell by cell
    table[1].show_chi_square(chi_square_form)    #show chi_square itself 
    
    sst=table[1].sst+table[2].sst+table[3].sst+'E\n'
    #print sst
    #jk=open("junk.sst","w")
    #jk.write(sst)
    #jk.close()
    outf=open(parameters["spread_sheet_file_name"],"w")
    outf.write(sst)
    outf.close()
    #print sst
    return sst



# MAIN PROGRAM #

if __name__=="__main__":

    outf=open("dwv_out_spread3.slk","w")
    
    parameters={}  #This will be the command dictionary already in the program
    #parameters["first_row"]=1

##    #initial test
##    parameters["nrow"]=3
##    parameters["ncol"]=4
##    parameters["rlab"]=["r1","r2","r3"]
##    parameters["clab"]=["c1","c2","c3","c4"]
##    parameters["ndim"]=2
##    parameters["sssubtable_upper_left_corner"]=(1,1)
##    parameters["rm"]=[1,2,1]
##    parameters["cm"]=[2,1,2,1]
##    #rx=zeros((3,2))
##    rx=array([[1,2],[1,1],[2,1]])
##    parameters['rx']=rx
##    #cx=zeros((4,2))
##    cx=array([[4,1],[3,2],[2,3],[1,4]])
##    parameters['cx']=cx
##    data=[[1,2,3,4],[2,3,4,1],[3,4,1,2]]
##    parameters['data']=array(data)
##    parameters['minkowski']=2
##    parameters['attenuation']=1

    #test what it does from scratch instead of just verifying Dutch Elections
    spread_sheet_file_name="Dutch_Elections1D.slk"
    #outf="dwv_out_spread3.slk"
    #outf=open("DutchElections2Dim.slk","w")
    #outf=open(outf,"w")
    parameters["spread_sheet_file_name"]=spread_sheet_file_name
    parameters["nrow"]=6
    parameters["ncol"]=6
    parameters["rlab"]=["Rural","Rural Industrialized","Commuter","Small City","Middle Large City","Large City"]
    parameters["clab"]=["Labour Party","Christn Dem","Liberals","Rt Liberal","Lt Liberal","Right-relig"]
    parameters["ndim"]=1
    parameters["sssubtable_upper_left_corner"]=(1,1)
    parameters["rm"]=[12.67,24.36,20.98,12.3,18,33.63]
    parameters["cm"]=[42.37,35.52,42.33,56.27,4.05,3.79]
    #rx=zeros((3,2))
    rx=array([[-.345588316603],[0],[0],[0],[0],[0]])
    parameters['rx']=rx
    #cx=zeros((4,2))
    cx=array([[-2.30571665452],[0],[0],[0],[0],[0]])
    parameters['cx']=cx
    observed_data=[[285,482,186,49,21,60],[620,914,308,102,42,97],[355,460,347,104,36,47],[336,337,168,62,27,46],
          [548,455,233,91,47,43],[903,516,343,153,110,37]]
    parameters['observed_data']=array(observed_data)
    parameters['minkowski_power']=2
    parameters['attenuation_power']=.64906
    parameters['d_start']=.1
    parameters['mod_form']="n_cauchy"
    

    sst=dwv_spread_sheet_generator(parameters)

    #print "sst text is:"
    #print sst
