#!/usr/bin/env python3
# pylint: disable=duplicate-code,too-many-locals,simplifiable-if-expression

import singer
import tap_snowflake.sync_strategies.common as common

LOGGER = singer.get_logger('tap_snowflake')

def sync_table(snowflake_conn, catalog_entry, state, columns, stream_version):
    """Sync table with N_ROWS"""
    # common.whitelist_bookmark_keys(BOOKMARK_KEYS, catalog_entry.tap_stream_id, state)

    with snowflake_conn.connect_with_backoff() as open_conn:
        with open_conn.cursor() as cur:
            select_sql = common.generate_select_sql(catalog_entry, columns) + ' LIMIT 10'
            params = {}

            common.sync_query(cur,
                              catalog_entry,
                              state,
                              select_sql,
                              columns,
                              stream_version,
                              params)

    # clear max pk value and last pk fetched upon successful sync
    singer.clear_bookmark(state, catalog_entry.tap_stream_id, 'max_pk_values')
    singer.clear_bookmark(state, catalog_entry.tap_stream_id, 'last_pk_fetched')