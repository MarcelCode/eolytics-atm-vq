from geodata.models import UserProjectShape
from projects.models import UserProject
from accounts.models import Profile


def get_entry_by_pk(pk, model):
    try:
        entry = model.objects.get(pk=pk)
    except:
        entry = None

    return entry


def get_available_cores(user):
    user_projects = UserProject.objects.filter(user=user)
    available_cores = Profile.objects.get(user=user).cpu_cores
    cores = sum(user_projects.values_list("cores", flat=True))

    return available_cores - cores


def bytes_to_gb(bytes_value):
    return bytes_value / 1000000000


def get_percentage(sum_value, part_value):
    return (part_value / sum_value) * 100
