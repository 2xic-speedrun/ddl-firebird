# DDL for Firebird

Simple parser to parse (parts of the) Firebird DDL format from DBeaver.

Will be used to benchmark aspects of Firebird DB by importing only tables dependent on each other.

## TODO (??)
- [ ] Complete the necessary parts of the parser
  - [ ] Will use reference counting for procedures
- [ ] Make the parser output the full objects (i.e that they can be used to reconstruct the tables)
- [ ] Put the tables in a graph, and make it possible to get the DDL for connected nodes.
