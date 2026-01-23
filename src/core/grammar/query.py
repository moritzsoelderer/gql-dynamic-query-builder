from pyparsing import Literal, Word, alphas, ZeroOrMore, Optional, Keyword, \
    ParserElement, OneOrMore, original_text_for, Empty

from src.core.grammar.subquery import get_table_specific_subquery, GENERIC_SUBQUERY
from src.core.grammar.where_clause import get_new_where_clause_and_content
from src.core.grammar.parse_actions import extend_where_clauses, inject_new_where_clauses


QUERY_KEYWORD_AND_NAME = original_text_for(Literal('query') + Word(alphas + '_'))
QUERY_PARAMETER = Literal('$') + Word(alphas + '_') + Literal(':') + Word(alphas)
QUERY_PARAMETER_SECTION = Literal('(') + OneOrMore(QUERY_PARAMETER) + Literal(')')


def prepare_query_grammar(table_name: str, where_clauses: str) -> ParserElement:
    where_clause, recursive_where_condition = get_new_where_clause_and_content()
    no_where_clause = Empty()

    table_subquery = get_table_specific_subquery(table_name, where_clause | no_where_clause)
    other_subqueries = ~Keyword(table_name) + GENERIC_SUBQUERY.copy()

    recursive_where_condition.set_parse_action(lambda tokens: extend_where_clauses(tokens, where_clauses))
    no_where_clause.set_parse_action(lambda: inject_new_where_clauses(where_clauses))

    return (
            QUERY_KEYWORD_AND_NAME.copy() +
            Optional(QUERY_PARAMETER_SECTION.copy()) +
            Literal('{') +
            ZeroOrMore(other_subqueries) +
            table_subquery +
            ZeroOrMore(other_subqueries) +
            Literal('}')
    )