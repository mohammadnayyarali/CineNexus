# ML concepts

## Content-based recommendation
A content-based system represents each item by its attributes and recommends items whose representations are similar. It does not learn a user's preferences unless user history is supplied.

## TF-IDF
A document is the combined content for one title. Term frequency measures how often a token occurs in that document. Inverse document frequency reduces the importance of tokens appearing in many documents. A common form is:

`tfidf(t, d) = tf(t, d) * log(N / df(t))`

The result is a sparse vector: most vocabulary terms do not occur in most titles.

## Cosine similarity
For vectors A and B:

`cos(A, B) = (A dot B) / (||A|| ||B||)`

It compares direction rather than raw document length, which suits normalized text vectors. TF-IDF rows are compared to the selected title row, producing one score per candidate.

## Ranking and Precision@K
Candidates are sorted by descending similarity and the query item is removed. With real relevance labels, Precision@K is the number of relevant items in the first K positions divided by K. Metadata-only Netflix catalogs do not provide those labels, so this project reports examples and coverage but does not invent a precision result.
