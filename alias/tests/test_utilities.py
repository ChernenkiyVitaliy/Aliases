from datetime import datetime
from django.test import TestCase, Client
from alias.utilities import get_aliases, alias_replace
from django.utils import timezone
from alias.models import Alias


class UtilitiesTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.now = timezone.now()
        Alias.objects.create(alias='alias2', target='target1',
                             start=timezone.make_aware(datetime(2021, 3, 13, 12, 30, 30, 456655)),
                             end=timezone.make_aware(datetime(2021, 4, 4, 13)))
        Alias.objects.create(alias='alias3', target='target1',
                             start=timezone.make_aware(datetime(2021, 3, 15, 10, 30, 30)),
                             end=datetime(2021, 4, 2, 14, 10, 20, 537555))
        Alias.objects.create(alias='alias4', target='target1',
                             start=timezone.make_aware(datetime(2021, 3, 14, 16, 30, 30)),
                             end=timezone.make_aware(datetime(2021, 4, 3, 14, 20)))
        Alias.objects.create(alias='alias5', target='target1',
                             start=timezone.make_aware(datetime(2021, 3, 15, 18, 15, 20, 200000)))
        Alias.objects.create(alias='alias6', target='target1',
                             start=timezone.make_aware(datetime(2021, 3, 18, 18, 15)))
        Alias.objects.create(alias='alias7', target='target1',
                             start=timezone.make_aware(datetime(2021, 4, 18, 18, 15)))
        Alias.objects.create(alias='alias8', target='target2',
                             end=timezone.make_aware(datetime(2021, 4, 20, 18, 15)))
        Alias.objects.create(alias='alias9', target='target2',
                             end=timezone.make_aware(datetime(2021, 3, 21, 19, 20)))
        Alias.objects.create(alias='alias10', target='target2',
                             end=timezone.make_aware(datetime(2021, 4, 21, 20, 15, 30, 155000)))
        Alias.objects.create(alias='alias11', target='target2',
                             end=timezone.make_aware(datetime(2021, 4, 21, 20, 15, 30, 155001)))

    def test_get_aliases_func(self):
        start = timezone.make_aware(datetime(2021, 3, 10, 16))
        end = timezone.make_aware(datetime(2021, 4, 4, 13))
        res = get_aliases('target1', from_date=start, to_date=end)
        results = [al.alias for al in res]

        self.assertIn('alias2', results)
        self.assertIn('alias3', results)
        self.assertIn('alias4', results)
        self.assertNotIn('alias5', results)

    def test_get_aliases_func_without_to_date(self):
        start = timezone.make_aware(datetime(2021, 3, 15, 18, 15, 20, 199999))
        res = get_aliases('target1', from_date=start)
        results = [al.alias for al in res]

        self.assertIn('alias5', results)
        self.assertIn('alias6', results)
        self.assertIn('alias7', results)
        self.assertNotIn('alias2', results)

    def test_get_aliases_fun_without_dates(self):
        res = get_aliases('target1')
        results = [al.alias for al in res]

        self.assertIn('alias2', results)
        self.assertIn('alias4', results)
        self.assertIn('alias6', results)
        self.assertNotIn('alias9', results)

    def test_alias_replace_func(self):
        existing_alias = Alias.objects.get(alias='alias2')
        end = timezone.make_aware(datetime(2021, 3, 25, 10, 30, 30))
        new_alias_value = 'new_alias'
        alias_replace(existing_alias, end, new_alias_value)

        changed_alias = Alias.objects.get(alias='alias2')
        new_alias = Alias.objects.get(alias=new_alias_value)
        
        self.assertEquals(new_alias.alias, new_alias_value)
        self.assertEquals(new_alias.start, end)
        self.assertEquals(new_alias.end, None)
        
        self.assertEquals(changed_alias.end, end)
        self.assertEquals(changed_alias.alias, 'alias2')
