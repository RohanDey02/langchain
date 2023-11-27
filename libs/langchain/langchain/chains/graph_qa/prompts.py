# flake8: noqa
from langchain.prompts.prompt import PromptTemplate

_DEFAULT_ENTITY_EXTRACTION_TEMPLATE = """Extract all entities from the following text. As a guideline, a proper noun is generally capitalized. You should definitely extract all names and places.

Return the output as a single comma-separated list, or NONE if there is nothing of note to return.

EXAMPLE
i'm trying to improve Langchain's interfaces, the UX, its integrations with various products the user might want ... a lot of stuff.
Output: Langchain
END OF EXAMPLE

EXAMPLE
i'm trying to improve Langchain's interfaces, the UX, its integrations with various products the user might want ... a lot of stuff. I'm working with Sam.
Output: Langchain, Sam
END OF EXAMPLE

Begin!

{input}
Output:"""
ENTITY_EXTRACTION_PROMPT = PromptTemplate(
    input_variables=["input"], template=_DEFAULT_ENTITY_EXTRACTION_TEMPLATE
)

_DEFAULT_GRAPH_QA_TEMPLATE = """Use the following knowledge triplets to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

{context}

Question: {question}
Helpful Answer:"""
GRAPH_QA_PROMPT = PromptTemplate(
    template=_DEFAULT_GRAPH_QA_TEMPLATE, input_variables=["context", "question"]
)

CYPHER_GENERATION_TEMPLATE = """Task:Generate Cypher statement to query a graph database.
Instructions:
Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.
Schema:
{schema}
Note: Do not include any explanations or apologies in your responses.
Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.
Do not include any text except the generated Cypher statement.

The question is:
{question}"""
CYPHER_GENERATION_PROMPT = PromptTemplate(
    input_variables=["schema", "question"], template=CYPHER_GENERATION_TEMPLATE
)

NEBULAGRAPH_EXTRA_INSTRUCTIONS = """
Instructions:

First, generate cypher then convert it to NebulaGraph Cypher dialect(rather than standard):
1. it requires explicit label specification only when referring to node properties: v.`Foo`.name
2. note explicit label specification is not needed for edge properties, so it's e.name instead of e.`Bar`.name
3. it uses double equals sign for comparison: `==` rather than `=`
For instance:
```diff
< MATCH (p:person)-[e:directed]->(m:movie) WHERE m.name = 'The Godfather II'
< RETURN p.name, e.year, m.name;
---
> MATCH (p:`person`)-[e:directed]->(m:`movie`) WHERE m.`movie`.`name` == 'The Godfather II'
> RETURN p.`person`.`name`, e.year, m.`movie`.`name`;
```\n"""

NGQL_GENERATION_TEMPLATE = CYPHER_GENERATION_TEMPLATE.replace(
    "Generate Cypher", "Generate NebulaGraph Cypher"
).replace("Instructions:", NEBULAGRAPH_EXTRA_INSTRUCTIONS)

NGQL_GENERATION_PROMPT = PromptTemplate(
    input_variables=["schema", "question"], template=NGQL_GENERATION_TEMPLATE
)

KUZU_EXTRA_INSTRUCTIONS = """
Instructions:

Generate statement with Kùzu Cypher dialect (rather than standard):
1. do not use `WHERE EXISTS` clause to check the existence of a property because Kùzu database has a fixed schema.
2. do not omit relationship pattern. Always use `()-[]->()` instead of `()->()`.
3. do not include any notes or comments even if the statement does not produce the expected result.
```\n"""

KUZU_GENERATION_TEMPLATE = CYPHER_GENERATION_TEMPLATE.replace(
    "Generate Cypher", "Generate Kùzu Cypher"
).replace("Instructions:", KUZU_EXTRA_INSTRUCTIONS)

KUZU_GENERATION_PROMPT = PromptTemplate(
    input_variables=["schema", "question"], template=KUZU_GENERATION_TEMPLATE
)

GREMLIN_GENERATION_TEMPLATE = CYPHER_GENERATION_TEMPLATE.replace("Cypher", "Gremlin")

GREMLIN_GENERATION_PROMPT = PromptTemplate(
    input_variables=["schema", "question"], template=GREMLIN_GENERATION_TEMPLATE
)

CYPHER_QA_TEMPLATE = """You are an assistant that helps to form nice and human understandable answers.
The information part contains the provided information that you must use to construct an answer.
The provided information is authoritative, you must never doubt it or try to use your internal knowledge to correct it.
Make the answer sound as a response to the question. Do not mention that you based the result on the given information.
If the provided information is empty, say that you don't know the answer.
Information:
{context}

Question: {question}
Helpful Answer:"""
CYPHER_QA_PROMPT = PromptTemplate(
    input_variables=["context", "question"], template=CYPHER_QA_TEMPLATE
)

SPARQL_INTENT_TEMPLATE = """Task: Identify the intent of a prompt and return the appropriate SPARQL query type.
You are an assistant that distinguishes different types of prompts and returns the corresponding SPARQL query types.
Consider only the following query types:
* SELECT: this query type corresponds to questions
* UPDATE: this query type corresponds to all requests for deleting, inserting, or changing triples
Note: Be as concise as possible.
Do not include any explanations or apologies in your responses.
Do not respond to any questions that ask for anything else than for you to identify a SPARQL query type.
Do not include any unnecessary whitespaces or any text except the query type, i.e., either return 'SELECT' or 'UPDATE'.

The prompt is:
{prompt}
Helpful Answer:"""
SPARQL_INTENT_PROMPT = PromptTemplate(
    input_variables=["prompt"], template=SPARQL_INTENT_TEMPLATE
)

SPARQL_GENERATION_SELECT_TEMPLATE = """Task: Generate a SPARQL SELECT statement for querying a graph database.
For instance, to find all email addresses of John Doe, the following query in backticks would be suitable:
```
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?email
WHERE {{
    ?person foaf:name "John Doe" .
    ?person foaf:mbox ?email .
}}
```
Instructions:
Use only the node types and properties provided in the schema.
Do not use any node types and properties that are not explicitly provided.
Include all necessary prefixes.
Schema:
{schema}
Note: Be as concise as possible.
Do not include any explanations or apologies in your responses.
Do not respond to any questions that ask for anything else than for you to construct a SPARQL query.
Do not include any text except the SPARQL query generated.

The question is:
{prompt}"""
SPARQL_GENERATION_SELECT_PROMPT = PromptTemplate(
    input_variables=["schema", "prompt"], template=SPARQL_GENERATION_SELECT_TEMPLATE
)

SPARQL_GENERATION_UPDATE_TEMPLATE = """Task: Generate a SPARQL UPDATE statement for updating a graph database.
For instance, to add 'jane.doe@foo.bar' as a new email address for Jane Doe, the following query in backticks would be suitable:
```
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
INSERT {{
    ?person foaf:mbox <mailto:jane.doe@foo.bar> .
}}
WHERE {{
    ?person foaf:name "Jane Doe" .
}}
```
Instructions:
Make the query as short as possible and avoid adding unnecessary triples.
Use only the node types and properties provided in the schema.
Do not use any node types and properties that are not explicitly provided.
Include all necessary prefixes.
Schema:
{schema}
Note: Be as concise as possible.
Do not include any explanations or apologies in your responses.
Do not respond to any questions that ask for anything else than for you to construct a SPARQL query.
Return only the generated SPARQL query, nothing else.

The information to be inserted is:
{prompt}"""
SPARQL_GENERATION_UPDATE_PROMPT = PromptTemplate(
    input_variables=["schema", "prompt"], template=SPARQL_GENERATION_UPDATE_TEMPLATE
)

SPARQL_QA_TEMPLATE = """Task: Generate a natural language response from the results of a SPARQL query.
You are an assistant that creates well-written and human understandable answers.
The information part contains the information provided, which you can use to construct an answer.
The information provided is authoritative, you must never doubt it or try to use your internal knowledge to correct it.
Make your response sound like the information is coming from an AI assistant, but don't add any information.
Information:
{context}

Question: {prompt}
Helpful Answer:"""
SPARQL_QA_PROMPT = PromptTemplate(
    input_variables=["context", "prompt"], template=SPARQL_QA_TEMPLATE
)

DQL_GENERATION_TEMPLATE= """Task: Generate an DGraph Query Language (DQL) query from a User Input.
You are an DGraph Query Language (DQL) expert responsible for translating a `User Input` into an DGraph Query Language (DQL) query.

You are given an `DGraph Schema`. It is a JSON Object containing an dictionary/json with schema type name as key,
and it's properties as values.

You may also be given a set of `DQL Query Examples` to help you create the `DQL Query`. If provided, the `DQL Query Examples` should be used as a reference, similar to how `DGraph Schema` should be used.

Things you should do:
- IMPORTANT: Remember to use "~" before a field which is a reverse edge. For example if in the Movie Schema, you see that the "cast" predicate is set to true.
If you want to reference cast from an Actor, you MUST use "~cast" to reference it.
- Think step by step.
- Rely on `DGraph Schema` and `DQL Query Examples` (if provided) to generate the query.
- IMPORTANT: Return the `DQL Query` wrapped in 3 backticks (```).
- Use only the provided relationship types and properties in the `DGraph Schema` and any `DQL Query Examples` queries.
- Only answer to requests related to generating an DQL Query.
- If a request is unrelated to generating DQL Query, say that you cannot help the user.

Things you should not do:

- You should NEVER prefix a field with its type. For example DO NOT USE Movie.year, or Movie.cast, INSTEAD use year or cast.
  For example, NEVER do:
    var(func: eq(name, "Forrest Gump")) 
      Movie.cast 
        Actor.name
        
- Do not use any properties/relationships that can't be inferred from the `DGraph Schema` or the `DQL Query Examples`.
- Do not include any text except the generated DQL Query.
- Do not provide explanations or apologies in your responses.
- Do not generate a DQL Query that removes or deletes any data.
- IMPORTANT: Don't use the var keyword unless you absolutely have to.
- IMPORTANT: Don't use the same variable name for two sections of the query.

  uses actor_name as name twice. This is not allowed.
- Under no circumstance should you generate an DQL Query that deletes any data whatsoever.

Raw notes on DQL query syntax is here:
{dql_syntax_notes}

DGraph Schema:
{dgraph_schema}

DQL Query Examples (Optional):
{dql_examples}

User Input:
{user_input}

DQL Query: 
"""

DQL_GENERATION_PROMPT = PromptTemplate(
    input_variables=["dgraph_schema", "dql_examples", "user_input", "dql_syntax_notes"],
    template=DQL_GENERATION_TEMPLATE,
)


DQL_FIX_TEMPLATE = """Task: Address the DGraph Query Language (DQL) error message of an DGraph Query Language query.

You are an DGraph Query Language (DQL) expert responsible for correcting the provided `DQL Query` based on the provided `DQL Error`. 

The `DQL Error` explains why the `DQL Query` could not be executed in the database.
The `DQL Error` may also contain the position of the error relative to the total number of lines of the `DQL Query`.
For example, 'error X at position 2:5' denotes that the error X occurs on line 2, column 5 of the `DQL Query`.  

You are given an `DGraph Schema`. It is a JSON Object containing an dictionary/json with schema type name as key,
and it's properties as values.
You will output the `Corrected DQL Query`. Do not include any text except the Corrected DQL Query.

Remember to think step by step.

DGraph Schema:
{dgraph_schema}

DQL Query:
{dql_query}

DQL Error:
{dql_error}

DQL Query Examples:
{dql_examples}

Corrected DQL Query:
"""

DGRAPH_FIX_PROMPT = PromptTemplate(
    input_variables=[
        "dgraph_schema",
        "dql_query",
        "dql_error",
        "dql_examples"
    ],
    template=DQL_FIX_TEMPLATE,
)


DQL_QA_TEMPLATE = """Task: Generate a natural language `Summary` from the results of an DGraph Query Language query.

You are an DGraph Query Language (DQL) expert responsible for creating a well-written `Summary` from the `User Input` and associated `DQL Result`.

A user has executed an DGraph Query Language query, which has returned the DQL Result in JSON format.
You are responsible for creating an `Summary` based on the DQL Result.

You are given the following information:
- `DGraph Schema`: Is a dictionary/json with schema type name as key, and it's properties as values.
- `User Input`: the original question/request of the user, which has been translated into an DQL Query.
- `DQL Query`: the DQL equivalent of the `User Input`, translated by another AI Model. Should you deem it to be incorrect, suggest a different DQL Query.
- `DQL Result`: the JSON output returned by executing the `DQL Query` within the DGraph Database.

Remember to think step by step.

Your `Summary` should sound like it is a response to the `User Input`.
Your `Summary` should not include any mention of the `DQL Query` or the `DQL Result`.

DGraph Schema:
{dgraph_schema}

User Input:
{user_input}

DQL Query:
{dql_query}

DQL Result:
{dql_result}
"""

DGRAPH_QA_PROMPT = PromptTemplate(
    input_variables=["dgraph_schema", "user_input", "dql_query", "dql_result"],
    template=DQL_QA_TEMPLATE,
)

AQL_GENERATION_TEMPLATE = """Task: Generate an ArangoDB Query Language (AQL) query from a User Input.

You are an ArangoDB Query Language (AQL) expert responsible for translating a `User Input` into an ArangoDB Query Language (AQL) query.

You are given an `ArangoDB Schema`. It is a JSON Object containing:
1. `Graph Schema`: Lists all Graphs within the ArangoDB Database Instance, along with their Edge Relationships.
2. `Collection Schema`: Lists all Collections within the ArangoDB Database Instance, along with their document/edge properties and a document/edge example.

You may also be given a set of `AQL Query Examples` to help you create the `AQL Query`. If provided, the `AQL Query Examples` should be used as a reference, similar to how `ArangoDB Schema` should be used.

Things you should do:
- Think step by step.
- Rely on `ArangoDB Schema` and `AQL Query Examples` (if provided) to generate the query.
- Begin the `AQL Query` by the `WITH` AQL keyword to specify all of the ArangoDB Collections required.
- Return the `AQL Query` wrapped in 3 backticks (```).
- Use only the provided relationship types and properties in the `ArangoDB Schema` and any `AQL Query Examples` queries.
- Only answer to requests related to generating an AQL Query.
- If a request is unrelated to generating AQL Query, say that you cannot help the user.

Things you should not do:
- Do not use any properties/relationships that can't be inferred from the `ArangoDB Schema` or the `AQL Query Examples`. 
- Do not include any text except the generated AQL Query.
- Do not provide explanations or apologies in your responses.
- Do not generate an AQL Query that removes or deletes any data.

Under no circumstance should you generate an AQL Query that deletes any data whatsoever.

ArangoDB Schema:
{adb_schema}

AQL Query Examples (Optional):
{aql_examples}

User Input:
{user_input}

AQL Query: 
"""

AQL_GENERATION_PROMPT = PromptTemplate(
    input_variables=["adb_schema", "aql_examples", "user_input"],
    template=AQL_GENERATION_TEMPLATE,
)

AQL_FIX_TEMPLATE = """Task: Address the ArangoDB Query Language (AQL) error message of an ArangoDB Query Language query.

You are an ArangoDB Query Language (AQL) expert responsible for correcting the provided `AQL Query` based on the provided `AQL Error`. 

The `AQL Error` explains why the `AQL Query` could not be executed in the database.
The `AQL Error` may also contain the position of the error relative to the total number of lines of the `AQL Query`.
For example, 'error X at position 2:5' denotes that the error X occurs on line 2, column 5 of the `AQL Query`.  

You are also given the `ArangoDB Schema`. It is a JSON Object containing:
1. `Graph Schema`: Lists all Graphs within the ArangoDB Database Instance, along with their Edge Relationships.
2. `Collection Schema`: Lists all Collections within the ArangoDB Database Instance, along with their document/edge properties and a document/edge example.

You will output the `Corrected AQL Query` wrapped in 3 backticks (```). Do not include any text except the Corrected AQL Query.

Remember to think step by step.

ArangoDB Schema:
{adb_schema}

AQL Query:
{aql_query}

AQL Error:
{aql_error}

Corrected AQL Query:
"""

AQL_FIX_PROMPT = PromptTemplate(
    input_variables=[
        "adb_schema",
        "aql_query",
        "aql_error",
    ],
    template=AQL_FIX_TEMPLATE,
)

AQL_QA_TEMPLATE = """Task: Generate a natural language `Summary` from the results of an ArangoDB Query Language query.

You are an ArangoDB Query Language (AQL) expert responsible for creating a well-written `Summary` from the `User Input` and associated `AQL Result`.

A user has executed an ArangoDB Query Language query, which has returned the AQL Result in JSON format.
You are responsible for creating an `Summary` based on the AQL Result.

You are given the following information:
- `ArangoDB Schema`: contains a schema representation of the user's ArangoDB Database.
- `User Input`: the original question/request of the user, which has been translated into an AQL Query.
- `AQL Query`: the AQL equivalent of the `User Input`, translated by another AI Model. Should you deem it to be incorrect, suggest a different AQL Query.
- `AQL Result`: the JSON output returned by executing the `AQL Query` within the ArangoDB Database.

Remember to think step by step.

Your `Summary` should sound like it is a response to the `User Input`.
Your `Summary` should not include any mention of the `AQL Query` or the `AQL Result`.

ArangoDB Schema:
{adb_schema}

User Input:
{user_input}

AQL Query:
{aql_query}

AQL Result:
{aql_result}
"""
AQL_QA_PROMPT = PromptTemplate(
    input_variables=["adb_schema", "user_input", "aql_query", "aql_result"],
    template=AQL_QA_TEMPLATE,
)


NEPTUNE_OPENCYPHER_EXTRA_INSTRUCTIONS = """
Instructions:
Generate the query in openCypher format and follow these rules:
Do not use `NONE`, `ALL` or `ANY` predicate functions, rather use list comprehensions.
Do not use `REDUCE` function. Rather use a combination of list comprehension and the `UNWIND` clause to achieve similar results.
Do not use `FOREACH` clause. Rather use a combination of `WITH` and `UNWIND` clauses to achieve similar results.
\n"""

NEPTUNE_OPENCYPHER_GENERATION_TEMPLATE = CYPHER_GENERATION_TEMPLATE.replace(
    "Instructions:", NEPTUNE_OPENCYPHER_EXTRA_INSTRUCTIONS
)

NEPTUNE_OPENCYPHER_GENERATION_PROMPT = PromptTemplate(
    input_variables=["schema", "question"],
    template=NEPTUNE_OPENCYPHER_GENERATION_TEMPLATE,
)

NEPTUNE_OPENCYPHER_GENERATION_SIMPLE_TEMPLATE = """
Write an openCypher query to answer the following question. Do not explain the answer. Only return the query. 
Question:  "{question}". 
Here is the property graph schema: 
{schema}
\n"""

NEPTUNE_OPENCYPHER_GENERATION_SIMPLE_PROMPT = PromptTemplate(
    input_variables=["schema", "question"],
    template=NEPTUNE_OPENCYPHER_GENERATION_SIMPLE_TEMPLATE,
)


DQL_QUERY_EXAMPLE = """
  {
  "Actor":[
        {
          "predicate":"age",
          "type":"int"
        },
        {
          "predicate":"name",
          "type":"string",
          "index":true,
          "tokenizer":[
              "term"
          ]
        }
    ],
    "Movie":[
      {
          "predicate":"cast",
          "type":"uid",
          "reverse":true,
          "list":true
      },
      {
          "predicate":"name",
          "type":"string",
          "index":true,
          "tokenizer":[
            "term"
          ]
      },
      {
          "predicate":"year",
          "type":"string",
          "index":true,
          "tokenizer":[
            "exact"
          ]
      }
    ]
  }
  
Here are some DQL Examples that you can use as a reference:
Here are some DQL Query examples:

Question: Find all the actors, and give me their names and ages.
DQL Query: 
{
  find_type(func: type(Actor)){
		uid
    name
  }
}

Question: Find all the movies, and their casts as well
DQL Query: 
{
  find_type(func: type(Movie)){
    uid
    name
    cast{
      uid
      name
    }
  }
}

Question: Find all movies that were released after 2016
DQL Query: 
{
  find_movies(func: type(Movie)) @filter(gt(year, "2016")){
    expand(_all_)
  }
}

Question: Find all the movies that Tom Hanks acted in
DQL Query:
{
 movies(func: eq(name, "Tom Hanks")){
    ~cast{
    	name
		}
  }
}


Question: Find all the actors that acted in Spiderman, and/or Superman
{
  var(func: eq(name, "Spiderman")){
    Spiderman as cast{
      uid
      name
    }
  }
  
  var(func: eq(name, "Superman")){
		Superman as cast{
			uid
      name
    }
  }
  
  actors(func: uid(movie_special, movie_baby)){
  	uid
    name
  }
}

Question: Find all the actors that acted in Spiderman
{
  var(func: eq(name, "Spiderman")){
    Spiderman as cast{
      uid
      name
    }
  }
  
  actors(func: uid(Spiderman)){
  	uid
    name
  }
}

OR

{
  spiderman_actors(func: eq(name, "Spiderman")){
    cast{
      uid
      name
    }
  }
}

"""


DQL_QUERYSYNTAX_INJECT_STRING = """
DQL query
Fetching data with Dgraph Query Language (DQL), is done through DQL Queries. Adding, modifying or deleting data is done through DQL Mutations.

This overview explains the structure of DQL Queries and provides links to the appropriate DQL reference documentation.

DQL query structure
DQL is declarative, which means that queries return a response back in a similar shape to the query. It gives the client application the control of what it gets: the request return exactly what you ask for, nothing less and nothing more. In this, DQL is similar to GraphQL from which it is inspired.

A DQL query finds nodes based on search criteria, matches patterns in the graph and returns the node attributes, relationships specified in the query.

A DQL query has

an optional parameterization, ie a name and a list of parameters
an opening curly bracket
at least one query block, but can contain many blocks
optional var blocks
a closing curly bracket
DQL Query with parameterization
Query parameterization
Parameters

must have a name starting with a $ symbol.
must have a type int, float, bool or string.
may have a default value. In the example below, $age has a default value of 95
may be mandatory by suffixing the type with a !. Mandatory parameters can’t have a default value.
Variables can be used in the query where a string, float, int or bool value are needed.

You can also use a variable holding uids by using a string variable and by providing the value as a quoted list in square brackets:
query title($uidsParam: string = "[0x1, 0x2, 0x3]") { ... }.

Error handling When submitting a query using parameters, Dgraph responds with errors if

A parameter value is not parsable to the given type.
The query is using a parameter that is not declared.
A mandatory parameter is not provided
The query parameterization is optional. If you don’t use parameters you can omit it and send only the query blocks.

DQL Query without parameters
Note The current documentation is usually using example of queries without parameters.
If you execute this query in our Movies demo database you can see that Dgraph will return a JSON structure similar to the request :

DQL response structure
Query block
A query block specifies information to retrieve from Dgraph.

A query block

must have name
must have a node criteria defined by the keyword func:
may have ordering and pagination information
may have a combination of filters (to apply to the root nodes)
must provide the list of attributes and relationships to fetch for each node matching the root nodes.
Refer to pagination, ordering, connecting filters for more information.

For each relationships to fetch, the query is using a nested block.

A nested block

may specify filters to apply on the related nodes
may specify criteria on the relationships attributes using filtering on facets)
provides the list of relationship attributes (facets)) to fetch.
provides the list of attributes and relationships to fetch for the related nodes.
A nested block may contain another nested block, and such at any level.

Escape characters in predicate names
If your predicate has special characters, wrap it with angular brackets < > in the query.

Formatting options
Dgraph returns the attributes and relationships that you specified in the query. You can specify an alternate name for the result by using aliases.

You can flatten the response structure at any level using @normalize directive.

Entering the list of all the attributes you want to fetch could be fastidious for large queries or repeating blocks : you may take advantage of fragments and the expand function.

Node criteria (used by root function or by filter)
Root criteria and filters are using functions applied to nodes attributes or variables.

Dgraph offers functions for

testing string attributes
term matching : allofterms, anyofterms
regular Expression : regexp
fuzzy match : match
full-text search : alloftext
testing attribute value
equality : eq
inequalities : le,lt,ge,gt
range : between
testing if a node
has a particular predicate (an attribute or a relation) : has
has a given UID : uid
has a relationship to a given node : uid_in
is of a given type : type()
testing the number of node relationships
equality : eq
inequalities : le,lt,ge,gt
testing geolocation attributes
if geo location is within distance : near
if geo location lies within a given area : within
if geo area contains a given location : contains
if geo area intersects a given are : intersects
Variable (var) block
Variable blocks (var blocks) start with the keyword var instead of a block name.

var blocks are not reflected in the query result. They are used to compute query-variables which are lists of node UIDs, or value-variables which are maps from node UIDs to the corresponding scalar values.

Note that query-variables and value-variables can also be computed in query blocks. In that case, the query block is used to fetch and return data, and to define some variables which must be used in other blocks of the same query.

Variables may be used as functions parameters in filters or root criteria in other blocks.

Summarizing functions
When dealing with array attributes or with relationships to many node, the query may use summary functions count , min, max, avg or sum.

The query may also contain mathematical functions on value variables.

Summary functions can be used in conjunction with @grouby directive to create aggregated value variables.

The query may contain anonymous block to return computed values. Anonymous block don’t have a root criteria as they are not used to search for nodes but only to returned computed values.

Graph traversal
When you specify nested blocks and filters you basically describe a way to traverse the graph.

@recurse and @ignorereflex are directives used to optionally configure the graph traversal.

Pattern matching
Queries with nested blocks with filters may be turned into pattern matching using @cascade directive : nodes that don’t have all attributes and all relationships specified in the query at any sub level are not considered in the result. So only nodes “matching” the complete query structure are returned.

Graph algorithms
The query can ask for the shortest path between a source (from) node and destination (to) node using the shortest query block.

Comments
Anything on a line following a # is a comment
"""