## About this project

This project emerged from the frustrating experience when trying to
write gql queries with dynamic filters. In some cases, think of a UI
to beautifully display database contents, one desires to be able to set filters 
dynamically if some value is provided, yet just ignore it if not.

This behavior was guaranteed by Hasura versions 1.3.3v and below - but disabled by default in later versions,
as described [here](https://hasura.io/docs/2.0/queries/postgres/filters/index/#pg-null-value-evaluation).

The env var `HASURA_GRAPHQL_V1_BOOLEAN_NULL_COLLAPSE` preserves this functionality globally. However,
this as well is not always desired, when a more fine-grained control over when a value is strictly necessary
for where conditions, and when not, is of importance.

This project therefore provides a **lightweight query builder** that takes a simple gql query string
as input and inserts the respective clauses if a value is presented, and does nothing, if not.
This avoids nasty, error-prone, string concatenations while avoiding heavy-weight ASTs and the necessity
of schema declarations as with [gql-DSL](https://gql.readthedocs.io/en/v3.0.0/modules/dsl.html).


