from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults



class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'
    template_fields = ("s3_key",)
    exe_sql = """
        COPY {staging_table}
        FROM '{data_path}'
        ACCESS_KEY_ID '{access_key}'
        SECRET_ACCESS_KEY '{secret_key}'
        REGION '{region}'
        JSON '{json_option}'
    """

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 aws_credentials_id="",
                 table="",
                 s3_bucket="",
                 s3_key="",
                 json_option="",
                 region="",
                 *args, **kwargs):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.aws_credentials_id = aws_credentials_id
        self.table = table
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.json_option = json_option
        self.region = region

    def execute(self, context):
        self.log.info(f'Starting to copy staging table: {self.table}')
        aws_hook = AwsHook(self.aws_credentials_id)
        credentials = aws_hook.get_credentials()
        redshift = PostgresHook(postgres_conn_id = self.redshift_conn_id)

        
        rendered_key = self.s3_key.format(**context)
        s3_path = "{}/{}".format(self.s3_bucket, rendered_key)
        
        formatted_sql = StageToRedshiftOperator.exe_sql.format(
            staging_table=self.table,
            data_path=s3_path,
            access_key=credentials.access_key,
            secret_key=credentials.secret_key,
            region=self.region,
            json_option=self.json_option
        )
        
        redshift.run(formatted_sql)
        
        self.log.info(f'Finish copying staging table: {self.table}')





