import re

grimms = open("grimms.txt","r")
with open('stopwords.txt') as sw:
    print("with open issue") 
    swlines = sw.read().splitlines()

#INITIALIZING VARIABLES  
ln = 0 
cbl = 0 #current blank line
fbl = False
upper = False 
cst = "" #current story title
start = 124 #start of fairy tales
end = 9209 #end of fairy tales is 
w2s = {} #words to stories dict
list_st = [] #list of story titles
lines = ['first index'] #indexable list of lines
q_st = []
q_ln = []
list_both = [] #overlapping story titles for AND case


#CREATING THE DICT OF DICT OF LISTS for each word mapped to it's story mapped to it's line numbers 
for line in grimms:
    ln += 1
    line = line.strip()
    lines.append(line)
    if (ln >= start and ln <= end):
        if not line: #checks for blank line 
            cbl = ln 
        if line.isupper(): #checks for story title (upper case) 
            cst = line
            list_st.append(line)
        line = re.sub("[^\w\s]", '', line) 
        line = line.lower()
        words_list = line.split()
        for word in words_list:
            if word not in swlines:
                w2s.setdefault(word, {}).setdefault(cst, []).append(ln) #create dict of dict of lists 
    if (ln > end):
        break 



#SEARCH INTERFACE
def search():
    query = input('Please enter your query: ')
    if (query == 'qquit'):  
        quit()
    print("query = ",query,)
    query_list = query.split() #save words of query into an indexable list 
    #CASE 1: query is one word 
    if len(query_list) is 1: 
        q_dict = w2s.get(query, 0) #saves a dictionary of {story title: lines} for that query 
        if q_dict is 0:             
                print('  --  ') #queries with no match 
                search()
        for key in q_dict:
            print(" ",key) #prints the story title
            q_subdict = q_dict.get(key,0) #list of lines at that story title 
            for linenum in q_subdict:
                toprint = (str(linenum)+' '+lines[linenum])
                found = '**' + query.upper() + '***' 
                toprint = re.sub(query, found, toprint)
                print ("       ",toprint)
        search() 

    #special case without and/or : treat like an AND case 
    elif len(query_list) is 2:
        temp = query_list[1]
        query_list[1] = "and" 
        query_list.append(temp)  
    
    if len(query_list) is 3: 
        #CASE 2: OR
        if ('or'== query_list[1]):
            dict1 = w2s.get(query_list[0],0) #save a dictionary of story titles mapped to line numbers for each query word 
            dict2 = w2s.get(query_list[2],0)
            qset = makeset(dict1, dict2) #create a set of possible story titles to loop through and check against  
            for stitle in qset:
                print(" ",stitle)
                #check query word 1 
                if stitle in dict1:
                    print("  ",query_list[0])
                    lines_in_st = dict1.get(stitle,0) 
                    printpretty(lines_in_st, query_list[0])
                if stitle not in dict1:
                    print("  ",query_list[0])
                    print("     ",'  --  ')
                #check query word 2 
                if stitle in dict2:
                    print("  ",query_list[2])
                    lines_in_st = dict2.get(stitle,0)
                    printpretty(lines_in_st, query_list[2])
                if stitle not in dict2:
                    print("  ",query_list[2])
                    print("     ",'  --  ')
            search()

        #CASE 3: AND
        elif ('and' ==query_list[1]):
            dict1 = w2s.get(query_list[0],0) #save a dictionary of story titles mapped to line numbers for each query word 
            dict2 = w2s.get(query_list[2],0)
            qset = makeset(dict1, dict2) #create a set of possible story titles to loop through 
            for stitle in qset:
                if (stitle in dict1) and (stitle in dict2): #only do things if both queries are in both storytitles 
                    print(" ",stitle)
                    print("  ",query_list[0])
                    lines_in_st = dict1.get(stitle,0) 
                    printpretty(lines_in_st, query_list[0])
                    print("  ",query_list[2])
                    lines_in_st = dict2.get(stitle,0)
                    printpretty(lines_in_st, query_list[2])
            search()
  
def makeset(dict1, dict2):
    newset = set()
    for key1, value in dict1.items():
        newset.add(key1)
    for key2, value in dict2.items():
        newset.add(key2)
    return newset

def printpretty(listlines, queryword):
    for linenum in listlines:
        toprint = (str(linenum)+' '+lines[linenum])
        found = '**' + queryword.upper() + '***' 
        toprint = re.sub(queryword, found, toprint)
        print ("       ",toprint)    

print("Welcome to the Grimms' Fairy Tales search system!")
print("                ")
print("                ") 
search() 

