import json
from collections import OrderedDict

json_file = 'map.json'
json_data=open(json_file)

j = json.load(json_data,object_pairs_hook=OrderedDict)

j_array = j['map']['product']['lbu']['locale']['concepts']['concept'] + j['map']['product']['lbu']['locale']['fields']['field'] + j['map']['product']['lbu']['locale']['references']['reference'] + j['map']['product']['lbu']['locale']['tasks']['task'] + j['map']['product']['lbu']['locale']['topics']['topic']
#print len(j_array)
#j_j = j_array[0]

#print j_j['@group']

def add_single_or_array(s):
    ret=''
    if isinstance(s,OrderedDict):
        if '#text' in s:
            ret = ret + s['#text']
        if '#tail' in s:
            ret = ret +' '+ s['#tail']
        return ret
    else:
        for arr in s:
            #print arr
            ret = ret + add_single_or_array(arr)
        return ret
            
            
#uni_code_text = ''.join(i for i in row['comments'] if ord(i)<128)        
    
        
   
def constructfull(innerjson):
    if isinstance(innerjson, basestring):
        return innerjson
    else:
        ns=''
        if '#text' in innerjson:
            ns = ns + innerjson['#text']
        for keys in innerjson:
            if keys != '#text':
                k = innerjson[keys]
                ns = ns + ' '+add_single_or_array(k)
        return ns
                
            
        

def get_abstract( text ):
    for val in j_array:
        if val['title'] == text:
            return val['abstract']


#p = get_abstract('What is a results list?')


#Tutorial: Getting Started with Lexis Advance\u00ae
text_file = open("output.tsv", "w")           
for val in j_array:
    abstract=''
    title=''
    if (val['title']):
        title=constructfull(val['title'])
    if(val['abstract']):
        abstract=constructfull(val['abstract'])
    dictionary = {'summary':abstract,'additionalLinks':'None'}
    row=title+'\t'+  json.dumps(dictionary)+'\n'
    row = ''.join(i for i in row if ord(i)<128)
    text_file.write(row)    
        
                    
text_file.close()		

            
        
    
    
        
    
    
