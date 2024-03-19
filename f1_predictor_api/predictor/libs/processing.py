import pandas as pd
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Model
from circuits.models import Circuit
from constructors.models import Constructor
from drivers.models import Driver
from results.models import RaceResult

from predictor.libs.utils import convert_queryset_to_dataframe

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
    return queryset


def make_model_df(model:Model, **kwarge) -> pd.DataFrame:
    drivers_qs = make_a_query(model, **kwarge)
    if len(drivers_qs) > 0:
      df = convert_queryset_to_dataframe(drivers_qs)
      return df  # Record found
    else:
      return pd.DataFrame([])

def compose_the_dataframe(driverId, constructorId, circuitId) -> pd.DataFrame:
    circuits = make_a_query(Circuit, circuitId=circuitId)
    constructors = make_a_query(Constructor, constructorId=constructorId)
    drivers = make_a_query(Driver, driverId=driverId)
    race_results = make_a_query(RaceResult, circuitId=circuitId, 
                                constructorId=constructorId,
                                driverId=driverId)
    
    return 0