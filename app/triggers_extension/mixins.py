from sqlalchemy import event, inspect

from triggers_extension.ddl import DropTrigger, Trigger


class TriggerExtensionMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if hasattr(self, '__triggers__'):
            if not isinstance(self.__triggers__, list):
                raise ValueError("'__triggers__' attribute must be a list")

            for element in self.__triggers__:
                if isinstance(element, Trigger):
                    table = inspect(self).selectable

                    event.listen(table, "after_create", element.create_ddl_element)
                    event.listen(table, "before_drop", element.drop_ddl_element)
                else:
                    # TODO: add some warning or error
                    pass
