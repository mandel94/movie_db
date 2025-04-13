from sqlalchemy.orm import sessionmaker, Session
from typing import TypeVar, Generic, Type
from repository import GenericSqlAlchemyRepository
from model.base import Base
from model.orm import Movie, Person, Genre, ProductionCompany, Review, Award, Keyword

from engine import engine

TModel = TypeVar("TModel", bound=Base)

SessionLocal = sessionmaker(bind=engine)

class BaseCRUDService(Generic[TModel]):
    def __init__(self, model_class: Type[TModel]):
        self.db: Session = SessionLocal()
        self.repo = GenericSqlAlchemyRepository(self.db, model_class)

    def add(self, data: dict) -> None:
        instance = self.repo.model_class(**data)
        self.repo.upsert(instance)

    def get(self, reference: int) -> TModel:
        return self.repo.get(reference)

    def list(self):
        return self.repo.list()

    def delete(self, reference: int) -> None:
        self.repo.delete(reference)

    def close(self) -> None:
        self.db.close()


class MovieCRUD(BaseCRUDService[Movie]):
    def __init__(self):
        super().__init__(Movie)

class PersonCRUD(BaseCRUDService[Person]):
    def __init__(self):
        super().__init__(Person)

class GenreCRUD(BaseCRUDService[Genre]):
    def __init__(self):
        super().__init__(Genre)

class ProductionCompanyCRUD(BaseCRUDService[ProductionCompany]):
    def __init__(self):
        super().__init__(ProductionCompany)

class ReviewCRUD(BaseCRUDService[Review]):
    def __init__(self):
        super().__init__(Review)

class AwardCRUD(BaseCRUDService[Award]):
    def __init__(self):
        super().__init__(Award)

class KeywordCRUD(BaseCRUDService[Keyword]):
    def __init__(self):
        super().__init__(Keyword)