from __future__ import annotations

import json

from src.core.grammar.query import prepare_query_grammar


def create_key_value_pair(value: str | int | list, operation: str) -> str:
    if operation in ['_like', '_ilike']:
        value = f'"%{value}%"'
    elif isinstance(value, str):
        value = f'"{value}"'

    return f'{operation}: {value}'

def construct_where_clause_string(nested_anc_explicit_where_clauses: dict) -> str:
    opt_explicit_clause = nested_anc_explicit_where_clauses.get('explicit_clause', None)
    nested_field_clauses = [opt_explicit_clause] if opt_explicit_clause else []
    for key, value in nested_anc_explicit_where_clauses.items():
        if isinstance(value, dict):
            nested_field_clauses.append(f"{key}: {{{construct_where_clause_string(value)}}}")
        else:
            nested_field_clauses.append(value)

    return " ".join(nested_field_clauses)

class GQLDynamicQueryBuilder:
    def __init__(self, query: str):
        self.query: str = query
        self.where_clauses: dict[str, dict[str, dict | str]] = {}
        self.processed_query = query

    def update_where_clauses(self, table_name: str, field_name: str, clause: str) -> None:
        current_table_clauses = self.where_clauses[table_name] if self.where_clauses.get(table_name, None) else {}
        fields = field_name.split('.')

        clause_dict = {fields[-1]: f'{fields[-1]}: {clause}'}
        for field in fields[:-1]:
            clause_dict = {field: clause_dict}

        current_table_clauses.update(clause_dict)
        self.where_clauses[table_name] = current_table_clauses

    def with_where_clause(
        self, table_name: str, field_name: str, value: str | int | list[int] | list[str], operation: str | list[str], skip_if_none:bool = False
    ):
        if value is None:
            if skip_if_none:
                return self
            else:
                raise ValueError("Encountered None value in with_where_clause - if you want to skip it set skip_if_none=True")

        if isinstance(value, list):
            if isinstance(operation, list):
                pairs = [create_key_value_pair(v, o) for v, o in zip(value, operation, strict=True)]
                self.update_where_clauses(table_name, field_name, f'{{{" ".join(pairs)}}}')
            else:
                value = json.dumps(value)
                self.update_where_clauses(table_name, field_name, f'{{{operation}: {value}}}')
        else:
            if isinstance(operation, list):
                raise TypeError("Operation should be scalar if value is scalar")
            self.update_where_clauses(table_name, field_name, f'{{{create_key_value_pair(value, operation)}}}')

        return self


    def with_where_clauses(
        self, clauses: dict[str, str], overwrite: bool = False
    ) -> GQLDynamicQueryBuilder:
        if overwrite:
            transformed_clauses = {table_name: {'explicit_clause': clause} for table_name, clause in clauses.items()}
            self.where_clauses = transformed_clauses
        else:
            for table_name, clause in clauses.items():
                if self.where_clauses.get(table_name, None):
                    self.where_clauses[table_name].update({'explicit_clause': clause})
                else:
                    self.where_clauses.update({table_name: {'explicit_clause': clause}})
        return self

    def build(self):
        for table_name, nested_and_explicit_where_clauses in self.where_clauses.items():
            where_clauses = construct_where_clause_string(nested_and_explicit_where_clauses)
            query_grammar = prepare_query_grammar(table_name, where_clauses)
            self.processed_query = query_grammar.transform_string(self.processed_query)
            print('Processed Query', self.processed_query)

        return self.processed_query