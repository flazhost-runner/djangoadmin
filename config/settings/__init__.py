"""Register PyMySQL as the ``MySQLdb`` driver for ``django.db.backends.mysql``.

PyMySQL is pure-Python, so the runtime image needs no ``libmysqlclient-dev`` /
``gcc`` build deps (unlike the ``mysqlclient`` C-extension). This runs on
``config.settings`` package import — before any settings module evaluates
``DATABASES`` or a DB connection is opened.
"""
try:
    import pymysql

    # Django 6.0's mysql backend gates on mysqlclient >= 2.2.1; PyMySQL reports
    # (1, 1, 1). Advertise a compatible version so the gate passes — PyMySQL
    # provides the DB-API surface Django uses via ``install_as_MySQLdb()``.
    # (Verified end-to-end against MySQL 8: migrate + connect succeed.)
    pymysql.version_info = (2, 2, 4, "final", 0)
    pymysql.install_as_MySQLdb()
except ImportError:
    pass
