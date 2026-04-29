# Neo4j connection config

import os
from contextlib import contextmanager
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

_driver = None

def get_driver():
    global _driver
    if _driver is None:
        uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        user = os.getenv("NEO4J_USER", "neo4j")
        password = os.getenv("NEO4J_PASSWORD", "")
        _driver = GraphDatabase.driver(uri, auth=(user, password))
    return _driver

@contextmanager
def get_session():
    driver = get_driver()
    database = os.getenv("NEO4J_DATABASE", "neo4j")
    session = driver.session(database=database)
    try:
        yield session
    finally:
        session.close()

def close_driver():
    global _driver
    if _driver is not None:
        _driver.close()
        _driver = None

def execute_query(query, params=None):
    with get_session() as session:
        result = session.run(query, params or {})
        return [dict(record) for record in result]

def execute_write(query, params=None):
    with get_session() as session:
        session.execute_write(lambda tx: tx.run(query, params or {}))

def check_connection():
    try:
        driver = get_driver()
        driver.verify_connectivity()
        return True
    except:
        return False
