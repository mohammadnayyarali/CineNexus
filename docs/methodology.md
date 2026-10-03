# Methodology

1. Validate that the CSV has a usable `title` column.
2. Normalize text, remove blank titles, and retain the first row for duplicate titles.
3. Combine configured metadata fields into one content document per title.
4. Fit `TfidfVectorizer` offline and store the sparse matrix.
5. At request time, compare the selected row with every catalog row using cosine similarity.
6. Exclude the selected title and return the highest scoring rows.

The baseline gives each combined document one shared TF-IDF vocabulary. This is intentionally simple and auditable. A long description can contribute more terms than a short genre field; field-specific weighting is a possible later experiment and should be evaluated rather than assumed to help.
