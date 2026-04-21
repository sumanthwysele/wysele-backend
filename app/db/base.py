# app/db/base.py
from app.db.base_class import Base  # noqa
from app.models.user import User # noqa

# Fix these two lines to match your actual filenames:
from app.models.log import Log  # noqa
from app.models.audit import Audit  # noqa
from app.models.contact import ContactInquiry  # noqa