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
        try:
            self.cursor.execute(query)
            for col1, col2 in self.cursor:
                print("%s, %s" % (col1, col2))
        finally:
            self.cursor.close()


    def query_asynch(self, table, columns='*'):
        self.cursor.execute_async("select %s from %s" % (columns, table))




def usage():
    print("hello")
    s = SnowflakeBroker(
        uname=os.environ['SNOWFLAKE_USER'],
        passwd=os.environ['SNOWFLAKE_PASSWD'],
        account=os.environ['SNOWFLAKE_ACT'],
        warehouse=os.environ['SNOWFLAKE_WH'],
        db=os.environ['SNOWFLAKE_DB'],
        schema=os.environ['SNOWFLAKE_SCHEMA']
    )

    s.query_synch("SELECT BUILD_URL, DATE FROM CDM_UNIT_TESTS LIMIT 10")


if __name__ == '__main__':
    usage()
