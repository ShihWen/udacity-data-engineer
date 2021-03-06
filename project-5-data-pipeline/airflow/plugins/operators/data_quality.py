from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id='',
                 dq_checks=[],
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id=redshift_conn_id
        self.dq_checks=dq_checks

    def execute(self, context):
        self.log.info('DataQualityOperator not implemented yet')
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        error_count = 0
        failing_tests = []
        self.log.info('Starting to Data Quality checks')
        
        for check in self.dq_checks:
            sql = check.get('check_sql')
            exp_result = check.get('expected_result')

            records = redshift.get_records(sql)[0]

            self.log.info(redshift.get_records(sql))
            
            if exp_result != records[0]:
                error_count += 1
                failing_tests.append(sql)
         
        if error_count > 0:
            self.log.info('Test failed')
            self.log.info(failing_tests)
            raise ValueError('Data Quality check failed')
        
        self.log.info('Data quality checks passed!')
       
        '''
        for table in self.check_tables:
            
            self.log.info(f"executing table {table}")
            """
            records = redshift.get_records(f"SELECT COUNT(*) FROM {table}")
            if len(records) < 1 or len(records[0]) < 1:
                raise ValueError(f"Data quality check failed. {table} returned no results")
            
            self.log.info(f"Row count of {table} table is {records}")
            num_records = records[0][0]
            """
       '''
            