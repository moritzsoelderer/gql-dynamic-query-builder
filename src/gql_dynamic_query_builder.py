from __future__ import annotations

from src.core.grammar.query import prepare_query_grammar


class GQLDynamicQueryBuilder:
    def __init__(self, query: str):
        self.query: str = query
        self.where_clauses: dict[str, str] = {}
        self.processed_query = query

    def with_where_clause(self, field_name: str, value: str | int | list, operation: str | list[str]):
        pass

    def with_where_clauses(self, clauses: dict[str, str], overwrite: bool = False) -> GQLDynamicQueryBuilder:
        if overwrite:
            self.where_clauses = dict(clauses)
        else:
            self.where_clauses.update(clauses)
        return self

    def build(self):
        for table_name, where_clauses in self.where_clauses.items():
            query_grammar = prepare_query_grammar(table_name, where_clauses)
            self.processed_query = query_grammar.transform_string(self.processed_query)
            print("Processed Query", self.processed_query)

        return self.processed_query


if __name__ == '__main__':
    query_with_where = """
        query ProductsQuery {
            products (where: {producer: {_eq: "lego"}}) {
                name
            }
        }
    """

    query_without_where = """
        query ProductsQuery {
            products () {
                name
            }
        }
    """

    query_with_where_and_limit = """
        query ProductsQuery {
            products (where: {producer: {_eq: "lego"}} limit: 10) {
                name
            }
        }
    """

    query_without_where_with_limit = """
        query ProductsQuery {
            resources (limit: 10) {
                price
            }
            products (limit: 10, order_by: asc,) {
                name
            }
        }
    """

    builder = GQLDynamicQueryBuilder(query_without_where_with_limit)
    builder = builder.with_where_clauses({"products": 'name: {_eq: "hasbro"}'})
    builder = builder.with_where_clauses({"resources": 'price: {_eq: 10}'})

    final_query = builder.build()
    print(final_query)