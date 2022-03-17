from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import ClauseElement
from sqlalchemy.sql.ddl import DDLElement


class CreateTrigger(DDLElement):
    AFTER_MODE = 'AFTER'
    BEFORE_MODE = 'BEFORE'
    INSTEAD_OF_MODE = 'INSTEAD OF'

    INSERT = 'INSERT'
    UPDATE = 'UPDATE'
    DELETE = 'DELETE'
    TRUNCATE = 'TRUNCATE'

    DEFERRABLE = 'DEFERRABLE'
    NOT_DEFERRABLE = 'NOT DEFERRABLE'
    INITIALLY_IMMEDIATE = 'INITIALLY IMMEDIATE'
    INITIALLY_DEFERRED = 'INITIALLY DEFERRED'

    FOR_EACH_STATEMENT = 'FOR EACH STATEMENT'
    FOR_EACH_ROW = 'FOR EACH ROW'

    def __init__(
            self, name, mode, procedure, events, update_of=None, as_constraint=False, from_foreign_table=None,
            deferrable_mode=None, time_to_check=None, for_each=FOR_EACH_STATEMENT, condition=None, arguments=None,
            comment=None
    ):
        self.name = name
        self.mode = mode
        self.procedure = procedure

        self.events = [events] if isinstance(events, str) else events
        self.update_of = update_of or []

        self.as_constraint = as_constraint
        self.from_foreign_table = from_foreign_table

        self.deferrable_mode = deferrable_mode
        self.time_to_check = time_to_check

        self.for_each = for_each

        self.condition = condition
        self.arguments = arguments or []
        self.comment = comment


# TODO: prevent SQL injections
@compiles(CreateTrigger, 'postgresql')
def create_trigger(element, compiler, **kw):
    sql = ['CREATE']
    if element.as_constraint:
        sql.append('CONSTRAINT')

    sql.append('TRIGGER')
    sql.append(element.name)
    sql.append(element.mode)

    # events
    if element.update_of and CreateTrigger.UPDATE in element.events:
        events = [event for event in element.events if event != CreateTrigger.UPDATE]

        update_of_stmt = f"{CreateTrigger.UPDATE} OF {', '.join(element.update_of)}"  # e.g. UPDATE OF col1, col2, col3
        events.append(update_of_stmt)
    else:
        events = element.events.copy()

    sql.append(' OR '.join(events))

    # table name
    sql.append('ON')
    sql.append(element.target.name)

    # FROM
    if element.from_foreign_table:
        sql.append('FROM')
        sql.append(element.from_foreign_table)

    # DEFERRABLE
    if element.deferrable_mode:
        sql.append(element.deferrable_mode)

        if element.deferrable_mode == CreateTrigger.DEFERRABLE and element.time_to_check:
            sql.append(element.time_to_check)

    # FOR EACH
    sql.append(element.for_each)

    # WHEN
    if element.condition is not None:
        sql.append('WHEN')
        sql.append(f'({element.condition})')

    sql.append('EXECUTE PROCEDURE')

    # procedure
    function_stmt = f"{element.procedure}({', '.join(element.arguments)})"  # e.g. - some_func('arg1', 'arg2', 'arg3')
    sql.append(function_stmt)

    stmt = ' '.join(sql) + ';'

    if element.comment:
        comment = f"COMMENT ON TRIGGER {element.name} ON {element.target.name} IS '{element.comment}';"
        stmt += ' ' + comment

    return stmt


class DropTrigger(DDLElement):
    # on_delete options
    RESTRICT = 'RESTRICT'
    CASCADE = 'CASCADE'

    def __init__(self, name, if_exists=False, on_delete=RESTRICT):
        self.name = name
        self.if_exists = if_exists
        self.on_delete = on_delete


@compiles(DropTrigger, 'postgresql')
def drop_trigger(element, compiler, **kw):
    sql = ['DROP TRIGGER']
    if element.if_exists:
        sql.append('IF EXISTS')

    sql.append(element.name)
    sql.append('ON')
    sql.append(element.target.name)
    sql.append(element.on_delete)

    return ' '.join(sql)


class Trigger:
    # on_delete options

    def __init__(
            self, name, mode, procedure, events, update_of=None, as_constraint=False, from_foreign_table=None,
            deferrable_mode=None, time_to_check=None, for_each=CreateTrigger.FOR_EACH_STATEMENT,
            condition=None, arguments=None, comment=None,
            drop_if_exists=False, on_delete=DropTrigger.RESTRICT
    ):
        self.name = name
        self.mode = mode
        self.procedure = procedure

        self.events = events
        self.update_of = update_of

        self.from_foreign_table = from_foreign_table
        self.as_constraint = as_constraint

        self.deferrable_mode = deferrable_mode
        self.time_to_check = time_to_check

        self.for_each = for_each
        self.condition = condition
        self.arguments = arguments
        self.comment = comment

        self.drop_if_exists = drop_if_exists
        self.on_delete = on_delete

    @property
    def create_ddl_element(self):
        return CreateTrigger(
            name=self.name,
            mode=self.mode,
            procedure=self.procedure,
            events=self.events,
            update_of=self.update_of,
            from_foreign_table=self.from_foreign_table,
            as_constraint=self.as_constraint,
            deferrable_mode=self.deferrable_mode,
            time_to_check=self.time_to_check,
            for_each=self.for_each,
            condition=self.condition,
            arguments=self.arguments,
            comment=self.comment
        )

    @property
    def drop_ddl_element(self):
        return DropTrigger(name=self.name, if_exists=self.drop_if_exists, on_delete=self.on_delete)
