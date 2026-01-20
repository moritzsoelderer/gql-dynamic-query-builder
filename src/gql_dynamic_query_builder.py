from __future__ import annotations

from pyparsing import Word, alphas, Literal, Forward, alphanums, Optional, QuotedString, Empty, \
    ZeroOrMore, ParseResults, nums, OneOrMore, Keyword, original_text_for

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
            # define where content grammar of the table query of interest
            recursive_where_part = Forward()
            value = QuotedString(quote_char='"', unquote_results=False) | (Literal('{') + recursive_where_part + Literal('}'))
            recursive_where_part <<= Word(alphas + '_') + Literal(':') + value
            where_content = ZeroOrMore(recursive_where_part)

            # define where content grammar of other table queries
            other_recursive_where_part = Forward()
            other_value = QuotedString(quote_char='"', unquote_results=False) | (
                        Literal('{') + other_recursive_where_part + Literal('}'))
            other_recursive_where_part <<= Word(alphas + '_') + Literal(':') + other_value
            other_where_content = ZeroOrMore(other_recursive_where_part)

            # define other table query parameter grammar (e.g. 'limit', 'order_by')
            other_table_query_parameter = ~Keyword('where') + Word(alphas + '_') + Literal(':') + (Word(alphanums) | QuotedString('"')) + Optional(Literal(','))

            # define where clause grammar of the table query of interest
            where_clause = Literal('where') + Literal(':') + Literal('{') + where_content + Literal('}')
            no_where_clause = Empty()
            table_query_grammar = (
                    Literal(table_name) +
                    Optional(
                        Literal('(') +
                        original_text_for(ZeroOrMore(other_table_query_parameter)) +
                        (where_clause | no_where_clause) +
                        original_text_for(ZeroOrMore(other_table_query_parameter)) + Literal(')')
                    ) +
                    Literal('{') +
                    OneOrMore(Word(alphanums)) +
                    Literal('}')
            )

            # define where clause grammar of other table queries
            other_where_clause = Literal('where') + Literal(':') + Literal('{') + other_where_content + Literal('}')
            other_no_where_clause = Empty()
            other_query_grammar = (
                    ~Keyword(table_name) +
                    Word(alphas + "_") +
                    Optional(
                        Literal('(') +
                        original_text_for(ZeroOrMore(other_table_query_parameter)) +
                        (other_where_clause | other_no_where_clause) +
                        original_text_for(ZeroOrMore(other_table_query_parameter)) +
                        Literal(')')
                    ) +
                    Literal('{') +
                    OneOrMore(Word(alphanums)) +
                    Literal('}')
            )

            # define parameters grammar for full query
            parameter = Literal('$') + Word(alphas + '_') + Literal(':') + Word(alphas)
            full_query_parameters = Literal('(') + OneOrMore(parameter) +Literal(')')

            # define full query
            full_query_grammar = (
                    original_text_for(Literal('query') +
                    Word(alphas + '_')) +
                    Optional(full_query_parameters) +
                    Literal('{') +
                    ZeroOrMore(other_query_grammar) +
                    table_query_grammar +
                    ZeroOrMore(other_query_grammar) +
                    Literal('}')
            )

            # define parse actions
            def extend_where_clauses(existing_where_clause: ParseResults) -> str:
                print(existing_where_clause)
                new_where_clause = ' ' + ''.join(existing_where_clause) + ''.join(where_clauses) + ' '
                print(new_where_clause)
                return new_where_clause

            def inject_new_where_clauses() -> str:
                print("no where clause")
                return ' where: {' + ''.join(where_clauses) + '} '

            # set parse actions for where clause of interest (existent and non-existent)
            where_content.set_parse_action(extend_where_clauses)
            no_where_clause.set_parse_action(inject_new_where_clauses)

            # parse and transform iteratively
            self.processed_query = full_query_grammar.transform_string(self.processed_query)
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

    builder = GQLDynamicQueryBuilder(query_with_where_and_limit)
    builder = builder.with_where_clauses({"products": 'name: {_eq: "hasbro"}'})
    builder = builder.with_where_clauses({"resources": 'price: {_eq: 10}'})

    final_query = builder.build()
    print(final_query)