import django_tables2 as tables
from .models import Climb, Grade
from django_tables2.utils import A
import datetime

DATE = datetime.date.today()


class ClimbTable(tables.Table):
    # AreaDate =  tables.Column(order_by=('date', 'area'))
    edit = tables.LinkColumn('climb_update', text='Edit', args=[A('pk')], orderable=False, empty_values=(), attrs={'td':{"class": "btn"}})
    selection = tables.CheckBoxColumn(accessor='pk', orderable = True)


    class Meta:
        model = Climb
        template_name = 'django_tables2/bootstrap-responsive.html'
        fields = ['date_created', 'anchor', 'area', 'grade', 'color', 'setter']


class QueueTable(tables.Table):
    edit = tables.LinkColumn('climb_update', text='Choose', args=[A('pk')], orderable=False, empty_values=(), attrs={'td':{"class": "btn"}})

    class Meta:
        model = Climb
        template_name = 'django_tables2/bootstrap-responsive.html'
        fields = ['date_created', 'grade']


class ClimbRemoveTable(tables.Table):
    class Meta:
        model = Climb
        template_name = 'django_tables2/bootstrap-responsive.html'
        fields = ['anchor', 'date_created', 'color', 'grade', 'area', 'setter']


class ClimbQuery(tables.Table):
    date_created = tables.Column()
    area__location_name = tables.Column()
    count = tables.Column()
    min_grade = tables.Column()
    max_grade = tables.Column()

    class Meta:
        template_name = 'django_tables2/bootstrap-responsive.html'


class GradeSpreadTable(tables.Table):
    grade = tables.Column()
