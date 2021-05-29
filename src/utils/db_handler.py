#!/usr/bin/env python3
# encoding: utf-8

"""
    Universal DB Handler to connect to postgres using psycopg2.
"""

import logging
import psycopg2


__author__ = "Mohammed Ataaur Rahaman"


class DbHandler:
    def __init__(self, db_name: str, db_user: str, db_pass: str, host: str, port: int):
        self.db_name = db_name
        self.db_pass = db_pass
        self.port = port
        self.host = host
        self.user = db_user
        self.url = host + ":" + str(port)
        self.conn = None
        self.cur = None

    def __str__(self):
        return f"connection to {self.db_name} on {self.url} as {self.user}"

    def __del__(self):
        self.close_connection()

    def create_connection(self):
        if self.conn is None:
            try:
                self.conn = psycopg2.connect(
                    host=self.host,
                    port=self.port,
                    database=self.db_name,
                    user=self.user,
                    password=self.db_pass,
                )
                self.create_cursor()
            except Exception as db_err:
                raise Exception(
                    "Error in making connection to db: {db_err}".format(db_err=db_err)
                )
        else:
            logging.info("Database connection already exists")

    def close_connection(self):
        self.close_cursor()
        if self.conn is not None:
            self.conn.close()
            self.conn = None
            logging.debug("Database connection closed.")

    def create_cursor(self):
        self.cur = self.conn.cursor()

    def close_cursor(self):
        if self.cur is not None:
            self.cur.close()
            self.cur = None

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def query_fetch_results(self, full=True):
        """
        Fetch query results
        :param full: Fetch all rows, if True, else fetch 1 row
        :return: List of rows
        """
        if self.cur is None:
            raise Exception(
                "cursor is not yet initialized, cannot perform fetch operation"
            )
        if full:
            return self.cur.fetchall()
        else:
            return self.cur.fetchone()

    def execute_query(self, query, params=None, error_msg=None):
        try:
            logging.debug("Executing query %s", query)
            self.cur.execute(query, params)
            self.commit()
        except Exception as e:
            self.rollback()
            if error_msg:
                print(error_msg)
                logging.error(error_msg)
            else:
                print(f"Error occurred while executing query: {query} Error=> {e}")
            logging.exception("Error occurred while executing query: %s", query)
            raise e

    def fetchall_query(self, query, params=None, error_msg=None):
        try:
            logging.debug("Executing query %s", query)
            self.cur.execute(query, params)
            self.commit()
            return self.cur.fetchall()
        except Exception as e:
            self.rollback()
            if error_msg:
                print(error_msg)
                logging.error(error_msg)
            else:
                print(f"Error occurred while executing query: {query} Error=> {e}")
            logging.exception("Error occurred while executing query: %s", query)
            raise e

    def execute_and_fetchone_query(self, query, error_msg=None):
        try:
            logging.debug("Executing query %s", query)
            self.cur.execute(query)
            self.commit()
            return self.cur.fetchone()
        except Exception as e:
            self.rollback()
            if error_msg:
                print(error_msg)
                logging.error(error_msg)
            else:
                print(f"Error occurred while executing query: {query} Error=> {e}")
            logging.exception("Error occurred while executing query: %s", query)
            raise e

    def execute_query_with_lambda(self, cb):
        self.create_cursor()
        try:
            result = cb(self.cur)
            self.commit()
            return result
        except Exception as e:
            self.rollback()
            logging.exception(
                "Error occurred while executing queries with lambda function"
            )
            raise e
        finally:
            self.close_cursor()
