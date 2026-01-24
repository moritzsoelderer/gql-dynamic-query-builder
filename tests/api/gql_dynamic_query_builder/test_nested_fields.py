import pytest

from api.gql_dynamic_query_builder import GQLDynamicQueryBuilder
from tests.conftest import ALL_QUERIES, is_valid_gql


class TestGQLDynamicQueryBuilderNestedFields:
    @pytest.mark.parametrize('query,subquery_to_test', ALL_QUERIES)
    def test_build_with_api_where_clause_one_op_one_value_nested_field(
        self, query, subquery_to_test
    ):
        builder = GQLDynamicQueryBuilder(query)

        builder.with_where_clause(
            'subquery_to_test', 'subquery_to_test_body_arg.name', 'test', '_eq'
        )
        result = builder.build()

        assert subquery_to_test not in result
        assert 'subquery_to_test_body_arg: {name: {_eq: "test"}}' in result
        assert is_valid_gql(result)

    @pytest.mark.parametrize('query,subquery_to_test', ALL_QUERIES)
    def test_build_with_api_where_clause_one_op_many_values_nested_field(
        self, query, subquery_to_test
    ):
        builder = GQLDynamicQueryBuilder(query)
        builder.with_where_clause(
            'subquery_to_test',
            'subquery_to_test_body_arg.name',
            ['test', 'hallo'],
            '_in',
        )
        result = builder.build()

        assert subquery_to_test not in result
        assert 'subquery_to_test_body_arg: {name: {_in: ["test", "hallo"]}}' in result
        assert is_valid_gql(result)

    @pytest.mark.parametrize('query,subquery_to_test', ALL_QUERIES)
    def test_build_with_api_where_clause_many_ops_one_value_nested_field(
        self, query, subquery_to_test
    ):
        builder = GQLDynamicQueryBuilder(query)

        with pytest.raises(TypeError):
            builder.with_where_clause(
                'subquery_to_test',
                'subquery_to_test_body_arg.name',
                'test',
                ['_in', '_eq'],
            )

    @pytest.mark.parametrize('query,subquery_to_test', ALL_QUERIES)
    def test_build_with_api_where_clause_many_ops_many_values_nested_field(
        self, query, subquery_to_test
    ):
        builder = GQLDynamicQueryBuilder(query)
        builder.with_where_clause(
            'subquery_to_test',
            'subquery_to_test_body_arg.name',
            ['test', 'hallo'],
            ['_gte', '_lt'],
        )
        result = builder.build()

        assert subquery_to_test not in result
        assert (
            'subquery_to_test_body_arg: {name: {_gte: "test" _lt: "hallo"}}' in result
        )
        assert is_valid_gql(result)

    @pytest.mark.parametrize('query,subquery_to_test', ALL_QUERIES)
    def test_build_with_api_where_clause_one_op_one_value_multiple_nested_fields(
        self, query, subquery_to_test
    ):
        builder = GQLDynamicQueryBuilder(query)

        builder.with_where_clause(
            'subquery_to_test', 'subquery_to_test_body_arg.name', 'test', '_eq'
        )
        builder.with_where_clause(
            'subquery_to_test',
            'subquery_to_test_body_arg.brand.name',
            'also_test',
            '_eq',
        )
        result = builder.build()

        assert subquery_to_test not in result
        assert (
            'subquery_to_test_body_arg: {name: {_eq: "test"} brand: {name: {_eq: "also_test"}}}'
            in result
        )
        assert is_valid_gql(result)

    @pytest.mark.parametrize('query,subquery_to_test', ALL_QUERIES)
    def test_build_with_api_where_clause_one_op_many_values_multiple_nested_fields(
        self, query, subquery_to_test
    ):
        builder = GQLDynamicQueryBuilder(query)
        builder.with_where_clause(
            'subquery_to_test',
            'subquery_to_test_body_arg.name',
            ['test', 'hallo'],
            '_in',
        )
        builder.with_where_clause(
            'subquery_to_test',
            'subquery_to_test_body_arg.brand.name',
            'also_test',
            '_eq',
        )
        result = builder.build()

        assert subquery_to_test not in result
        assert (
            'subquery_to_test_body_arg: {name: {_in: ["test", "hallo"]} brand: {name: {_eq: "also_test"}}}'
            in result
        )
        assert is_valid_gql(result)

    @pytest.mark.parametrize('query,subquery_to_test', ALL_QUERIES)
    def test_build_with_api_where_clause_many_ops_many_values_multiple_nested_fields(
        self, query, subquery_to_test
    ):
        builder = GQLDynamicQueryBuilder(query)
        builder.with_where_clause(
            'subquery_to_test',
            'subquery_to_test_body_arg.name',
            ['test', 'hallo'],
            ['_gte', '_lt'],
        )
        builder.with_where_clause(
            'subquery_to_test',
            'subquery_to_test_body_arg.brand.name',
            'also_test',
            '_eq',
        )
        result = builder.build()

        assert subquery_to_test not in result
        assert (
            'subquery_to_test_body_arg: {name: {_gte: "test" _lt: "hallo"} brand: {name: {_eq: "also_test"}}}'
            in result
        )
        assert is_valid_gql(result)
