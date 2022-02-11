from typing import Dict

from actions_pasing_strategies import (
    TransitionActionParser,
    UpdateActionParser,
    CreateActionParser, IParse
)
from dict_diff_calculator import DictDiff
from file_reader import read_json_from_file


def main():
    # read from file
    json_data = read_json_from_file(
        input() or 'sample1'
    )
    # get results list
    history_events = json_data['results']

    # dict mapping event_type: parsing strategy
    action_parsing_strategies: Dict[str, IParse] = {
        'created': CreateActionParser(),
        'updated': UpdateActionParser(DictDiff()),
        'transition': TransitionActionParser(),
    }
    # write to console based on action type
    # create - basic write with order items list
    # transition - basic write with transition name
    # update - check update fields and write
    for pos, event in enumerate(history_events):
        event_type = event['event_type']
        parsing_class = action_parsing_strategies[event_type]
        print(parsing_class.parse(history_events, pos), '\n')


if __name__ == '__main__':
    main()
