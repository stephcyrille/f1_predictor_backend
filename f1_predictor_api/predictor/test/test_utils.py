from django.test import TestCase
from drivers.models import Driver
from constructors.models import Constructor
from circuits.models import Circuit
from results.models import RaceResult
from predictor.libs.processing import make_a_query, make_model_df, compose_the_base_df, compose_prediction_df, prepare_the_prediction

class RaceComponentsTestCase(TestCase):
  fixtures = ['test_dump.json', ]

  def setUp(self) -> None:
    self.driverId = 1
    self.constructorId = 131
    self.circuitId = 3
    self.race_round = 1
    self.year = 2023

  def test_driver_query(self):
    """Test a generic query from from the Driver"""
    qs = make_a_query(Driver, driverId=self.driverId)
    self.assertEqual(len(qs), 1)

  def test_constructor_query(self):
    """Test a generic query from from the Constructor"""
    qs = make_a_query(Constructor, constructorId=self.constructorId)
    self.assertEqual(len(qs), 1)

  def test_circuit_query(self):
    """Test a generic query from from the Circuit"""
    qs = make_a_query(Circuit, circuitId=self.circuitId)
    self.assertEqual(len(qs), 1, "There is an error with the request parameter")

  def test_race_result_query(self):
    """Test a generic query from from the Race Result"""
    qs = make_a_query(RaceResult, circuitId=self.circuitId, 
                      constructorId=self.constructorId, driverId=self.driverId)
    self.assertGreater(len(qs), 1, 'There is no race result found for these parameters')

  def test_make_circuit_dataframe_from_model(self):
    circuits_df = make_model_df(Circuit, circuitId=self.circuitId)
    self.assertEqual(circuits_df.shape[0], 1, 
                     "The size of the df must just be 1 because we have an unique circuit id")

  def test_make_constructor_dataframe_from_model(self):
    constructor_df = make_model_df(Constructor, constructorId=self.constructorId)
    self.assertEqual(constructor_df.shape[0], 1, 
                     "The size of the df must just be 1 because we have an unique constructor id")

  def test_make_driver_dataframe_from_model(self):
    driver_df = make_model_df(Driver, driverId=self.driverId)
    self.assertEqual(driver_df.shape[0], 1, 
                     "The size of the df must just be 1 because we have an unique driver id")

  def test_make_previous_race_dataframe_from_model(self):
    prev_race_df = make_model_df(RaceResult, circuitId=self.circuitId, 
                                 constructorId=self.constructorId, 
                                 driverId=self.driverId)
    self.assertGreater(prev_race_df.shape[0], 1, 
                       "The size of the df must be greater than 1 because we need the previous races to continue")

  def test_make_all_race_results_dataframe_from_model(self):
    race_results_df = make_model_df(RaceResult)
    self.assertGreater(race_results_df.shape[0], 1, "The size of the df must be greater than 1")

  def test_compose_the_base_df(self):
    response_data = compose_the_base_df(self.driverId, self.constructorId, self.circuitId, self.race_round, self.year)
    self.assertEqual(response_data["statusCode"], 7200, f"{response_data['message']}")

  def test_compose_df_prediction(self):
    response_data = compose_the_base_df(self.driverId, self.constructorId, self.circuitId, self.race_round, self.year)
    prediction_df = compose_prediction_df(response_data['extra'])
    self.assertEqual(len(prediction_df.columns), 44, "The merged dataset contain a bad number of columns")

  def test_the_prediction_dataset_prepared(self):
    response_data = compose_the_base_df(self.driverId, self.constructorId, self.circuitId, self.race_round, self.year)
    prediction_df = compose_prediction_df(response_data['extra'])
    df = prepare_the_prediction(prediction_df)
    self.assertEqual((0, len(df.columns)), (0, 30), "The dataset lenght for this prediction must be (0, 30)")