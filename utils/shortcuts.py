from functools import wraps                                                         
from django.shortcuts import render_to_response                                     
from django.template import RequestContext                                          
                                                                                    
def render_to(template):                                                            
    """                                                                             
    Decorator for Django views that sends returned dict to render_to_response       
    function with given template and RequestContext as context instance.            
                                                                                    
    If view doesn't return dict then decorator simply returns output.               
                                                                                    
    Parameters:                                                                     
                                                                                    
     - template: template name to use                                               
    """                                                                             
    def render_to_decorator(func):                                                  
        @wraps(func)                                                                
        def wrapper(request, *args, **kwargs):                                      
            output = func(request, *args, **kwargs)                                 
            if isinstance(output, dict):                                            
                return render_to_response(template, output, RequestContext(request))
            return output                                                           
        return wrapper                                                              
    return render_to_decorator         
