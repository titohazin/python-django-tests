import unittest
from .notification import Notification


class NotificationsUnitTests(unittest.TestCase):

    def test_notification_add_messages(self):
        notification = Notification()
        with self.assertRaises(TypeError) as assert_error:
            notification.add_message()
            self.assertTrue(
                "'context' and 'message'" in assert_error.exception.args[0])
        self.assertEqual(notification.messages, {})
        notification.add_message('info', 'foo')
        notification.add_message('info', 'bar')
        notification.add_message('warning', 'foobar')
        self.assertEqual(notification.messages, {
            'info': ['foo', 'bar'],
            'warning': ['foobar']
        })

    def test_notification_remove_messages(self):
        notification = Notification()
        with self.assertRaises(TypeError) as assert_error:
            notification.remove_message()
            self.assertTrue(
                "'context' and 'message'" in assert_error.exception.args[0])
        notification.add_message('info', 'foobar')
        notification.remove_message('fake', 'foobar')
        notification.remove_message('info', 'fake')
        notification.remove_message('fake', 'fake')
        self.assertEqual(notification.messages, {'info': ['foobar']})
        notification.remove_message('info', 'foobar')
        self.assertEqual(notification.messages, {'info': []})

    def test_notification_clear_messages(self):
        notification = Notification()
        notification.add_message('info', 'foo')
        notification.add_message('info', 'bar')
        notification.add_message('warning', 'foobar')
        self.assertEqual(notification._Notification__temp, ['foobar'])
        self.assertEqual(notification.messages, {
            'info': ['foo', 'bar'],
            'warning': ['foobar']
        })
        notification.clear('info')
        self.assertEqual(notification.messages, {'warning': ['foobar']})
        self.assertEqual(notification._Notification__temp, [])
        notification.add_message('info', 'foo')
        notification.add_message('info', 'bar')
        self.assertEqual(notification._Notification__temp, ['foo', 'bar'])
        notification.clear()
        self.assertEqual(notification.messages, {})
        self.assertEqual(notification._Notification__temp, [])

    def test_notification_messages_filter(self):
        notification = Notification()
        with self.assertRaises(TypeError) as assert_error:
            notification.messages_filter()
            self.assertTrue('context' in assert_error.exception.args[0])
        notification.add_message('info', 'foo')
        notification.add_message('info', 'bar')
        notification.add_message('warning', 'foobar')
        self.assertIsInstance(notification.messages_filter('info'), Notification)
        self.assertEqual(notification._Notification__temp, ['foo', 'bar'])
        notification.messages_filter('fake')
        self.assertEqual(notification._Notification__temp, [])

    def test_notification_messages_filter_to_str(self):
        notification = Notification()
        notification.add_message('info', 'foo')
        notification.add_message('info', 'bar')
        notification.add_message('warning', 'foobar')
        self.assertEqual(
            notification.messages_filter('fake').to_str(), '')
        self.assertEqual(
            notification.messages_filter('info').to_str(), 'foo\nbar')
        self.assertEqual(
            notification.messages_filter('info').to_str(separator=';'), 'foo;bar')
        self.assertEqual(
            notification.messages_filter('info').to_str(end='!'), 'foo\nbar!')
        self.assertEqual(
            notification.messages_filter('info').to_str(';', '!'), 'foo;bar!')

    def test_notification_messages_filter_to_list(self):
        notification = Notification()
        notification.add_message('info', 'foo')
        notification.add_message('info', 'bar')
        notification.add_message('warning', 'foobar')
        self.assertEqual(
            notification.messages_filter('fake').to_list(), [])
        self.assertEqual(
            notification.messages_filter('info').to_list(), ['foo', 'bar'])
