"""
Here we use strategy pattern to parse different actions with different methods.
To specify which strategy to use for specific actions we use dictionary.
"""
import datetime
from abc import ABC, abstractmethod
from typing import List

from dict_diff_calculator import DictDiff


class IParse(ABC):
    @abstractmethod
    def parse(self, actions: List[dict], action_pos: int) -> str:
        pass


class AbstractActionParseStrategy(IParse, ABC):
    event_time_format: str = '%Y-%m-%dT%H:%M:%S.%fZ'
    output_time_format: str = '%Y-%m-%d %H:%M'

    def parse(self, actions: List[dict], action_pos: int) -> str:
        """
        Should be implemented in concrete classes.
        Returns formatted string, containing summary of an action.
        :param actions: list of history actions
        :param action_pos: list index of target action
        """
        raise NotImplementedError

    @staticmethod
    def get_action_user_name(action_data: dict) -> str:
        """
        Return user name.
        Defaults to 'System'.
        """
        username = 'System'
        user = action_data.get('user', None)

        if user is None:
            return username

        username = user.get('username', None)
        first_name = user.get('first_name', '')
        username = f'{username or first_name}'
        return username

    def get_action_formatted_time(self, action_data: dict) -> str:
        """
        Format event_time to more readable form.
        """
        time = datetime.datetime.strptime(
            action_data['event_time'],
            self.event_time_format
        )
        formatted_time = time.strftime(self.output_time_format)
        return '\t\t\t' + formatted_time


class TransitionActionParser(AbstractActionParseStrategy):
    def parse(self, actions: List[dict], action_pos: int) -> str:
        action_data = actions[action_pos]

        user_name = self.get_action_user_name(action_data)
        action_name = action_data['extra_data']['action_name']
        time = self.get_action_formatted_time(action_data)
        return f'({user_name})NEW ACTION: {action_name} {time}'


class CreateActionParser(AbstractActionParseStrategy):
    def parse(self, actions: List[dict], action_pos: int) -> str:
        action_data = actions[action_pos]

        time = self.get_action_formatted_time(action_data)
        user_name = self.get_action_user_name(action_data)
        header = f'({user_name})ORDER CREATED {time}\n'
        items = self.parse_items_list(action_data)
        return header + items

    @staticmethod
    def parse_items_list(action_data: dict) -> str:
        parsed_items = ''
        items = action_data['order_items']

        for item in items:
            parsed_items += f"\t {item['saved_product']['title']}  -{item['quantity']}+"

        return items


class UpdateActionParser(AbstractActionParseStrategy):
    def __init__(self, diff_calculator: DictDiff):
        self.diff_calculator = diff_calculator

    def parse(self, actions: List[dict], action_pos: int) -> str:
        action_data = actions[action_pos]
        previous_action_data = actions[action_pos - 1]

        time = self.get_action_formatted_time(action_data)
        user_name = self.get_action_user_name(action_data)

        parsed_diff = self.parse_diff(
            action_data,
            previous_action_data
        )
        header = f'({user_name})ORDER UPDATED {time}\n'
        return header + parsed_diff

    def parse_diff(
        self,
        action_data: dict,
        previous_action_data: dict
    ) -> str:
        parsed_diff = ''
        diff: dict = self.diff_calculator.compare(
            previous_action_data,
            action_data,
        )
        for key, item in diff.items():
            parsed_diff += f'\t{key}: {item}\n'
        return parsed_diff
