## Data
three sample csv files which contain glucose values for users.
The naming pattern for the files is: user_id.csv .

## Task 1
Create a suitable model
in the backend to store the glucose values. Also supply means of
loading the sample data into the model / database.

## Task 2
Implement the following API endpoints which use the model / database:

- /api/v1/levels/ : Retrieve ( GET ) a list of glucose levels for a given
user_id , filter by start and stop timestamps (optional). This endpoint
should support pagination, sorting, and a way to limit the number of
glucose levels returned.

- /api/v1/levels/<id>/ : Retrieve ( GET ) a particular glucose level by id .