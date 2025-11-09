from ..models import Variable

def get_variables():
    queryset = Variable.objects.all()
    return (queryset)

def get_variable(id):
    variable = Variable.objects.raw("SELECT * FROM variables_variable WHERE id=%s" % id)[0]
    return (variable)

def create_variable(form):
    measurement = form.save()
    measurement.save()
    return ()
