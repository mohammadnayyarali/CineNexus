# Dataset setup

This repository includes a small **synthetic demonstration dataset** at `data/raw/netflix_titles.csv` so the application can run immediately. The titles, people, countries, and descriptions are fictional and must not be presented as official Netflix data.

For production or portfolio evaluation, replace it with a licensed Netflix titles CSV or set `DATASET_PATH`.

The only required column is `title`. Optional columns are `type`, `director`, `cast`, `country`, `rating`, `listed_in`, `description`, `release_year`, `show_id`, `date_added`, and `duration`. The project does not include or fabricate a dataset.

A common public source is the Netflix Movies and TV Shows dataset on Kaggle. Check its license and terms before using it. The system uses metadata only; it does not contain user ratings, watch history, or personal profiles.
