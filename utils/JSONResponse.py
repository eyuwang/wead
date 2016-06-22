import json                                                                         
                                                                                    
from django.core import serializers                                                 
from django.core.serializers.json import DjangoJSONEncoder                          
from django.http import HttpResponse                                                
from django.db.models.query import QuerySet                                         
                                                                                    
                                                                                    
class JSONEncoder(json.JSONEncoder):                                                
    """                                                                             
    Encode an object in JSON.                                                       
    """                                                                             
    def default(self, obj):                                                         
        if hasattr(obj, '__json__'):                                                
            return obj.__json__()                                                   
        return json.JSONEncoder.default(self, obj)                                  
                                                                                    
                                                                                    
class JsonResponse(HttpResponse):                                                   
    """                                                                             
    Create a response that contains a JSON string.                                  
    """                                                                             
    def __init__(self, content, content_type='application/json; charset=utf-8',  
                 status=200, encoder=JSONEncoder):                                  
        if isinstance(content, QuerySet):                                           
            temp = serializers.serialize('python', content)                         
            data = json.dumps(temp, indent=3, cls=DjangoJSONEncoder)                
        else:                                                                       
            data = json.dumps(content, indent=3, cls=encoder)                       
        HttpResponse.__init__(self, data, content_type, status) 
