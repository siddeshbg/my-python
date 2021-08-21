#!/usr/bin/env python3
import os
import snowflake.connector

class SnowflakeBroker():
    def __init__(self, uname, passwd, account, warehouse, db, schema):
        self.uname = uname
        self.passwd = passwd
        self.account = account
        self.warehouse = warehouse
        self.db = db
        self.schema = schema
        self.conn = snowflake.connector.connect(
            user=self.uname,
            password=self.passwd,
            account=self.account,
            warehouse=self.warehouse,
            database=self.db,
            schema=self.schema)
        self.cursor = self.conn.cursor()

    def query_synch(self, query):
        print("Executing snowflake query ...")
        try:
            self.cursor.execute(query)
            results = self.cursor.execute(query).fetchall()
        finally:
            print("closing snowflake connection ...")
            self.cursor.close()

        return results

    def query_asynch(self, table, columns='*'):
        self.cursor.execute_async("select %s from %s" % (columns, table))




def usage():
    s = SnowflakeBroker(
        uname=os.environ['SNOWFLAKE_USER'],
        passwd=os.environ['SNOWFLAKE_PASSWD'],
        account=os.environ['SNOWFLAKE_ACT'],
        warehouse=os.environ['SNOWFLAKE_WH'],
        db=os.environ['SNOWFLAKE_DB'],
        schema=os.environ['SNOWFLAKE_SCHEMA']
    )

    query = """
    SELECT BUILD_URL, DATE, ERRORS, FAILURES, TESTS, TEST_PATH, TEST_SUITE, 
    COMPONENT FROM CDM_UNIT_TESTS 
    WHERE (ERRORS > 0 OR FAILURES > 0) AND DATE >= DATEADD(day,-7, CURRENT_DATE())
    ORDER BY DATE DESC
    """
    results = s.query_synch(query)
    for rec in results:
        print(rec)


if __name__ == '__main__':
    usage()
