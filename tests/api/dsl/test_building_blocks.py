import pytest

from gql_dynamic_query_builder.api.builder import GQLDynamicQueryBuilder
from gql_dynamic_query_builder.api.dsl.query import dynamic_query
from tests.conftest import ALL_QUERIES


class TestDSLBehavesAsBuilder:
    @pytest.mark.parametrize('query,subquery_to_test', ALL_QUERIES)
    def test_l(self, query, subquery_to_test):
        result_dsl = (dynamic_query(query).table('subquery_to_test')
                  .where('test', is_optional=True).
                  _in(['a', 'b', 'c'])
                  .offset(15)
                  .limit(25)
                  .where('test2')
                  ._gte(5)
                  .build()
                  )

        result_builder = (GQLDynamicQueryBuilder(query)
                          .with_where_clause('subquery_to_test', 'test', ['a', 'b', 'c'], '_in')
                          .with_offset('subquery_to_test', 15)
                          .with_limit('subquery_to_test', 25)
                          .with_where_clause('subquery_to_test', 'test2', 5, '_gte')
                          ).build()

        assert result_dsl == result_builder
