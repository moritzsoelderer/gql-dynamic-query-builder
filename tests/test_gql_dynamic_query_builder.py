import pytest

from src.api.gql_dynamic_query_builder import GQLDynamicQueryBuilder
from tests.conftest import ALL_QUERIES

class TestGQLDynamicQueryBuilder:

    @pytest.mark.parametrize("query,subquery_to_test", ALL_QUERIES)
    def test_build_with_explicit_where_clauses(self, query, subquery_to_test):
        builder = GQLDynamicQueryBuilder(query)

        builder.with_where_clauses({'subquery_to_test': 'subquery_to_test_body_arg: {_eq : "test"}'})
        result = builder.build()

        assert subquery_to_test not in result
        assert 'subquery_to_test_body_arg: {_eq : "test"}' in result


    @pytest.mark.parametrize("query,subquery_to_test", ALL_QUERIES)
    def test_build_with_api_where_clause_one_op_one_value(self, query, subquery_to_test):
        builder = GQLDynamicQueryBuilder(query)

        builder.with_where_clause('subquery_to_test', 'subquery_to_test_body_arg', 'test', '_eq')
        result = builder.build()

        assert subquery_to_test not in result
        assert 'subquery_to_test_body_arg: {_eq: "test"}' in result


    @pytest.mark.parametrize("query,subquery_to_test", ALL_QUERIES)
    def test_build_with_api_where_clause_one_op_many_values(self, query, subquery_to_test):
        builder = GQLDynamicQueryBuilder(query)
        builder.with_where_clause('subquery_to_test', 'subquery_to_test_body_arg', ['test', 'hallo'], '_in')
        result = builder.build()

        assert subquery_to_test not in result
        assert 'subquery_to_test_body_arg: {_in: ["test", "hallo"]}' in result


    @pytest.mark.parametrize("query,subquery_to_test", ALL_QUERIES)
    def test_build_with_api_where_clause_many_ops_one_value(self, query,subquery_to_test):
        builder = GQLDynamicQueryBuilder(query)

        with pytest.raises(TypeError):
            builder.with_where_clause('subquery_to_test', 'subquery_to_test_body_arg', 'test', ['_in', '_eq'])


    @pytest.mark.parametrize("query,subquery_to_test", ALL_QUERIES)
    def test_build_with_api_where_clause_many_ops_many_values(self, query,subquery_to_test):
        builder = GQLDynamicQueryBuilder(query)
        builder.with_where_clause('subquery_to_test', 'subquery_to_test_body_arg', ['test', 'hallo'], ['_gte', '_lt'])
        result = builder.build()

        assert subquery_to_test not in result
        assert 'subquery_to_test_body_arg: {_gte: "test" _lt: "hallo"}' in result