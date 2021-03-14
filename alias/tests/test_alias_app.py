from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from alias.models import Alias


class AliasTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        Alias.objects.create(alias='alias1', target='target1',
                             start=timezone.make_aware(datetime(2021, 3, 13, 12, 30, 30, 456655)),
                             end=timezone.make_aware(datetime(2021, 4, 4, 13)))
        Alias.objects.create(alias='alias2', target='target2',
                             end=datetime(2021, 3, 18, 14, 10, 20, 537555))
        Alias.objects.create(alias='alias3', target='target3',
                             start=timezone.make_aware(datetime(2021, 3, 13, 16, 30, 30)),
                             end=timezone.make_aware(datetime(2021, 3, 21, 14, 20, 20, 345655)))
        Alias.objects.create(alias='alias4', target='target1',
                             start=timezone.make_aware(datetime(2021, 3, 15, 18, 15)))

    def test_get_target_by_alias(self):
        url = reverse('get_target')
        resp = self.client.get(url, {'alias': 'alias1'})
        self.assertEquals(resp.status_code, 200)
        self.assertTrue(b'target1' in resp.content)

    def test_create_overlap_alias_not_allowed(self):
        url = reverse('create_alias')
        alias = {
            'alias': 'alias1',
            'target': 'target1',
            'start': '2021-03-17/15:30:30',
            'end': '2021-04-06/15'
        }
        resp = self.client.post(url, alias)

        self.assertEquals(resp.status_code, 200)
        self.assertIn(b'Failure', resp.content)
        self.assertIn(b'Alias lifetime should not overlap same name alias on the target.',
                      resp.content)

    def test_milliseconds_difference_not_overlap(self):
        url = reverse('create_alias')  # 2021, 3, 18, 14, 10, 20, 537555)
        alias = {
            'alias': 'alias2',
            'target': 'target2',
            'start': '2021-03-18/14:10:20.537555',
            'end': '2021-04-06/15'
        }
        resp = self.client.post(url, alias)

        self.assertEquals(resp.status_code, 200)
        self.assertIn(b'Success', resp.content)

    def test_milliseconds_difference_overlap(self):
        url = reverse('create_alias')
        alias = {
            'alias': 'alias3',
            'target': 'target3',
            'start': '2021-03-21/14:20:20.345654',
            'end': '2021-04-06/15'
        }
        resp = self.client.post(url, alias)

        self.assertEquals(resp.status_code, 200)
        self.assertIn(b'Failure', resp.content)
        self.assertIn(b'Alias lifetime should not overlap same name alias on the target.',
                      resp.content)
    
    def test_create_alias_and_get_target(self):
        url = reverse('create_alias')
        alias = {
            'alias': 'alias1.1',
            'target': 'target1',
            'start': '2021-03-13/12:30:30.456655',
            'end': '2021-04-04/13'
        }
        resp = self.client.post(url, alias)

        get_url = reverse('get_target')
        get_resp = self.client.get(get_url, {'alias': 'alias1.1'})

        self.assertEquals(resp.status_code, 200)
        self.assertEquals(get_resp.status_code, 200)

        self.assertIn(b'target1', get_resp.content)
        self.assertIn(b'Success', resp.content)
