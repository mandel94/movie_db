from typing import Type, List, TypeVar, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from model.base import Base  # Ensure that `Base` is imported from your models module
from repository import AbstractRepository

# Create a TypeVar to ensure only models derived from Base are accepted
TModel = TypeVar('TModel', bound=Base) # type: ignore

class GenericSqlAlchemyRepository(AbstractRepository, Type[TModel]):
    """
    A generic repository class for managing any SQLAlchemy model.

    This class abstracts the SQLAlchemy CRUD operations for any given model.

    Args:
        session: SQLAlchemy session object used for database transactions.
        model_class: The SQLAlchemy model class to be managed by this repository.
    """

    def __init__(self, session: Session, model_class: Type[TModel]):
        """
        Initializes the repository with a database session and a model class.
        
        Args:
            session: SQLAlchemy session object.
            model_class: The model class (which is a subclass of `Base`).
        """
        self.session = session
        self.model_class = model_class

    def add(self, data: TModel) -> None:
        """Adds an object to the session."""
        self.session.add(data)
        self.session.commit()

    def get(self, value: int, by: str = "reference") -> TModel:
        """
        Retrieves an object by its unique reference or another attribute.
        
        Args:
            value: The value to search for.
            by (str): The attribute to filter by (e.g., 'reference', 'name', etc.).
        
        Returns:
            TModel: The retrieved object instance.

        Raises:
            NoResultFound: If no record is found matching the query.
        """
        if by == "reference":
            result = self.session.query(self.model_class).filter_by(id=value).one_or_none()
        else:
            result = self.session.query(self.model_class).filter_by(**{by: value}).one_or_none()

        if result is None:
            raise NoResultFound(f"No {self.model_class.__name__} found with {by} = {value}")
        
        return result

    def list(self) -> List[TModel]:
        """Returns all instances of the model class stored in the database."""
        return self.session.query(self.model_class).all()

    def update(self, reference: int, updated_data: dict) -> TModel:
        """
        Updates an object in the database.

        Args:
            reference (int): The unique reference (usually the primary key) of the record.
            updated_data (dict): The data to update the object with.

        Returns:
            TModel: The updated object.

        Raises:
            NoResultFound: If no record is found matching the reference.
        """
        obj = self.session.query(self.model_class).filter_by(id=reference).one_or_none()
        if obj is None:
            raise NoResultFound(f"{self.model_class.__name__} with reference {reference} not found.")
        
        for key, value in updated_data.items():
            setattr(obj, key, value)
        
        self.session.commit()
        return obj

    def delete(self, reference: int) -> None:
        """
        Deletes an object from the database.

        Args:
            reference (int): The unique reference (usually the primary key) of the record.
        
        Raises:
            NoResultFound: If no record is found matching the reference.
        """
        obj = self.session.query(self.model_class).filter_by(id=reference).one_or_none()
        if obj is None:
            raise NoResultFound(f"{self.model_class.__name__} with reference {reference} not found.")
        
        self.session.delete(obj)
        self.session.commit()
