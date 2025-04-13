import abc
from typing import List, Any

class AbstractRepository(abc.ABC):
    """
    Abstract base class for repositories. Defines the required methods 
    for any repository implementation that interacts with data storage.
    """

    @abc.abstractmethod
    def add(self, data: Any) -> None:
        """Adds an object to the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, value: Any, by: str = "reference") -> Any:
        """Retrieves an object from the repository by reference or title."""
        raise NotImplementedError

    @abc.abstractmethod
    def list(self) -> List[Any]:
        """Returns a list of all objects stored in the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, reference: Any, updated_data: dict) -> Any:
        """Updates a record by reference."""
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, reference: Any) -> None:
        """Deletes a record by reference."""
        raise NotImplementedError
