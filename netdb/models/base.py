from pydantic import BaseModel, Extra

class BaseColumnModel(BaseModel):
    class Config:
        extra = Extra.forbid


class BaseContainer(BaseColumnModel):
    __flat__ = False
    __categories__ = []

    weight: int
    datasource: str

    @property
    def categories(self):
        return self.__categories__

    @property
    def flat(self):
        return self.__flat__
