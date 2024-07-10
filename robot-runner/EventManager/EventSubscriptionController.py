from typing import Callable, List, Tuple
from EventManager.Models.RobotRunnerEvents import RobotRunnerEvents

class EventSubscriptionController:
    __call_back_register = dict()

    @staticmethod
    def subscribe_to_single_event(event: RobotRunnerEvents, callback_methods: List[Callable]):
            EventSubscriptionController.__call_back_register[event] = callback_methods

    @staticmethod
    def subscribe_to_multiple_events(subscriptions: List[Tuple[RobotRunnerEvents, Callable]]):
        for sub in subscriptions:
            event, callback = sub[0], List[sub[1]]
            EventSubscriptionController.subscribe_to_single_event(event, callback)

    @staticmethod
    def subscribe_to_multiple_events_multiple_callbacks(subscriptions: List[Tuple[RobotRunnerEvents, List[Callable]]]):
        for sub in subscriptions:
            event, callbacks = sub[0], sub[1]
            EventSubscriptionController.subscribe_to_single_event(event, callbacks)

    @staticmethod
    def raise_event(event: RobotRunnerEvents, robot_runner_context = None):
        event_callbacks = []
        try:
            event_callbacks = EventSubscriptionController.__call_back_register[event]
        except KeyError:
            return None

        for event_callback in event_callbacks:
            if robot_runner_context:
                event_callback(robot_runner_context)
            else:
                event_callback()

    @staticmethod
    def get_event_callback(event: RobotRunnerEvents):
        try:
            return EventSubscriptionController.__call_back_register[event]
        except KeyError:
            return None
