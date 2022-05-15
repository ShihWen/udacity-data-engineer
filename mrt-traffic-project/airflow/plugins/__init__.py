from __future__ import division, absolute_import, print_function

from airflow.plugins_manager import AirflowPlugin

import operators
import helpers

# Defining the plugin class
class UdacityPlugin(AirflowPlugin):
    name = "udacity_plugin"
    operators = [
        operators.StageToRedshiftOperator,
        operators.StageToRedshiftOperatorMRT,
        operators.LoadFactOperator,
        operators.LoadFactOperatorMRT,
        operators.LoadDimensionOperator,
        operators.LoadDimensionOperatorMRT,
        operators.DataQualityOperator
    ]
    helpers = [
        helpers.SqlQueries,
        helpers.MrtSqlQueries
    ]
