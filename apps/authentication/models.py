import hashlib
import uuid

from django.db import models


def _uuid4_str():
    return str(uuid.uuid4())


def hash_token(token: str) -> str:
    """SHA-256 hex digest of a JWT — the portable, fixed-length (64-char) unique
    key stored for blacklisting. Indexing the raw JWT is not portable: a variable
    -length ``TextField`` cannot carry a unique index on MySQL (error 1170), and a
    bounded ``CharField`` risks truncation since JWT length grows with the email
    claim. A fixed 64-char hash indexes cleanly on MySQL, PostgreSQL, and SQLite."""
    return hashlib.sha256(token.encode()).hexdigest()


class BlacklistedToken(models.Model):
    class Meta:
        db_table = 'blacklisted_tokens'

    id = models.CharField(max_length=36, primary_key=True, default=_uuid4_str, editable=False)
    token_hash = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token_hash[:16]
