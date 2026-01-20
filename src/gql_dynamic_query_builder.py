from __future__ import annotations

from pyparsing import Word, alphas, Literal, Forward, alphanums, Optional, QuotedString, Empty, \
    ZeroOrMore, ParseResults, nums


class GQLDynamicQueryBuilder:
    def __init__(self, query: str):
        self.query: str = query
        self.where_clauses: dict[str, str] = {}

    def with_where_clause(self, field_name: str, value: str | int | list, operation: str | list[str]):
        pass

    def with_where_clauses(self, clauses: dict[str, str], overwrite: bool = False) -> GQLDynamicQueryBuilder:
        new_clauses = self.where_clauses.update(clauses) if overwrite else clauses
        self.where_clauses = new_clauses
        return self

    def build(self):
        for table_name, where_clauses in self.where_clauses.items():
            ### initialize grammar
            recursive_grammar = Forward()
            value = QuotedString(quote_char='"', unquote_results=False) | (Literal('{') + recursive_grammar + Literal('}'))
            recursive_grammar <<= Word(alphas + '_') + Literal(':') + value

            where_content = ZeroOrMore(recursive_grammar)
            where_clause = Literal('where') + Literal(':') + Literal('{') + where_content + Literal('}')
            limit_clause = Optional(Literal('limit') + Literal(':') + Word(nums))
            no_where_clause = Empty()

            query_grammar = Literal(table_name) + Literal('(') + (where_clause | no_where_clause) + limit_clause + Literal(')') + Literal('{') + Word(alphanums) + Literal('}')

            def extend_where_clauses(existing_where_clause: ParseResults) -> str:
                print(existing_where_clause)
                new_where_clause = ''.join(existing_where_clause) + ''.join(where_clauses)
                print(new_where_clause)
                return new_where_clause

            def inject_new_where_clauses() -> str:
                print("no where clause")
                return 'where: {' + ''.join(where_clauses) + '}'



            ### set parse actions
            where_content.set_parse_action(extend_where_clauses)
            no_where_clause.set_parse_action(inject_new_where_clauses)
            ### parse and transform
            print(self.query)
            return query_grammar.transform_string(self.query)


if __name__ == '__main__':
    query_with_where = """
        products (where: {producer: {_eq: "lego"}}) {
            name
        }
    """

    query_without_where = """
        products () {
            name
        }
    """

    query_with_where_and_limit = """
        products (where: {producer: {_eq: "lego"}} limit: 10) {
            name
        }
    """

    query_without_where_with_limit = """
        products (limit: 10) {
            name
        }
    """

    builder = GQLDynamicQueryBuilder(query_without_where_with_limit)
    builder = builder.with_where_clauses({"products": 'name: {_eq: "hasbro"}'})

    final_query = builder.build()
    print(final_query)