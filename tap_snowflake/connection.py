#!/usr/bin/env python3

import backoff
import singer
import sys
import snowflake.connector

LOGGER = singer.get_logger('tap_snowflake')


class TooManyRecordsException(Exception):
    """Exception to raise when query returns more records than max_records"""


def retry_pattern():
    """Retry pattern decorator used when connecting to snowflake
    """
    return backoff.on_exception(backoff.expo,
                                snowflake.connector.errors.OperationalError,
                                max_tries=5,
                                on_backoff=log_backoff_attempt,
                                factor=2)


def log_backoff_attempt(details):
    """Log backoff attempts used by retry_pattern
    """
    LOGGER.info('Error detected communicating with Snowflake, triggering backoff: %d try', details.get('tries'))


def validate_config(config):
    """Validate configuration dictionary"""
    errors = []
    required_config_keys = [
        'account',
        'dbname',
        'user',
        'password',
        'warehouse'
    ]

    # Check if mandatory keys exist
    for k in required_config_keys:
        if not config.get(k, None):
            errors.append(f'Required key is missing from config: [{k}]')

    return errors


class SnowflakeConnection:
    """Class to manage connection to snowflake data warehouse"""

    def __init__(self, connection_config):
        """
        connection_config:      Snowflake connection details
        """
        self.connection_config = connection_config
        config_errors = validate_config(connection_config)
        if len(config_errors) == 0:
            self.connection_config = connection_config
        else:
            LOGGER.error('Invalid configuration:\n   * %s', '\n   * '.join(config_errors))
            sys.exit(1)


    def open_connection(self):
        """Connect to snowflake database"""
        return snowflake.connector.connect(
            user=self.connection_config['user'],
            password=self.connection_config['password'],
            account=self.connection_config['account'],
            database=self.connection_config['dbname'],
            warehouse=self.connection_config['warehouse'],
            insecure_mode=self.connection_config.get('insecure_mode', False)
            # Use insecure mode to avoid "Failed to get OCSP response" warnings
            #insecure_mode=True
        )


    @retry_pattern()
    def connect_with_backoff(self):
        """Connect to snowflake database and retry automatically a few times if fails"""
        return self.open_connection()


    def query(self, query, params=None, max_records=0):
        """Run a query in snowflake"""
        result = []
        with self.connect_with_backoff() as connection:
            with connection.cursor(snowflake.connector.DictCursor) as cur:
                queries = []

                # Run every query in one transaction if query is a list of SQL
                if isinstance(query, list):
                    queries.append('START TRANSACTION')
                    queries.extend(query)
                else:
                    queries = [query]

                for sql in queries:
                    LOGGER.debug('SNOWFLAKE - Running query: %s', sql)
                    cur.execute(sql, params)

                    # Raise exception if returned rows greater than max allowed records
                    if 0 < max_records < cur.rowcount:
                        raise TooManyRecordsException(
                            f'Query returned too many records. This query can return max {max_records} records')

                    if cur.rowcount > 0:
                        result = cur.fetchall()

        return result
