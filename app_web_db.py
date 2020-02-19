# Импорты SQLAlchemy
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Путь до базы
DB_PAHT = 'sqlite:///albums.sqlite3'

# Базовый класс
Base = declarative_base()

# Описываем свои классы ошибок
class Error(Exception):
    pass


class DublicateAbums(Error):
    pass

class Albums(Base):
    """
    Описывает структуру таблицы album для хранения записей музыкальной библиотеки
    """
    __tablename__ = 'album'

    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)

def connect_db():
    # Соединяемся с DB
    engine = sa.create_engine(DB_PAHT, echo=True)
    # Описание таблицы
    Base.metadata.create_all(engine)
    # Создаем фабрику сессию
    Session = sessionmaker(engine)

    return Session()


def find(artist):
    """
    Поск артиста в базе
    :param artist:
    :return: album
    """
    session = connect_db()
    album = session.query(Albums).filter(Albums.artist == artist).all()
    return album

def save(year, artist, genre, album):
    assert isinstance(year, int), 'Incorrect date'
    assert isinstance(artist, str), 'Incorrect artist'
    assert isinstance(genre, str), 'Incorrect genre'
    assert isinstance(album, str), 'Incorrect album'

    session = connect_db()
    # Чекаем базу на наличие
    saved_album = session.query(Albums).filter(Albums.album == album, Albums.artist == artist).first()
    # проверяем на дубль
    if saved_album is not None:
        raise DublicateAbums(f'Альбом уже существует {saved_album.id}')

    # Создаем объект класса album
    album = Albums(
        year=year,
        artist=artist,
        genre=genre,
        album=album
    )
    session.add(album)
    session.commit()
    return album