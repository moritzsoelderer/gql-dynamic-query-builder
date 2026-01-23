from pyparsing import (
    Keyword,
    Literal,
    OneOrMore,
    Optional,
    ParserElement,
    QuotedString,
    Word,
    ZeroOrMore,
    alphanums,
    alphas,
    original_text_for,
)

from src.core.grammar.where_clause import WHERE_CLAUSE

SUBQUERY_FILTERS_EXCLUDING_WHERE_CLAUSE = (
    ~Keyword('where')
    + Word(alphas + '_')
    + Literal(':')
    + (Word(alphanums) | QuotedString('"'))
    + Optional(Literal(','))
)

PRECEDING_SUBQUERY_FILTERS_EXCLUDING_WHERE_CLAUSE = Literal('(') + original_text_for(
    ZeroOrMore(SUBQUERY_FILTERS_EXCLUDING_WHERE_CLAUSE.copy())
)

FOLLOWING_SUBQUERY_FILTERS_EXCLUDING_WHERE_CLAUSE = original_text_for(
    ZeroOrMore(SUBQUERY_FILTERS_EXCLUDING_WHERE_CLAUSE.copy())
) + Literal(')')

GENERIC_SUBQUERY_BODY = Literal('{') + OneOrMore(Word(alphanums)) + Literal('}')

GENERIC_SUBQUERY = (
    Word(alphas + '_')
    + Optional(
        PRECEDING_SUBQUERY_FILTERS_EXCLUDING_WHERE_CLAUSE.copy()
        + Optional(WHERE_CLAUSE.copy())
        + FOLLOWING_SUBQUERY_FILTERS_EXCLUDING_WHERE_CLAUSE.copy()
    )
    + GENERIC_SUBQUERY_BODY.copy()
)


def get_table_specific_subquery(
    table_name: str, where_clause: ParserElement
) -> ParserElement:
    return (
        Literal(table_name)
        + Optional(
            PRECEDING_SUBQUERY_FILTERS_EXCLUDING_WHERE_CLAUSE.copy()
            + where_clause
            + FOLLOWING_SUBQUERY_FILTERS_EXCLUDING_WHERE_CLAUSE.copy()
        )
        + GENERIC_SUBQUERY_BODY.copy()
    )
