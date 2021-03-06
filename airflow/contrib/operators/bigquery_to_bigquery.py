import logging

from airflow.contrib.hooks.bigquery_hook import BigQueryHook
from airflow.models import BaseOperator
from airflow.utils import apply_defaults

class BigQueryToBigQueryOperator(BaseOperator):
    """
    Copy a BigQuery table to another BigQuery table.
    """
    template_fields = ('source_dataset_tables','destination_project_dataset_table',)
    template_ext = ('.sql',)
    ui_color = '#e6f0e4'

    @apply_defaults
    def __init__(
        self, 
        source_dataset_tables,
        destination_project_dataset_table,
        write_disposition='WRITE_EMPTY',
        create_disposition='CREATE_IF_NEEDED',
        bigquery_conn_id='bigquery_default',
        delegate_to=None,
        *args, 
        **kwargs):
        """
        Copies data from one BigQuery table to another. See here:

        https://cloud.google.com/bigquery/docs/reference/v2/jobs#configuration.copy

        For more details about these parameters.

        :param source_dataset_tables: One or more dotted <dataset>.<table>
            BigQuery tables to use as the source data. Use a list if there are
            multiple source tables.
        :type source_dataset_tables: list|string
        :param destination_project_dataset_table: The destination BigQuery
            table. Format is: <project>.<dataset>.<table>
        :type destination_project_dataset_table: string
        :param write_disposition: The write disposition if the table already exists.
        :type write_disposition: string
        :param create_disposition: The create disposition if the table doesn't exist.
        :type create_disposition: string
        :param bigquery_conn_id: reference to a specific BigQuery hook.
        :type bigquery_conn_id: string
        :param delegate_to: The account to impersonate, if any.
            For this to work, the service account making the request must have domain-wide delegation enabled.
        :type delegate_to: string
        """
        super(BigQueryToBigQueryOperator, self).__init__(*args, **kwargs)
        self.source_dataset_tables = source_dataset_tables
        self.destination_project_dataset_table = destination_project_dataset_table
        self.write_disposition = write_disposition
        self.create_disposition = create_disposition
        self.bigquery_conn_id = bigquery_conn_id
        self.delegate_to = delegate_to

    def execute(self, context):
        logging.info('Executing copy of %s into: %s', self.source_dataset_tables, self.destination_project_dataset_table)
        hook = BigQueryHook(bigquery_conn_id=self.bigquery_conn_id, delegate_to=self.delegate_to)
        conn = hook.get_conn()
        cursor = conn.cursor()
        cursor.run_copy(
            self.source_dataset_tables,
            self.destination_project_dataset_table,
            self.write_disposition,
            self.create_disposition)
