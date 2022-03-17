from sqlalchemy import Column, Integer, inspect

from db import Base, engine
from triggers_extension.ddl import CreateTrigger, Trigger


class MySuperTable(Base):
    __tablename__ = 'my_super_table'

    __triggers__ = [
        Trigger(
            name='delete_old_row',
            mode=CreateTrigger.AFTER_MODE,
            events=CreateTrigger.INSERT,
            for_each=CreateTrigger.FOR_EACH_ROW,
            procedure='delete_old_row',
            arguments=['3'],
            condition='NEW.id > 5'
        )
    ]

    id = Column(Integer, primary_key=True)


if __name__ == '__main__':
    Base.metadata.drop_all(engine, tables=[inspect(MySuperTable).selectable])
    Base.metadata.create_all(engine)
