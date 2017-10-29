#imports libraries
import pandas as pd
import re
import editdistance as editd

#open tower files
def csvFilesToDataFrame(files):
    return pd.concat([pd.read_csv(_file) for _file in files])
     
def select_columns(prefix_list, columns):
    return [item for item in col_names 
            if any(item.startswith(prefex) for prefex in prefix_list)]


#read from the file
def read_rtf(rtf_file):
    _file = open(rtf_file, 'r')
    rtf_data = _file.read().strip()
    _file.close()
    return rtf_data

#pick the links in the file
def rtf_links(rtf_data):
    return re.findall('\s+(.*?)}}', rtf_data)
#split and clean strings
def split_clean_str(string, split, index):
    return string.split(split)[index].strip()
#clean all the links in the rtf file
def link_text(rtf_links):
    return [split_clean_str(item, '3', 1) for item in rtf_links if not 'http' in item]
#Get the text from all the links in the rtf file
def get_rtf_linkTexts(rtf_file):
    twr_comps = read_rtf(rtf_file)
    twr_comp_links = rtf_links(twr_comps)
    return link_text(twr_comp_links)
    


#Input:
    #name1: Name of a company
    #name2: Name of a company
    #lte_name: Name of a known LTE provider
#output:
    #Checks if name of the lte company is in name1 and name2
    #calculates score based on the how much of the lte provider's name
    #is in both name1 and name2
def commonGrade(name1,name2, lte_name):
    name1 = str(name1).lower()
    name2 = str(name2).lower()
    
    whole = 30.0
    first = 18.0
    dist = 0
    if any([isinstance(nam,float) for nam in [name1, name2, lte_name]]):
            return dist
    if isinstance(lte_name, str):
        lte_name = lte_name.lower()
        
        
        if lte_name in name1 and lte_name in name2:
            return whole;
        return dist
    if isinstance(lte_name, tuple):
        main = lte_name[0].lower()
        extension = lte_name[1].lower()
        if main in name1 and main in name2:
            dist+=first
            if extension in name1 and extension in name2:
                dist+=whole-first
        return dist
    raise ValueError("Found something lte name that's neither string nor tuple!")
            
def both_LTE(name1,name2):
    #print [commonGrade(name1,name2, lte_name) for lte_name in lte]
    return max([commonGrade(name1,name2, lte_name) for lte_name in lte])
'''
Calculates the distance between the names of two companies based on the edit distance and
the number of similar works present
'''
def distance(name1, name2):
    #print "name 1: "+name1
    #print "name 2: "+name2
    _nm1 = str(name1).lower().split(',')[0]#.split(' ')
    _nm2 = str(name2).lower().split(',')[0]#.split(' ')
    nm1 = _nm1.split(' ')
    nm2 = _nm2.split(' ')
   
    bound = min(len(nm1),len(nm2))
    dist = 20.0
    both_lte = both_LTE(name1, name2)
    for i in range(bound):
        if nm1[i]==nm2[i]:
            dist+=dist/((i+1)**2)
        else:
            dist-=dist/((i+1)**2)
    return dist - editd.eval(_nm1, _nm2)+both_lte
                   
    



#distances array between a names and list of names
def one_to_many(one, many):
    return [(one,item, distance(one, item)) for item in many]
'''
input:
    owners: Owner names of found towers
    towerComp: Known tower companies 
output:
    data frame of (owner, tower companies, names distance)
'''
def owner_to_company_name_dist(owners, towerComp):
    distances = [one_to_many(name[0], towerComp) for name in owners]
    comparision_frame = pd.concat([pd.DataFrame(item, columns = ('tower owner', 'tower company','name distance')) 
                                 for item in distances])
    return comparision_frame

#input:
    #html_file: html file
#output: 
    #Tables: list of raw tables extracted from the file
def wekipediaScraper(html_file):
    open_file = open(html_file, 'r')
    file_data = open_file.read()
    open_file.close()
    opening_table = '<table class=[.*?] border=[.*?] cellpadding=[.*?] style=[.*?]>'
    tables= re.findall('(?s)(?<=<table)(.+?)(?=</table>)', file_data)
    #print file_data
    return tables


#input:
    #tables: list of raw html table contents
#output: 
    #matrix of html table row raw contents
def tableRow(tables):
    return [re.findall('(?s)(?<=<tr)(.+?)(?=</tr>)', table) for table in tables]


#input: 
    #tr: raw html row content
#output:
    #list of clean text extracted each column of the row
def separateCols(tr):
    cols = re.findall('(?s)(?<=<td)(.+?)(?=/td>)|(?s)(?<=<th)(.+?)(?=/th>)', tr)
    clean_cols = [re.findall('(?s)(?<=>)(.+?)(?=<)',max(col, key = len)) for col in cols]
    cleaned_cols = [max(col,key=len).split('>')[-1] if col else 'NaN' for col in clean_cols]
    
    
    return cleaned_cols

#input:
    #table: raw html table content
#output:
    #Data frame of the html table cell text
def table_to_dataframe(table):
    matrix = [separateCols(tr) for tr in table]
    return pd.DataFrame(matrix[1:], columns=matrix[0])
#input:
    #html_file: html file
    #index: index location of a table in the file
#output:
    #dataframe of the cell content of the table with given index
def html_table_to_dataframe(html_file, index):
    tables = wekipediaScraper(html_file)
    row_separated = tableRow(tables)
    return table_to_dataframe(table[index])


