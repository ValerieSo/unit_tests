from random import choice
import pytest


class TestBooksCollector:

    # метод add_new_book добавляет книги в словарь books_genre
    def test_add_new_book_add_two_books_sucsessful(self, collector):
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')
        assert len(collector.get_books_genre()) == 2

    # метод add_new_book добавляет книги с валидным названием
    @pytest.mark.parametrize('name', [
        'Я',  # граничное значение
        'Мы',  # приграничное значение
        'Lorem ipsum dolor sit amet, consectetuer',  # граничное значение
        'Lorem ipsum dolor sit amet, consectetue',  # приграничное значение
        'Название',  # значение внутри диапазона
        '1984',  # числа в строке
        'Соб@ка!'  # спецсимволы в строке
     ])
    def test_add_new_book_valid_name_succesful(self, collector, name):
        collector.add_new_book(name)
        assert name in collector.get_books_genre()

    # метод add_new_book не добавляет книги с невалидным названием
    @pytest.mark.parametrize('bad_name', [
        'Lorem ipsum dolor sit amet, consectetuera',
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla vulputate, nunc sit amet mattis volutpat, dolor dolor rutrum justo, ac vulputate quam massa in odio. Suspendisse potenti.',
        ''
    ])
    def test_add_new_book_invalid_name_unsuccessful(self, collector, bad_name):
        collector.add_new_book(bad_name)
        assert bad_name not in collector.get_books_genre()

    # метод add_new_book добавляет новую книгу в словарь без жанра
    def test_add_new_book_book_added_without_genre(self, collector):
        collector.add_new_book('Мы')
        book_genre = collector.books_genre.get('Мы')
        assert book_genre == ''

    # метод set_book_genre назначает допустимый жанр книге
    def test_set_book_genre_valid_genre_successful(self, collector):
        collector.add_new_book('Название')
        valid_genre = choice(collector.genre)
        collector.set_book_genre('Название', valid_genre)
        book_genre = collector.books_genre.get('Название')
        assert book_genre == valid_genre

    # метод set_book_genre не назначает недопустимый жанр книге
    def test_set_book_genre_invalid_genre_result_not_set(self, collector):
        collector.add_new_book('Название')
        collector.set_book_genre('Название', 'Комикс')
        books_genre = collector.books_genre.get('Название')
        assert books_genre == ''

    # метод set_book_genre не назначает жанр несуществующей книге
    def test_set_book_genre_nonexistent_book_none(self, collector):
        collector.set_book_genre('НЛО', 'Детектив')
        assert collector.books_genre.get('НЛО') is None

    # метод get_book_genre выводит жанр книги по ее названию
    def test_get_book_genre_fiction_book_shows_fiction_genre(self, collector):
        collector.add_new_book('Война миров')
        collector.set_book_genre('Война миров', 'Фантастика')
        correct_genre = collector.books_genre.get('Война миров')
        assert correct_genre == 'Фантастика'

    # метод get_books_with_specific_genre выводит книги с определенным жанром
    def test_get_books_with_specific_genre_only_fiction_true(self, collector):
        collector.add_new_book('Война миров')
        collector.set_book_genre('Война миров', 'Фантастика')
        collector.add_new_book('Киберзолушка')
        collector.set_book_genre('Киберзолушка', 'Фантастика')
        collector.add_new_book('Клуб убийств по четвергам')
        collector.set_book_genre('Клуб убийств по четвергам ', 'Детективы')
        fiction = collector.get_books_with_specific_genre('Фантастика')
        assert 'Война миров' in fiction and 'Киберзолушка' in fiction

    # метод get_books_genre возвращает словарь
    def test_get_books_genre_initial_setup_return_dict(self, collector):
        expected_result = {}
        result = collector.get_books_genre()
        assert result == expected_result

    # метод get_books_for_children возвращает книги с допустимым жанром Фантастика
    def test_get_books_for_children_book_with_suitable_genre_fiction_added_for_children(self, collector):
        collector.add_new_book('Киберзолушка')
        collector.set_book_genre('Киберзолушка', 'Фантастика')
        books_for_children = collector.get_books_for_children()
        assert 'Киберзолушка' in books_for_children

    # метод get_books_for_children возвращает книги с допустимым жанром Мультфильмы
    def test_get_books_for_children_book_with_suitable_genre_cartoon_added_for_children(self, collector):
        collector.add_new_book('Винни-Пух')
        collector.set_book_genre('Винни-Пух', 'Мультфильмы')
        books_for_children = collector.get_books_for_children()
        assert 'Винни-Пух' in books_for_children

    # метод get_books_for_children возвращает книги с допустимым жанром Комедии
    def test_get_books_for_children_book_with_suitable_genre_comedy_added_for_children(self, collector):
        collector.add_new_book('Ревизор')
        collector.set_book_genre('Ревизор', 'Комедии')
        books_for_children = collector.get_books_for_children()
        assert 'Ревизор' in books_for_children

    # метод get_books_for_children не возвращает книги с неподходящим жанром Детективы
    def test_get_books_for_children_book_with_restricted_genre_detective_not_added_for_children(self, collector):
        collector.add_new_book('Клуб убийств по четвергам')
        collector.set_book_genre('Клуб убийств по четвергам', 'Детективы')
        books_for_children = collector.get_books_for_children()
        assert books_for_children == []

    # метод get_books_for_children не возвращает книги с неподходящим жанром Ужасы
    def test_get_books_for_children_book_with_restricted_genre_horror_not_added_for_children(self, collector):
        collector.add_new_book('Хребты безумия')
        collector.set_book_genre('Хребты безумия', 'Ужасы')
        books_for_children = collector.get_books_for_children()
        assert books_for_children == []

    # метод add_book_in_favorites добавляет книгу в избранное
    def test_add_book_in_favorites_one_book_successful(self, collector):
        collector.add_new_book('Киберзолушка')
        collector.add_book_in_favorites('Киберзолушка')
        assert 'Киберзолушка' in collector.favorites

    #  метод add_book_in_favorites не создает дубли книги в избранном при повторном добавлении
    def test_add_book_in_favorites_same_book_twice_no_double_in_list(self, collector):
        collector.add_new_book('Киберзолушка')
        collector.add_book_in_favorites('Киберзолушка')
        collector.add_book_in_favorites('Киберзолушка')
        assert len(collector.favorites) == 1

    # метод delete_book_from_favorites удаляет книгу из избранного
    def test_delete_book_from_favorites_one_book_empty_list(self, collector):
        collector.add_new_book('Киберзолушка')
        collector.add_book_in_favorites('Киберзолушка')
        collector.delete_book_from_favorites('Киберзолушка')
        assert collector.favorites == []

    # метод delete_book_from_favorites из избранного удаляет только указанную книгу
    def test_delete_book_from_favorites_one_book_other_books_stay(self, collector):
        collector.add_new_book('Киберзолушка')
        collector.add_new_book('Клуб убийств по четвергам')
        collector.add_book_in_favorites('Киберзолушка')
        collector.add_book_in_favorites('Клуб убийств по четвергам')
        collector.delete_book_from_favorites('Киберзолушка')
        assert 'Клуб убийств по четвергам' in collector.favorites and 'Киберзолушка' not in collector.favorites

    # метод get_list_of_favorites_books возвращает список избранных книг
    def test_get_list_of_favorites_books_two_books_succesful(self, collector):
        collector.add_new_book('Киберзолушка')
        collector.add_new_book('Клуб убийств по четвергам')
        collector.add_book_in_favorites('Киберзолушка')
        collector.add_book_in_favorites('Клуб убийств по четвергам')
        favorite_books = collector.get_list_of_favorites_books()
        assert 'Клуб убийств по четвергам' in favorite_books and 'Киберзолушка' in favorite_books
