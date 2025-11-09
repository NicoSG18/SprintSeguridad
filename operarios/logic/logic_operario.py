from ..models import Operario

def get_operarios():
    queryset = Operario.objects.all().order_by('-dateTime')[:10]
    return (queryset)

def create_operario(form):
    operario = form.save()
    operario.save()
    return ()