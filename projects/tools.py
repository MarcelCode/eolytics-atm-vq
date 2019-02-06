from geodata.models import UserProjectShape


def get_entry_by_pk(pk):
    try:
        entry = UserProjectShape.objects.get(pk=pk)
    except:
        entry = None

    return entry



