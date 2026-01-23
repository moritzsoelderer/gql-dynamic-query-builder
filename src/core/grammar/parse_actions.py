### These functions are used as parse actions for matches
from pyparsing import ParseResults


def extend_where_clauses(existing_where_clause: ParseResults, where_clauses: str) -> str:
    print(existing_where_clause)
    new_where_clause = ' ' + ''.join(existing_where_clause) + ''.join(where_clauses) + ' '
    print(new_where_clause)
    return new_where_clause


def inject_new_where_clauses(where_clauses) -> str:
    print("no where clause")
    return ' where: {' + ''.join(where_clauses) + '} '