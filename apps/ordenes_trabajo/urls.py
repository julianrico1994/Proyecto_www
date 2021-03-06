from django.conf.urls import patterns, url
from .views import *
from .forms import *

urlpatterns = patterns('',
    url(r'^ordenes_trabajo/registro/$', RegisterView.as_view(), name='registro_orden'),
    url(r'^ordenes_trabajo/repuesto/$', AutorizarRepuestoView.as_view(), name='autorizar_repuesto'),
    url(r'^ordenes_trabajo/buscar/$', OrderDataTableView.as_view()),
    url(r'^ordenes_trabajo/consultar_estado/$', recibir_dato),
)
