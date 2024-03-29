import math
import pandas as pd
import numpy as np
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Model
from circuits.models import Circuit
from constructors.models import Constructor
from drivers.models import Driver
from results.models import RaceResult

from predictor.libs.utils import convert_queryset_to_dataframe, encode_labels

def make_a_query(model_class:Model, **kwargs):
    queryset = None
    if 'driverId' in kwargs and len(kwargs.keys()) == 1:
      queryset = model_class.objects.filter(driverId=kwargs['driverId'])
    elif 'constructorId' in kwargs and len(kwargs.keys()) == 1:
      queryset = model_class.objects.filter(constructorId=kwargs['constructorId'])
    elif 'circuitId' in kwargs and len(kwargs.keys()) == 1:
      queryset = model_class.objects.filter(circuitId=kwargs['circuitId'])
    elif 'circuitId' in kwargs and 'constructorId' in kwargs and 'driverId' in kwargs:
      queryset = model_class.objects.filter(constructorId=kwargs['constructorId'],
                                         circuitId=kwargs['circuitId'], 
                                         driverId=kwargs['driverId'])
    else:
       queryset = model_class.objects.filter()
    return queryset


def make_model_df(model:Model, **kwarge) -> pd.DataFrame:
    drivers_qs = make_a_query(model, **kwarge)
    if len(drivers_qs) > 0:
      df = convert_queryset_to_dataframe(drivers_qs)
      return df  # Record found
    else:
      return pd.DataFrame([])

def race_result_base_data(prev_races:pd.DataFrame, df_races_results:pd.DataFrame, 
                         driverId:int, constructorId:int, circuitId:int, year:int, 
                         race_round:int, statusId = 1, points = 0) -> list:
  if prev_races.shape[0] > 0:
    grid = prev_races.iloc[0]['grid']
    race_rank = prev_races.iloc[0]['race_rank'] # value to predict
    points = prev_races['points'].mean() # by default is 0
    laps = prev_races['laps'].max()
    milliseconds = int(prev_races['milliseconds'].median())
    fastestLap = int(prev_races['fastestLap'].median())
    fastestLapTime = int(prev_races['fastestLapTime'].median())
    fastestLapSpeed = prev_races['fastestLapSpeed'].mean()
    statusId = statusId
  else:
    grid = math.ceil(df_races_results['grid'].mean())
    race_rank = df_races_results['race_rank'].median()
    points = points
    laps = df_races_results['laps'].median()
    milliseconds = int(df_races_results['milliseconds'].median())
    fastestLap = int(df_races_results['fastestLap'].median())
    fastestLapTime = int(df_races_results['fastestLapTime'].median())
    fastestLapSpeed = df_races_results['fastestLapSpeed'].mean()
    statusId = statusId

  data = [1, 2, driverId, constructorId, grid, race_rank, points, laps, milliseconds, fastestLap, 
          fastestLapTime, fastestLapSpeed, statusId, year, race_round, circuitId, 'Circuit dummy name']
  return data

def compose_the_base_df(driverId, constructorId, circuitId, race_round, year) -> pd.DataFrame:
    colums_names = ['resultId', 'raceId', 'driverId', 'constructorId', 'grid', 'race_rank', 'points', 'laps', 
                   'milliseconds', 'fastestLap', 'fastestLapTime','fastestLapSpeed', 'statusId', 'year', 
                   'round', 'circuitId', 'name']
    circuits_df = make_model_df(Circuit, circuitId=circuitId)
    constructors_df = make_model_df(Constructor, constructorId=constructorId)
    drivers_df = make_model_df(Driver, driverId=driverId)
    prev_results_df = make_model_df(RaceResult, circuitId=circuitId, 
                                constructorId=constructorId,
                                driverId=driverId)
    race_results_df = make_model_df(RaceResult)

    try:
        # We need to chek if all the datasets are empty except the race result dataset
        if circuits_df.shape[0] == 0 or constructors_df.shape[0] == 0 or drivers_df.shape[0] == 0:
          if circuits_df.shape[0] == 0:
            df_empty = 'Circuit'
            df_id = circuitId
          if constructors_df.shape[0] == 0:
            df_empty = 'Constructor'
            df_id = constructorId
          if drivers_df.shape[0] == 0:
            df_empty = 'Driver'
            df_id = driverId
          response = {
            "data": pd.DataFrame([]),
            "statusCode": 7400,
            "message": f"There is no {df_empty} with the id {df_id}"
          }
          return response
        else:
          result_data = race_result_base_data(prev_results_df, race_results_df, driverId, 
                                                 constructorId, circuitId, year, race_round)
          df = pd.DataFrame([result_data], columns=colums_names) 
          response = {
            "data": df,
            "statusCode": 7200,
            "message": f"Dataframe size {df.shape[0]}",
            "extra": {
               "predict_df": df,
               "circuits_df": circuits_df,
               "constructors_df": constructors_df,
               "drivers_df": drivers_df
            }
          }
          return response
    except Exception as e:
      response = {
        "data": pd.DataFrame([]),
        "statusCode" : 7500,
        "message" : e.__str__()
      }
      return response
  
def compose_prediction_df(df_dict:dict) -> pd.DataFrame:
  df_prediction = df_dict['predict_df']
  circuits_df = df_dict['circuits_df']
  constructors_df = df_dict['constructors_df']
  drivers_df = df_dict['drivers_df']

  df_prediction = df_prediction.merge(drivers_df, on='driverId', how='inner')
  df_prediction = df_prediction.merge(constructors_df, on='constructorId', how='inner')
  df_prediction = df_prediction.merge(circuits_df[['circuitId', 'circuits_is_active']], on='circuitId', how='inner')
  
  return df_prediction

def prepare_the_prediction(df:pd.DataFrame, 
                           to_encode_label:list = ['grid', 'race_rank', 'laps', 'fastestLap', 'statusId'],
                           not_correlated_cols:list = ['constructorId', 'raceId', 'resultId', 
                                                'year', 'round', 'circuitId', 'age',
                                                'driver_most_won_circuit_id']) -> pd.DataFrame:
  #  Not corr columns
  df_pred = df.drop(not_correlated_cols, axis=1)
  df_pred['driver_avg_point'] = df_pred['driver_avg_point'].astype('float64')
  df_pred['driver_avg_speed'] = df_pred['driver_avg_speed'].astype('float64')
  df_pred['constructor_avg_point'] = df_pred['constructor_avg_point'].astype('float64')
  cols = df_pred.select_dtypes(np.object_).columns.to_list()
  df_pred = df_pred.drop(cols, axis=1)
  df_pred = encode_labels(df_pred, to_encode_label)
  return df_pred
