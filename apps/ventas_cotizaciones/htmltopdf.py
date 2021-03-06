import os
from django.conf import settings
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from xhtml2pdf import pisa


# Convert HTML URIs to absolute system paths so xhtml2pdf can access those resources
def link_callback(uri, rel):
    # use short variable names
    sUrl = settings.STATIC_URL      # Typically /static/
    sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL       # Typically /static/media/
    mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri # handle absolute uri (ie: http://some.tld/foo.png)

    # make sure that file exists
    if not os.path.isfile(path):
            raise Exception(
                    'media URI must start with %s or %s' % \
                    (sUrl, mUrl))
    return path

def generate_pdf(template_src,  context_dict):
   

    # Render html content through html template with context
    template = get_template(template_src)
    html  = template.render(Context(context_dict))

    # Write PDF to file
    filename = ''
    if template_src == 'factura_venta.html':
        filename = 'factura{0}.pdf'.format(context_dict['fecha'])
    elif template_src == 'recibo_consignacion.html':
        filename = 'recibo{0}.pdf'.format(context_dict['fecha'])
    path = 'static/pdfs/' + filename
    print path
    file = open(path, "w+b")
    pisaStatus = pisa.CreatePDF(html, dest=file,
            link_callback = link_callback)

    # Return PDF document through a Django HTTP response
    file.seek(0)
    pdf = file.read()
    file.close()            # Don't forget to close the file handle
    
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition']='attachment; filename=' + filename
    os.remove(path) 
    return response
    #return HttpResponse(pdf, 'application/pdf')