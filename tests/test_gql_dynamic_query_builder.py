import pytest

from src.api.gql_dynamic_query_builder import GQLDynamicQueryBuilder
from tests.conftest import ALL_QUERIES


@pytest.mark.parametrize("query,subquery_to_test", ALL_QUERIES)
def test_build(query, subquery_to_test):
    builder = GQLDynamicQueryBuilder(query)

    builder.with_where_clauses({'subquery_to_test': 'subquery_to_test_body_arg: {_eq : "test"}'})
    result = builder.build()

    assert subquery_to_test not in result
    assert 'subquery_to_test_body_arg: {_eq : "test"}' in result