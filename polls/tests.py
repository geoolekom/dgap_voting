from django.test import TestCase
from polls.models import Poll, Choice
from profiles.models import UserProfile
from django.contrib.auth.models import User
from django.utils import timezone
from django.test.utils import override_settings


@override_settings(DEBUG=True)  # In order to the one user can vote repeatedly
class PollTestCase(TestCase):
    def _check_results(self, choices, results):
        """
        Parameters
        ----------
        results: list-like objects
        """
        for choice, result in zip(choices, results):
            choice.refresh_from_db()
            self.assertEqual(choice.votes, result)

    def _common_test_for_ONE_and_MANY(self, poll, choices):
        response = self.client.post(
            '/polls/%s/vote/' % poll.id, {},
            follow=True
        )

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual('Вы не выбрали вариант ответа',
                         str(messages[0]))
        self._check_results(choices, [0, 0, 0])

        response = self.client.post(
            '/polls/%s/vote/' % poll.id, {'choice': choices[0].id},
            follow=True
        )

        self._check_results(choices, [1, 0, 0])

        response = self.client.post(
            '/polls/%s/vote/' % poll.id, {'choice': [choices[1].id] * 5},
            follow=True
        )

        self._check_results(choices, [1, 1, 0])
        self._last_results = [1, 1, 0]

    def setUp(self):
        User.objects.create_user(username='john',
                                 password='johnpassword',
                                 email='lennon@thebeatles.com')
        user = User.objects.get(username='john')
        user.userprofile.is_approved = True
        user.userprofile.room = '000'
        user.userprofile.group = '429'
        user.is_staff = True
        user.userprofile.save()
        user.save()

        self.client.login(username='john', password='johnpassword')

    def test_vote_answer_type_ONE(self):
        Poll.objects.create(
            name='Test_ONE', question='question1',
            begin_date=timezone.now(),
            end_date=timezone.now()+timezone.timedelta(minutes=1),
            answer_type='ONE'
        )

        poll = Poll.objects.get(name='Test_ONE')
        poll.choice_set.add(Choice(choice_text='ans1', created=timezone.now()))
        poll.choice_set.add(Choice(choice_text='ans2', created=timezone.now()))
        poll.choice_set.add(Choice(choice_text='ans3', created=timezone.now()))

        choices = poll.get_ordered_choices()

        self._common_test_for_ONE_and_MANY(poll, choices)

        response = self.client.post(
            '/polls/%s/vote/' % poll.id,
            {
                'choice': [choices[1].id, choices[2].id],
            },
            follow=True
        )

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual('Вы должны выбрать один вариант ответа',
                         str(messages[0]))
        self._check_results(choices, self._last_results)

    def test_vote_answer_type_MANY(self):
        Poll.objects.create(
            name='Test_MANY', question='question1',
            begin_date=timezone.now(),
            end_date=timezone.now()+timezone.timedelta(minutes=1),
            answer_type='MANY'
        )

        poll = Poll.objects.get(name='Test_MANY')
        poll.choice_set.add(Choice(choice_text='ans1', created=timezone.now()))
        poll.choice_set.add(Choice(choice_text='ans2', created=timezone.now()))
        poll.choice_set.add(Choice(choice_text='ans3', created=timezone.now()))

        choices = poll.get_ordered_choices()

        self._common_test_for_ONE_and_MANY(poll, choices)

        response = self.client.post(
            '/polls/%s/vote/' % poll.id,
            {
                'choice': [choices[1].id, choices[2].id],
            },
            follow=True
        )
        results = self._last_results
        results[1] += 1
        results[2] += 1

        self._check_results(choices, results)

        response = self.client.post(
            '/polls/%s/vote/' % poll.id,
            {
                'choice': [choices[1].id, choices[1].id,
                           choices[0].id],
            },
            follow=True
        )
        results = self._last_results
        results[1] += 1
        results[0] += 1

        self._check_results(choices, results)
