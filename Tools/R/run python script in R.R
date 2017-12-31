# run python scripts and catch output & functions in R
library(reticulate)
python_fns = import_from_path('spliteCSV',path = './')
python_fns$get_chunk_csv()
