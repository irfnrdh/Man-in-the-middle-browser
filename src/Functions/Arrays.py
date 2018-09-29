'''
This file contains the array functions this program use
'''

def get_phrase_from_list(list, phrase):
    ''' This function return only the objects that has specific phrase '''
    listOut = []
    for obj in list:
        if (phrase in obj):
            listOut.append(obj)
    return listOut

def split_list_by_phrase(list, phrase, location):
    ''' This function split each line in the list and return specififc part of the splitted line '''
    listOut = []
    for line in list:
        listOut.append(str(line).split(phrase)[location])
    return listOut
    
def count_layers(l):
    count = 0
    for e in l:
        if isinstance(e, list):
            count = count + 1 + count_layers(e)
    return count