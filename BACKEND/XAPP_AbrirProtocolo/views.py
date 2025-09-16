from django.http import HttpResponse

# Create your views here.
def Hello(request):
    return HttpResponse("Hello, world. You're at the XAPP_AbrirProtocolo index.")