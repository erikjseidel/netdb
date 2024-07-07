from pydantic import BaseModel, ConfigDict, Extra


class BaseColumnModel(BaseModel):
    """
    The Pydantic models used to define column structure are all derived from
    this basic model. Currently only share attibute is that disallowing fields
    which have not been explicitely defined in the relevant Pydantic model.

    """

    model_config = ConfigDict(extra='forbid')


class BaseContainer(BaseColumnModel):
    """
    Base Pydantic "container" type that is inherited by column type specific
    containers. Every column type has its own container type that holds certain
    metadata about the column contained therein as well as the column data.

    """

    __flat__ = False
    __categories__ = []

    weight: int
    datasource: str

    @property
    def categories(self):
        """
        Property method to return available category types for this column.

        """
        return self.__categories__

    @property
    def flat(self):
        """
        Property method to return whether or not this is a "flat" column type.

        """
        return self.__flat__
