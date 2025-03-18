import abc
from model import Movie

# https://www.cosmicpython.com/book/chapter_02_repository.html

class AbstractRepository(abc.ABC):
    """
    Abstract base class for repositories. Defines the required methods 
    for any repository implementation that interacts with data storage.

    Methods:
        add(data): Adds a new record to the repository.
        get(reference): Retrieves a record by its unique reference.
    
    Example:
        class InMemoryRepository(AbstractRepository):
            def __init__(self):
                self._data = {}

            def add(self, movie: Movie):
                self._data[movie.id] = movie

            def get(self, reference):
                return self._data.get(reference)
    """

    @abc.abstractmethod
    def add(self, data):
        """
        Adds an object to the repository.
        
        Args:
            data: The object to be added to the repository.

        Raises:
            NotImplementedError: If the method is not implemented by a subclass.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference):
        """
        Retrieves an object from the repository by reference.

        Args:
            reference: The unique identifier of the object.

        Returns:
            An instance of the stored object.

        Raises:
            NotImplementedError: If the method is not implemented by a subclass.
        """
        raise NotImplementedError


class MovieSqlAlchemyRepository(AbstractRepository):
    """
    SQLAlchemy-based repository implementation for managing Movie records.

    Args:
        session: SQLAlchemy session object used for database transactions.

    Methods:
        add(data): Adds a Movie object to the database session.
        get(reference): Retrieves a Movie object from the database by reference.
        list(): Returns all Movie objects from the database.

    Example:
        from sqlalchemy.orm import sessionmaker
        from sqlalchemy import create_engine

        engine = create_engine('sqlite:///movies.db')
        Session = sessionmaker(bind=engine)
        session = Session()

        repo = MovieSqlAlchemyRepository(session)
        movie = Movie(id=1, title="Inception", year=2010)
        repo.add(movie)
        session.commit()

        retrieved_movie = repo.get(1)
        print(retrieved_movie.title)  # Output: Inception
    """

    def __init__(self, session):
        """
        Initializes the repository with a database session.

        Args:
            session: An active SQLAlchemy session.
        """
        self.session = session
        self.model_class = Movie

    def add(self, data):
        """
        Adds a Movie instance to the session.

        Args:
            data (Movie): The movie instance to add.

        Example:
            movie = Movie(id=1, title="Interstellar", year=2014)
            repo.add(movie)
            session.commit()
        """
        self.session.add(data)

    def get(self, value, by="reference"):
        """
        Retrieves a Movie instance by a given attribute.

        Args:
            value: The value to search for.
            by (str): The attribute to filter by ('reference' or 'title').

        Returns:
            Movie: The retrieved Movie instance.

        Example:
            # Get movie by reference
            retrieved_movie = repo.get(1)
            print(retrieved_movie.title)

            # Get movie by title
            retrieved_movie = repo.get("Inception", by="title")
            print(retrieved_movie.title)
        """
        if by == "reference":
            return self.session.query(self.model_class).filter_by(reference=value).one()
        elif by == "title":
            return self.session.query(self.model_class).filter_by(title=value).one()
        else:
            raise ValueError("Invalid filter. Use 'reference' or 'title'.")


    def list(self):
        """
        Returns all movies stored in the database.

        Returns:
            Query: A SQLAlchemy query object containing all movies.

        Example:
            movies = repo.list().all()
            for movie in movies:
                print(movie.title)
        """
        return self.session.query(self.model_class)
