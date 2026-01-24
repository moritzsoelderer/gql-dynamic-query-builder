import pytest

from core.helpers import (
    construct_operation_value_string,
    construct_where_clause_string,
    recursive_dict_merge,
)


class TestHelpers:
    @pytest.mark.parametrize(
        'value,operation,expected',
        [
            (1, '_eq', '_eq: 1'),
            ('1', '_eq', '_eq: "1"'),
            ('1', '_like', '_like: "%1%"'),
            ('1', '_ilike', '_ilike: "%1%"'),
        ],
    )
    def test_construct_operation_value_string(self, value, operation, expected):
        result = construct_operation_value_string(value, operation)
        assert result == expected

    def test_construct_where_clause_string(self):
        test_dict = {
            'A': {'A1': 'A1 {_eq: V1}'},
            'B': {
                'B1': {
                    'B11': 'B11 {_eq: V2}',
                    'B12': 'B13 {_eq: V3}',
                },
            },
            'C': 'C {_eq: V4}',
        }
        result = construct_where_clause_string(test_dict)

        assert (
            result
            == 'A: {A1 {_eq: V1}} B: {B1: {B11 {_eq: V2} B13 {_eq: V3}}} C {_eq: V4}'
        )

    def test_recursive_dict_merge(self):
        dict_to_merge_into = {
            'A': {'A1': 'A1 {_eq: V1}'},
            'B': {
                'B1': {
                    'B11': 'B11 {_eq: V2}',
                    'B12': 'B13 {_eq: V3}',
                },
            },
            'C': 'C {_eq: V4}',
        }

        dict_to_merge = {
            'A': 'A: {_eq: V0}',
            'B': {
                'B1': {
                    'B13': 'B11 {_eq: V5}',
                    'B14': {'B141': 'B141 {_eq: V6}'},
                },
            },
            'C': {'C1': 'C1 {_gt: V7'},
        }

        ### A and C being overwritten should not be a problem, as only 'primitive' types should be comparable
        ### either A and C are primitive or they have primitive attributes that can be used to filter the query
        ### but not both
        expected = {
            'A': 'A: {_eq: V0}',
            'B': {
                'B1': {
                    'B11': 'B11 {_eq: V2}',
                    'B12': 'B13 {_eq: V3}',
                    'B13': 'B11 {_eq: V5}',
                    'B14': {'B141': 'B141 {_eq: V6}'},
                }
            },
            'C': {'C1': 'C1 {_gt: V7'},
        }
        result = recursive_dict_merge(dict_to_merge_into, dict_to_merge)

        assert result == expected
