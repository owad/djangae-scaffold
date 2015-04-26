from copy import copy

from django.test import TestCase

from lottery import pick_bugmans


class LotteryTest(TestCase):

    def _no_same_bugman_in_a_row(self, bugmans):
        bugmans_copy = copy(bugmans) + ['']
        for i, bugman in enumerate(bugmans):
            self.assertNotEqual(bugman, bugmans_copy[i+1])

    def test_more_devs_than_working_days(self):
        devs = ['bob', 'mike', 'ernie', 'fred', 'pooh']
        days = ['monday', 'tuesday', 'wednesday']
        res = pick_bugmans(devs, days)
        self.assertEqual(len(set(res)), len(days))
        self._no_same_bugman_in_a_row(res)

    def test_less_devs_than_working_days(self):
        devs = ['bob', 'mike', 'ernie']
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
        res = pick_bugmans(devs, days)
        self.assertTrue(len(set(res)), len(devs))
        self._no_same_bugman_in_a_row(res)

        devs = ['bob', 'mike']
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
        res = pick_bugmans(devs, days)
        self.assertTrue(len(set(res)), len(devs))
        self._no_same_bugman_in_a_row(res)

    def test_same_devs_as_working_days(self):
        devs = ['bob', 'mike', 'ernie', 'fred', 'pooh']
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
        res = pick_bugmans(devs, days)
        self.assertTrue(len(set(res)), len(devs))
        self._no_same_bugman_in_a_row(res)

    def test_one_dev_for_the_whole_week(self):
        devs = ['bob']
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
        res = pick_bugmans(devs, days)
        self.assertTrue(all(dev == 'bob' for dev in res))