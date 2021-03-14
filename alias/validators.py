
def check_overlaps(model, alias) -> bool:
    """
        Function checks if created alias instance
        don't overlap other aliases with same name and target
            Args:
                model: alias ORM class.
                alias: checking alias instance.
            Returns:
                True if dates on object with same alias and target
                don't overlap each other else False.
    """
    aliases = model.objects.filter(alias=alias.alias, target=alias.target)
    if aliases.exists():
        return all(is_overlap(alias, al) for al in aliases)

    return True


def is_overlap(first_alias, sec_alias) -> bool:
    """
        Function checks if passed alias instances
        overlap each other.
            Args:
                first_alias: alias instance.
                sec_alias: alias instance.
            Returns:
                True if aliases don't overlap each other.
        """
    if first_alias.end is not None and sec_alias.end is not None:
        latest_start = max(first_alias.start, sec_alias.start)
        earliest_end = min(first_alias.end, sec_alias.end)
        return latest_start >= earliest_end

    elif first_alias.end is None:
        return sec_alias.end <= first_alias.start

    elif sec_alias.end is None:
        return first_alias.end <= sec_alias.start

    return False
