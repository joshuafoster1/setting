import django_tables2 as tables
from .models import Climb, Grade
from django_tables2.utils import A
import datetime

DATE = datetime.date.today()

def row_format(record):
    weeks = ((DATE - record.date_created)/7).days
    if weeks > 9:
        return 'table-danger'
    elif weeks > 7:
        return 'table-warning'
    else:
        return 'table-success'

def query_format(record):
    weeks = ((DATE - record['date_created'])/7).days
    if weeks > 9:
        return 'table-danger'
    elif weeks > 7:
        return 'table-warning'
    else:
        return 'table-success'


class WeeksOldColumn(tables.Column):
    def render(self, value, record):
        weeks = (DATE - record.date_created)/7
        return weeks.days


class InProgressTable(tables.Table):
    revert = tables.LinkColumn('revert_climb', text='Revert', args=[A('pk')], orderable=False, empty_values=(), attrs={'td':{"class": "btn"}})
    update = tables.LinkColumn('climb_update', text='Edit', args=[A('pk')], orderable=False, empty_values=(), attrs={'td':{"class": "btn"}})
    class Meta:
        model = Climb
        template_name = 'django_tables2/bootstrap-responsive.html'
        fields = [ 'anchor', 'area', 'grade', 'color', 'setter']
        sequence = ('update', 'area', 'grade', 'color', 'setter','anchor' )


class ClimbTable(tables.Table):
    # AreaDate =  tables.Column(order_by=('date', 'area'))
    update = tables.LinkColumn('climb_update', text='Edit', args=[A('pk')], orderable=False, empty_values=(), attrs={'td':{"class": "btn"}})
    selection = tables.CheckBoxColumn(accessor='pk', orderable = True)
    weeks_old = WeeksOldColumn(empty_values=(), order_by=('date_created'))

    class Meta:
        model = Climb
        template_name = 'django_tables2/bootstrap-responsive.html'
        fields = [ 'anchor', 'area', 'grade', 'color', 'setter']
        sequence = ('selection', 'update', 'weeks_old', 'area', 'grade', 'color', 'setter','anchor' )
        row_attrs = {
            'class': lambda record: row_format(record)
        }

class ClimbQueryTable(ClimbTable):
    # update = tables.LinkColumn('climb_select', text='Edit', args=[A('pk')], orderable=False, empty_values=(), attrs={'td':{"class": "btn"}})
    selection = tables.CheckBoxColumn(accessor='pk', checked=True, orderable = True)
    weeks_old = WeeksOldColumn(empty_values=(), order_by=('date_created'))

    class Meta:
        model = Climb
        template_name = 'django_tables2/bootstrap-responsive.html'
        fields = [ 'anchor', 'area', 'grade', 'color', 'setter']
        sequence = ('selection', 'update', 'weeks_old', 'area', 'grade', 'color', 'setter','anchor' )
        row_attrs = {
            'class': lambda record: row_format(record)
        }

class QueueTable(tables.Table):
    choose = tables.LinkColumn('climb_select', text='Choose', args=[A('pk')], orderable=False, empty_values=(), attrs={'td':{"class": "btn"}})
    class Meta:
        model = Climb
        template_name = 'django_tables2/bootstrap-responsive.html'
        fields = ['grade', 'area']

class ForemanQueueTable(tables.Table):
    modify = tables.LinkColumn('queue_modify', text='Change', args=[A('pk')], orderable=False, empty_values=(), attrs={'td':{"class": "btn"}})
    class Meta:
        model = Climb
        template_name = 'django_tables2/bootstrap-responsive.html'
        fields = ['grade', 'area']

class ClimbRemoveTable(tables.Table):
    # selection = tables.CheckBoxColumn(accessor='id', checked=True, orderable = True)

    class Meta:
        model = Climb
        template_name = 'django_tables2/bootstrap-responsive.html'
        fields = ['date_created', 'color', 'grade', 'area', 'setter', 'anchor']


class ClimbQuery(tables.Table):
    selection = tables.CheckBoxColumn(accessor='date_created', orderable = True)

    date_created = tables.Column()
    area__location_name = tables.Column()
    count = tables.Column()
    min_grade = tables.Column()
    max_grade = tables.Column()

    class Meta:
        template_name = 'django_tables2/bootstrap-responsive.html'
        row_attrs = {'class': lambda record: query_format(record)
        }

class GradeSpreadTable(tables.Table):
    grade = tables.Column()
