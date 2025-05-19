import contextlib
import os

from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def is_odbc_connection(connection_string):
    """Check if the connection string is for an ODBC connection."""
    if "SERVER=" in connection_string:
        logger.info("ODBC connection detected!")
        return True
    return False


@contextlib.contextmanager
def get_session(conn_string=None, echo=False):
    """Get a database session."""
    """
    To enable ssl
    connect_args={'ssl_verify_cert': True}
    """
    if is_odbc_connection(conn_string):
        from urllib.parse import quote_plus

        import pyodbc

        driver = pyodbc.drivers()[0]
        connection_string = f"DRIVER={driver};{conn_string}"

        quoted = quote_plus(connection_string)
        engine = create_engine("mssql+pyodbc:///?odbc_connect={}".format(quoted))

    else:
        con_args = {"ssl_verify_cert": True} if os.getenv("SSL", False) else {}
        con_str = conn_string if conn_string else os.getenv("CAI_DB_CONN")
        engine = create_engine(con_str, connect_args=con_args, echo=echo)

    session_cls = sessionmaker(bind=engine)
    session = session_cls()
    yield session
    session.close()
    engine.dispose()
