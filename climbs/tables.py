import django_tables2 as tables
from .models import Boulder, Route, Climb

class ClimbTable(tables.Table):
    # AreaDate =  tables.Column(order_by=('date', 'area'))
    selection = tables.CheckBoxColumn(accessor='pk', orderable = True)
    class Meta:
        model = Climb
        template_name = 'django_tables2/bootstrap-responsive.html'
        fields = ['date', 'area', 'grade', 'color', 'setter']
        # order_by_field = True
class ClimbRemoveTable(tables.Table):
    class Meta:
        model = Climb
        template_name = 'django_tables2/bootstrap-responsive.html'

class RouteTable(tables.Table):
    selection = tables.CheckBoxColumn(accessor='pk', orderable = True)
    class Meta:
        model = Boulder
        template_name = 'django_tables2/bootstrap-responsive.html'
