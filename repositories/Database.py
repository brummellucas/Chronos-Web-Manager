from app import db
from contextlib import contextmanager

class Database:
    @staticmethod
    @contextmanager
    def session_scope():
        """Fornece um escopo transacional seguro."""
        session = db.session
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()