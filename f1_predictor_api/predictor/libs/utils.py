import pandas as pd
from sklearn.preprocessing import LabelEncoder

def convert_queryset_to_dataframe(queryset):
  # Get the model class from the queryset
  model_class = queryset.model
  # Get the field names from the model class
  field_names = [field.name for field in model_class._meta.fields]
  # Remove the extra fields that's not requiered for our dataset
  to_remove = ['id', 'createdDate', 'updateDate', 'isArchived', 'picture', 'logo', 'card_id', 'country_img']
  field_names = [x for x in field_names if x not in to_remove]
  # For a specific case (driver model)
  if len(field_names) > 19:
    field_names.remove('constructorId')
  # Extract values from the queryset with the field names
  data = queryset.values(*field_names)

  # Convert the queryset to a pandas DataFrame
  df = pd.DataFrame(list(data))
  return df

def encode_labels(df:pd.DataFrame, cols:list[str]) -> pd.DataFrame:
  le = LabelEncoder()
  for i in cols:
      df[i] = le.fit_transform(df[i])
  return df
