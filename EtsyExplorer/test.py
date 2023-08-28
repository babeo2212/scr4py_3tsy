
import itertools
import pandas as pd

def iterate_dataframe_lazy(df):
  """Iterates through a DataFrame using lazy evaluation.

  Args:
    df: The DataFrame to iterate through.

  Yields:
    Each row of the DataFrame.
  """
  # Create a shallow copy of the DataFrame.
  df_copy = df.copy()

  # Create two iterators over the DataFrame.
  it1, it2 = itertools.tee(df_copy.iterrows())

  # Iterate over the first iterator.
  for _, row in it1:
    yield row


df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
rows = iterate_dataframe_lazy(df)
# for row in iterate_dataframe_lazy(df):
#   print(row)
print(next(rows))
print(next(rows))
print(next(rows))