import pytest

from gql_dynamic_query_builder.api.dsl.query import _and, _or, dynamic_query, where
from tests.conftest import ALL_QUERIES, is_valid_gql, normalize


class TestDSLNestedOrAndClauses:
    @pytest.mark.parametrize('query,subquery_to_test', ALL_QUERIES)
    def test_dsl_build_nested_or_and_third_level_clause(self, query, subquery_to_test):
        result = (
            dynamic_query(query)
            .table('subquery_to_test')
            ._or(
                [
                    _and((where('test')._eq(1), where('test2')._eq(2))),
                    _or((where('test3')._eq(3), where('test4')._eq(4))),
                    where('test5')._eq(5),
                ]
            )
            .build()
        )

        expected = """
            _or: [
                    {_and: [
                            {test: {_eq: 1}}
                            {test2: {_eq: 2}}
                        ]
                    } 
                    {test3: {_eq: 3}}
                    {test4: {_eq: 4}}
                    {test5: {_eq: 5}}
                ]
        """
        assert subquery_to_test not in result
        assert normalize(expected) in normalize(result)
        assert is_valid_gql(result)

    @pytest.mark.parametrize('query,subquery_to_test', ALL_QUERIES)
    def test_dsl_build_nested_or_and_third_level_clause_with_none(
        self, query, subquery_to_test
    ):
        result = (
            dynamic_query(query)
            .table('subquery_to_test')
            ._or(
                [
                    _and(
                        (
                            where('test')._eq(1),
                            where('test2', is_optional=True)._eq(None),
                        )
                    ),
                    _or((where('test3')._eq(3), where('test4')._eq(4))),
                    where('test5')._eq(5),
                ]
            )
            .build()
        )

        expected = """
            _or: [
                    {_and: [
                            {test: {_eq: 1}}
                        ]
                    } 
                    {test3: {_eq: 3}}
                    {test4: {_eq: 4}}
                    {test5: {_eq: 5}}
                ]
        """
        assert subquery_to_test not in result
        assert normalize(expected) in normalize(result)
        assert is_valid_gql(result)
