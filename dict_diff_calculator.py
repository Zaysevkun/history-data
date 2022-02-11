from abc import ABC, abstractmethod


class ICompare(ABC):
    @abstractmethod
    def compare(
        self,
        initial_dict: dict,
        compared_dict: dict,
    ) -> dict:
        """
        Compares two dicts and returns dict with differing fields.
        """
        pass


class DictDiff(ICompare):
    def compare(
        self,
        initial_dict: dict,
        compared_dict: dict
    ) -> dict:
        """
        Calculate diff of basic items in dicts, then add nested items diff to it.
        """
        nested_items_diff = self._compare_nested_items(
            initial_dict,
            compared_dict
        )

        initial_set = set(initial_dict.items())
        compared_set = set(compared_dict.items())
        items_diff = dict(compared_set - initial_set)

        items_diff.update(nested_items_diff)
        return items_diff

    def _compare_nested_items(
        self,
        initial_dict: dict,
        compared_dict: dict
    ) -> dict:
        """
        Nested dict comparison was purposefully simplified for more clearer,
        information in history representation.
        """
        nested_items_diff = {}

        initial_nested_items = self._pop_nested_items(initial_dict)
        compared_nested_items = self._pop_nested_items(compared_dict)

        for key in initial_nested_items.keys():
            if initial_nested_items[key] != compared_nested_items.get(key, {}):
                nested_items_diff[key] = 'updated'

        return nested_items_diff

    @staticmethod
    def _pop_nested_items(target: dict) -> dict:
        """
        Method removes nested items from target and returns dict them.
        """
        target_copy = target.copy()
        nested_items = {
            key: target.pop(key)
            for key, value in target_copy.items()
            if isinstance(value, dict)
        }
        return nested_items
