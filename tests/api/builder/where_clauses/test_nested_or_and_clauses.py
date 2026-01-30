import pytest

from gql_dynamic_query_builder.api.builder import GQLDynamicQueryBuilder
from tests.conftest import ALL_QUERIES, is_valid_gql, normalize


class TestGQLDynamicQueryBuilderNestedOrAndClauses:
    @pytest.mark.parametrize('query,subquery_to_test', ALL_QUERIES)
    def test_build_nested_or_first_level_clause(self, query, subquery_to_test):
        builder = GQLDynamicQueryBuilder(query)

        builder.with_where_clause(
            'subquery_to_test',
            ('subquery_to_test_body_arg_1', 'subquery_to_test_body_arg_2'),
            ('test_1', 'test_2'),
            ('_eq', '_gt'),
            wrap_in_or=True,
        )
        result = builder.build()

        expected = """
            _or: [
                {subquery_to_test_body_arg_1: {_eq: "test_1"}}
                {subquery_to_test_body_arg_2: {_gt: "test_2"}}
                ]
        """

        assert subquery_to_test not in result
        assert normalize(expected) in normalize(result)
        assert is_valid_gql(result)

    @pytest.mark.parametrize('query,subquery_to_test', ALL_QUERIES)
    def test_build_nested_or_and_second_level_clause(self, query, subquery_to_test):
        builder = GQLDynamicQueryBuilder(query)

        builder.with_where_clause(
            'subquery_to_test',
            (
                'subquery_to_test_body_arg_1',
                ('subquery_to_test_body_arg_2', 'subquery_to_test_body_arg_3'),
            ),
            ('test_1', ('test_2', 'test_3')),
            ('_eq', ('_gt', '_lte')),
            wrap_in_or=True,
        )
        result = builder.build()

        expected = """
            _or: [
                {subquery_to_test_body_arg_1: {_eq: "test_1"}}
                {_and: [
                    {subquery_to_test_body_arg_2: {_gt: "test_2"}}
                    {subquery_to_test_body_arg_3: {_lte: "test_3"}}
                    ]
                }
            ]
        """

        assert subquery_to_test not in result
        assert normalize(expected) in normalize(result)
        assert is_valid_gql(result)

    @pytest.mark.parametrize('query,subquery_to_test', ALL_QUERIES)
    def test_build_nested_or_and_third_level_clause(self, query, subquery_to_test):
        builder = GQLDynamicQueryBuilder(query)

        builder.with_where_clause(
            'subquery_to_test',
            (
                'subquery_to_test_body_arg_1',
                (
                    ('subquery_to_test_body_arg_2', 'subquery_to_test_body_arg_3'),
                    'subquery_to_test_body_arg_4',
                ),
            ),
            ('test_1', (('test_2', ['test_3', "test_4"]), ['test_5', 'test_6'])),
            ('_eq', (('_gt', ['_lte', '_gte']), '_in')),
            wrap_in_or=True,
        )
        result = builder.build()

        expected = """
            _or: [
                {subquery_to_test_body_arg_1: {_eq: "test_1"}}
                {_and: [
                     {_or: [
                            {subquery_to_test_body_arg_2: {_gt: "test_2"}}
                            {subquery_to_test_body_arg_3: {_lte: "test_3" _gte: "test_4"}}
                        ]}
                        {subquery_to_test_body_arg_4: {_in: ["test_5", "test_6"]}}
                    ]
                }
            ]
        """

        assert subquery_to_test not in result
        assert normalize(expected) in normalize(result)
        assert is_valid_gql(result)
