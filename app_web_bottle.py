# Импорт подключения к DB
import app_web_db


# Ипорты bottle
from bottle import run, HTTPError, request, route


@route('/albums/<artist>')
def artists(artist):
    all_album = app_web_db.find(artist)
    if not all_album:
        message = f'Альбомы {artist} не найдены'
        result = HTTPError(404, message)
    else:
        album_name = [app_web_db.album for app_web_db in all_album]
        result = f'Кол-во альбомов артиста <strong>{artist} = {len(album_name)}</strong><br>Название альбомов артиста <strong>{artist}</strong><br>'
        result += '<br>'.join(album_name)
    return result

@route('/albums', method='POST')
def create_artist():
    # Берем данные формы
    year = request.forms.get('year')
    artist = request.forms.get('artist')
    genre = request.forms.get('genre')
    album_name = request.forms.get('album')

    # Обрабатываем ошибки
    try:
        year = int(year)
    except ValueError:
        return HTTPError(400, 'Указан некорректный год альбома')
    try:
        new_album = app_web_db.save(year, artist, genre, album_name)
    except AssertionError as err:
        result = HTTPError(400, str(err))
    except app_web_db.DublicateAbums as err:
        result = HTTPError(409, str(err))
    else:
        print(f'Альбом создан {new_album.id}')
        result = f'Альбом создан {new_album.id}'
    return result

# Точка входа
if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True)
