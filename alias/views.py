from django.core.exceptions import ValidationError
from django.http import JsonResponse, HttpResponseNotAllowed
from .models import Alias
from .utilities import datetime_from_string


def create_alias(request):
    if request.method == 'POST':
        alias_args = {
            'alias': request.POST['alias'],
            'target': request.POST['target']
        }

        if 'start' in request.POST:
            alias_args['start'] = datetime_from_string(request.POST['start'])

        if 'end' in request.POST:
            alias_args['end'] = datetime_from_string(request.POST['end'])

        try:
            alias = Alias(**alias_args)
            alias.save()
        except ValidationError as exc:
            return JsonResponse({'Failure': exc.message})

        return JsonResponse({'Success': f'{alias_args["alias"]} '
                                        f'alias was created for {alias_args["target"]} object'})
    return HttpResponseNotAllowed(['POST'])


def get_target_by_alias(request):
    alias = request.GET['alias'].replace('/', '')
    aliases = Alias.objects.filter(alias=alias)
    return JsonResponse({f'{alias} objects': aliases.count(),
                         'target': list(al.target for al in aliases)})
