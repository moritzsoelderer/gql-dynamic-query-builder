import pytest

from gql_dynamic_query_builder.api.builder import GQLDynamicQueryBuilder
from tests.conftest import ALL_QUERIES, is_valid_gql


class TestGQLDynamicQueryBuilderLimit:
    @pytest.mark.parametrize('query,subquery_to_test', ALL_QUERIES)
    def test_limit(self, query, subquery_to_test):
        builder = GQLDynamicQueryBuilder(query)

        builder.with_limit('subquery_to_test', 15)
        result = builder.build()

        assert subquery_to_test not in result
        assert 'limit: 15' in result
        assert is_valid_gql(result)
