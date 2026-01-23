from __future__ import annotations

import json

from src.core.grammar.query import prepare_query_grammar


def create_key_value_pair(value: str | int | list, operation: str) -> str:
    if operation in ['_like', '_ilike']:
        value = f'"%{value}%"'
    elif isinstance(value, str):
        value = f'"{value}"'

    return f'{operation}: {value}'


class GQLDynamicQueryBuilder:
    def __init__(self, query: str):
        self.query: str = query
        self.where_clauses: dict[str, str] = {}
        self.processed_query = query

    def with_where_clause(
        self, table_name: str, field_name: str, value: str | int | list[int] | list[str], operation: str | list[str]
    ):
        if isinstance(value, list):
            if isinstance(operation, list):
                pairs = [create_key_value_pair(v, o) for v, o in zip(value, operation, strict=True)]
                self.where_clauses[table_name] = f'{field_name}: {{{" ".join(pairs)}}}'
            else:
                value = json.dumps(value)
                self.where_clauses[table_name] = f'{field_name}: {{{operation}: {value}}}'
        else:
            if isinstance(operation, list):
                raise TypeError("Operation should be scalar if value is scalar")

            self.where_clauses[table_name] = f'{field_name}: {{{create_key_value_pair(value, operation)}}}'

        return self


    def with_where_clauses(
        self, clauses: dict[str, str], overwrite: bool = False
    ) -> GQLDynamicQueryBuilder:
        if overwrite:
            self.where_clauses = dict(clauses)
        else:
            self.where_clauses.update(clauses)
        return self

    def build(self):
        for table_name, where_clauses in self.where_clauses.items():
            query_grammar = prepare_query_grammar(table_name, where_clauses)
            self.processed_query = query_grammar.transform_string(self.processed_query)
            print('Processed Query', self.processed_query)

        return self.processed_query