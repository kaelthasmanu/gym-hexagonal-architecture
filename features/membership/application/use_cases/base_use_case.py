from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar('T')

class BaseUseCase(ABC, Generic[T]):
    @abstractmethod
    async def execute(self, *args, **kwargs) -> T:
        raise NotImplementedError("Subclasses must implement this method")