import json


json_file = 'map.json'
json_data=open(json_file)

j = json.load(json_data)

j_array = j['map']['product']['lbu']['locale']['concepts']['concept'] + j['map']['product']['lbu']['locale']['fields']['field'] + j['map']['product']['lbu']['locale']['references']['reference'] + j['map']['product']['lbu']['locale']['tasks']['task'] + j['map']['product']['lbu']['locale']['topics']['topic']
#print len(j_array)
#j_j = j_array[0]

#print j_j['@group']

def get_abstract( text ):
    for val in j_array:
        if val['title'] == text:
            return val['abstract']


get_abstract('What is narrowing my results?')


            
        

        
    
    
        
    
    
