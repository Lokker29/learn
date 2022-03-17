from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeMeta, declarative_base

from triggers_extension.mixins import TriggerExtensionMixin


class BaseDeclarativeMeta(TriggerExtensionMixin, DeclarativeMeta):
    pass


engine = create_engine('postgresql://postgres:postgres@0.0.0.0:5432/postgres', echo=True)

Base = declarative_base(metaclass=BaseDeclarativeMeta)
