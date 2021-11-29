from auto import DatasetReader
'''
We import:
- the Flask class
- Flask's render_template() helper function to serve an HTML template as the response.
- request, as Web applications use different HTTP methods when accessing URLs. Remember that by default, a route only answers to GET requests.

'''
from flask import Flask, render_template, request
'''
First we imported the Flask class. An instance of this class will be our WSGI application.
Next we create an instance of this class. The first argument is the name of the application’s module or package.
 __name__ is a convenient shortcut for this that is appropriate for most cases. 
This is needed so that Flask knows where to look for resources such as templates and static files.
'''

myapp = Flask(__name__)

registry = None
'''
We then use the route() decorator to tell Flask what URL should trigger our function.
The function returns the HTML template we want to display in the user’s browser. 
The default content type is HTML, so HTML in the string will be rendered by the browser.
'''
@myapp.route("/")
def index():
    '''
    #All you have to do is provide the name of the template and the variables you want to pass to the template as keyword arguments.
    Flask will look for templates in the templates folder. In this case we have:
    /auto.py
    /templates
        /index.html
    I could also write an additional route "/index.html" and it would access both pages
    '''
    return render_template("index.html", registry=registry)

@myapp.route("/manufacturer")
def manufacturer():
    '''
    request.args returns a "dictionary" object for you:
    get(key, default=None, type=None)
    In this case I want to make sure to return manufacturers for the brands that are in the registry
    '''
    brand = request.args.get("brand")

    if brand in registry:
        manufacturer = registry[brand]
    else:
        manufacturer = None

    return render_template("brand.html", manufacturer=manufacturer)


if __name__ == '__main__':
    registry = DatasetReader.read('Auto.tsv')
    myapp.run()



