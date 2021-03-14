from datetime import datetime
from django.utils import timezone
from .models import Alias


def datetime_from_string(date_str: str) -> datetime:
    """
    Function converts string into datetime
    String argument must be like 2021-01-01/12:15:15.555555
    Necessary only year month and day then hours minutes and second
    will be 00:00:00
        Args:
            date_str: string data.
        Returns:
            aware datetime value.
    """
    if len(date_str) == 10:
        result = timezone.make_aware(datetime.strptime(date_str, '%Y-%m-%d'))

    elif len(date_str) == 13:
        result = timezone.make_aware(datetime.strptime(date_str, '%Y-%m-%d/%H'))

    elif len(date_str) == 16:
        result = timezone.make_aware(datetime.strptime(date_str, '%Y-%m-%d/%H:%M'))

    elif len(date_str) == 19:
        result = timezone.make_aware(datetime.strptime(date_str, '%Y-%m-%d/%H:%M:%S'))

    else:
        result = timezone.make_aware(datetime.strptime(date_str, '%Y-%m-%d/%H:%M:%S.%f'))

    return result


def get_aliases(target: str, from_date=None, to_date=None):
    """
        Function retrieves a set of alias objects that suit passed filters.
        from_date, to_date are not necessary parameters by default None.
            Args:
                target: foreign key or slug of aliased object.
                from_date: date from which alias gets active.
                to_date: date by which alias is active.
            Returns:
                queryset with alias objects.
        """
    if from_date and to_date:
        result = Alias.objects.filter(target=target, start__gte=from_date, end__lte=to_date)
    
    elif from_date and to_date is None:
        result = Alias.objects.filter(target=target, start__gte=from_date, end__isnull=True)
    
    elif from_date is None and to_date:
        result = Alias.objects.filter(target=target, end__lte=to_date)
    
    else:
        result = Alias.objects.filter(target=target)

    return result


def alias_replace(existing_alias: Alias, replace_at: datetime, new_alias_value: str):
    """
        Function replaces an existing alias with a new one
        at a specific time point (replace_at).

        Args:
            existing_alias: existing alias object.
            replace_at: point of time where to replace existing_alias with anew one.
            new_alias_value: name of new alias.

        Returns:
            None because changes existing objects.
    """
    existing_alias.end = replace_at
    existing_alias.save(update=True)

    Alias.objects.create(alias=new_alias_value, target=existing_alias.target,
                         start=replace_at)

    return None
