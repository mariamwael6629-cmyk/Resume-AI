from app.core.database import Base, engine
from app.models import models  # noqa: F401  (ensure models are registered)


def init_db():
    Base.metadata.create_all(bind=engine)
