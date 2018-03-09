import django_tables2 as tables
from .models import Boulder, Route

class BoulderTable(tables.Table):
    # AreaDate =  tables.Column(order_by=('date', 'area'))
    selection = tables.CheckBoxColumn(accessor='pk', orderable = True)
    class Meta:
        model = Boulder
        template_name = 'django_tables2/bootstrap-responsive.html'
        # order_by_field = True

class RouteTable(tables.Table):
    selection = tables.CheckBoxColumn(accessor='pk', orderable = True)
    class Meta:
        model = Boulder
        template_name = 'django_tables2/bootstrap-responsive.html'
