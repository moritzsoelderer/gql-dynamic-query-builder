from graphql import GraphQLSyntaxError, parse

query_with_subquery_before_and_after = (
    """
        query Test {
            test_subquery_before {
                test_subquery_body_arg_before
            }
            subquery_to_test {
                subquery_to_test_body_arg
            }
            test_subquery_after {
                test_subquery_body_arg_after
            }
        }
    """,
    """
        subquery_to_test {
            subquery_to_test_body_arg
        }
    """,
)

query_without_filters = (
    """
        query TestQuery {
            subquery_to_test {
                subquery_to_test_body_arg
            }
        }
    """,
    """
        subquery_to_test {
            subquery_to_test_body_arg
        }
    """,
)

query_with_where = (
    """
        query TestQuery {
            subquery_to_test (where: {producer: {_eq: "lego"}}) {
                subquery_to_test_body_arg
            }
        }
    """,
    """
        subquery_to_test (where: {producer: {_eq: "lego"}}) {
            subquery_to_test_body_arg
        }
    """,
)

query_with_limit = (
    """
        query TestQuery {
            subquery_to_test (limit: 10) {
                subquery_to_test_body_arg
            }
        }
    """,
    """
        subquery_to_test (limit: 10) {
            subquery_to_test_body_arg
        }
    """,
)

query_with_where_and_limit = (
    """
        query TestQuery {
            subquery_to_test (where: {producer: {_eq: "lego"}} limit: 10) {
                subquery_to_test_body_arg
            }
        }
    """,
    """
        subquery_to_test (where: {producer: {_eq: "lego"}} limit: 10) {
            subquery_to_test_body_arg
        }
    """,
)

ALL_QUERIES = [
    query_with_where,
    query_with_limit,
    query_without_filters,
    query_with_where_and_limit,
    query_with_subquery_before_and_after,
]


def is_valid_gql(query: str) -> bool:
    try:
        parse(query)
        return True
    except GraphQLSyntaxError as e:
        print(e)
        return False
