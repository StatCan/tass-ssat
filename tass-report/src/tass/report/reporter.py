from abc import ABC, abstractmethod


class ReporterABC(ABC):
    @abstractmethod
    def report(self, result):
        pass

    @classmethod
    def __subclasshook__(cls, C):
        if cls is ReporterABC:
            if all(
                any("report" in B.__dict__ for B in C.__mro__),
                any("end_report" in B.__dict__ for B in C.__mro__),
                any("start_report" in B.__dict__ for B in C.__mro__)
            ):
                return True
        return NotImplemented


class ReporterBase(ReporterABC):
    @abstractmethod
    def __init__(self, uuid, *args, **kwargs):
        self._uuid = uuid

    @abstractmethod
    def start_report(self, *args, **kwargs):
        pass

    @abstractmethod
    def report(self, *args, **kwargs):
        pass

    @abstractmethod
    def end_report(self, *args, **kwargs):
        pass
