'''
This file contains the parsing functions this program use
'''
def get_object_unbyte(obj):
    '''Returns Unbyted object'''
    if (type(obj) == bytes):
        return bytes(obj).decode()
    else:
        return obj
