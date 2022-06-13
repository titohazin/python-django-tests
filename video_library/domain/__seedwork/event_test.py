from abc import ABC
from dataclasses import is_dataclass
from datetime import datetime
import unittest
from unittest.mock import patch

from .event import EventDispatcher, EventHandlerInterface, EventInterface


class EventInterfaceUnitTests(unittest.TestCase):

    def test_if_is_a_data_class(self):
        self.assertTrue(is_dataclass(EventInterface))

    def test_if_is_a_abstract_class(self):
        event_interface = EventInterface()
        self.assertIsInstance(event_interface, ABC)

    def test_init_properties(self):
        event = EventInterface()
        self.assertIsNotNone(event.occurred_at)
        self.assertIsInstance(event.occurred_at, datetime)
        self.assertIsNone(event.event_data)
        test_occurred_at = datetime.now()
        test_data = {'foo': 'bar'}
        event = EventInterface(test_data, test_occurred_at)
        self.assertEqual(event.occurred_at, test_occurred_at)
        self.assertEqual(event.event_data, test_data)


class EventHandlerInterfaceUnitTests(unittest.TestCase):

    def test_if_is_a_abstract_class_and_methods(self):
        with self.assertRaises(TypeError) as assert_error:
            EventHandlerInterface()
        self.assertEqual(assert_error.exception.args[0], "Can't instantiate " +  # noqa: W504
                         "abstract class EventHandlerInterface with abstract method handle")


class EventStub(EventInterface):
    pass


class EventHandlerStub(EventHandlerInterface):

    result = str

    def handle(self, event: EventStub) -> None:
        self.result = f'[{event.occurred_at.__str__()}] {event.event_data}'


class EventDispatcherInterfaceUnitTests(unittest.TestCase):

    sing_dispatcher = EventDispatcher.instance

    def test_if_dispatcher_initializes_with_empty_handlers(self):
        self.assertEqual(EventDispatcher.instance._handlers, {})

    def test_if_is_a_singleton(self):
        with self.assertRaises(TypeError) as assert_error:
            EventDispatcher()
        self.assertTrue("EventDispatcher can not be instantiated" in
                        assert_error.exception.args[0])
        self.assertIsNotNone(self.sing_dispatcher)
        self.assertIsInstance(self.sing_dispatcher, EventDispatcher)
        self.sing_dispatcher._handlers = {'foobar': []}
        self.assertEqual(
            self.sing_dispatcher._handlers,
            EventDispatcher.instance._handlers
        )

    def test_dispatcher_register_and_unregister_handlers(self):
        self.sing_dispatcher._handlers = {}
        foo_handler_test = EventHandlerStub()
        bar_handler_test = EventHandlerStub()
        self.sing_dispatcher.register('EventHandlerStub', foo_handler_test)
        self.sing_dispatcher.register('EventHandlerStub', bar_handler_test)
        self.assertEqual(
            self.sing_dispatcher._handlers,
            {'EventHandlerStub': [foo_handler_test, bar_handler_test]}
        )
        self.sing_dispatcher.unregister('EventHandlerStub', foo_handler_test)
        self.assertEqual(
            self.sing_dispatcher._handlers,
            {'EventHandlerStub': [bar_handler_test]}
        )
        self.sing_dispatcher.unregister_all()
        self.assertEqual(self.sing_dispatcher._handlers, {})

    def test_dispatcher_notify_method(self):
        handler = EventHandlerStub()
        with patch.object(EventHandlerStub, 'handle', wraps=handler.handle) as spy_handle:
            self.sing_dispatcher.register('EventStub', handler)
            occurred_at = datetime.now()
            data = {'foo': 'bar'}
            event = EventStub(data, occurred_at)
            self.sing_dispatcher.notify(event)
            self.assertEqual(handler.result, f'[{occurred_at.__str__()}] {data}')
            spy_handle.assert_called_once()
