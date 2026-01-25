import pytest

from api.gql_dynamic_query_builder import GQLDynamicQueryBuilder
from tests.conftest import ALL_QUERIES, is_valid_gql


class TestGQLDynamicQueryBuilderOffset:
    @pytest.mark.parametrize('query,subquery_to_test', ALL_QUERIES)
    def test_limit(self, query, subquery_to_test):
        builder = GQLDynamicQueryBuilder(query)

        builder.with_offset('subquery_to_test', 10)
        result = builder.build()

        assert subquery_to_test not in result
        assert 'offset: 10' in result
        assert is_valid_gql(result)
