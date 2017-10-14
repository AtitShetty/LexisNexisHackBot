import json
from collections import OrderedDict

name_title = dict()

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

def flatten(keys):
    ret=''
    if isinstance(keys,OrderedDict):
        if 'name' in keys:
            ret = ret + name_title[keys['name']]
        return ret
    else:
        count = 0
        for arr in keys:
            #print arr
            if count == 0:
                ret = ret + flatten(arr)
                count = count+1
            else:
                ret = ret + ','+flatten(arr)
        return ret
    
            
            
#uni_code_text = ''.join(i for i in row['comments'] if ord(i)<128)        
    
        
   
def constructfull(innerjson):
    if isinstance(innerjson, basestring):
        return innerjson
    else:
        ns=''
        count = 0
        if '#text' in innerjson:
            ns = ns + innerjson['#text']
            count = count+1
        for keys in innerjson:
            if count == 0:
                if keys != '#text':
                    k = innerjson[keys]
                    ns = ns + add_single_or_array(k)
                    count = count + 1
            else:
                if keys != '#text':
                    k = innerjson[keys]
                    ns = ns + ' '+ add_single_or_array(k)
        return ns
                
            
        

def get_abstract( text ):
    for val in j_array:
        if val['title'] == text:
            return val


p = get_abstract('What is narrowing my results?')



def get_add_links(conrefs):
    if isinstance(conrefs, basestring):
        return name_title[conrefs]
    retref=''
    count = 0
    for keys in conrefs:
        if count == 0:
            retref = retref + flatten(conrefs[keys])
            count = count+1
        else:
            retref = retref +','+ flatten(conrefs[keys])
    return retref


        
for val in j_array:
    title = ''
    if (val['title']):
        title=constructfull(val['title'])
    name_title[val['name']] = title
    
#Tutorial: Getting Started with Lexis Advance\u00ae
text_file = open("output.tsv", "w")           
for val in j_array:
    abstract=''
    title=''
    if (val['title']):
        title=constructfull(val['title'])
    if(val['abstract']):
        abstract=constructfull(val['abstract'])
    if(val['conrefs']):
        add_links = get_add_links(val['conrefs'])
    else:
        add_links = None
    dictionary = {'summary':abstract,'additionalLinks':add_links}
    row=title+'\t'+  json.dumps(dictionary)+'\n'
    row = ''.join(i for i in row if ord(i)<128)
    text_file.write(row)    
        
                    
text_file.close()		

            
        
    
    
        
    
    
