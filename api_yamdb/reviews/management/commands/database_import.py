import io
import logging
from csv import DictReader

from django.core.management import BaseCommand

from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import ReviewUser

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO
)

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""

LIST_OF_TABLES = [Category, Genre, Title, GenreTitle, Review, Comment]


class Command(BaseCommand):
    help = 'Loads data from children.csv'

    def handle(self, *args, **options):
        for tables in LIST_OF_TABLES:
            if tables.objects.exists():
                logging.warning('data already loaded...exiting.')
                raise Exception(ALREDY_LOADED_ERROR_MESSAGE)

        logging.info('Loading - data into a table - Category')
        for row in DictReader(
            io.open('static/data/category.csv', mode="r", encoding="utf-8")
        ):
            Category.objects.get_or_create(
                name=row['name'],
                slug=row['slug']
            )
        logging.info('Successfully - loading data into table - Category')

        logging.info('Loading - data into a table - Genre')
        for row in DictReader(
            io.open('static/data/genre.csv', mode="r", encoding="utf-8")
        ):
            Genre.objects.get_or_create(
                name=row['name'],
                slug=row['slug']
            )
        logging.info('Successfully - loading data into table - Genre')

        logging.info('Loading - data into a table - Title')
        for row in DictReader(
            io.open('static/data/titles.csv', mode='r', encoding='utf-8')
        ):
            category = Category.objects.get(pk=row['category'])
            Title.objects.get_or_create(
                name=row['name'],
                year=row['year'],
                category=category
            )
        logging.info('Successfully - loading data into table - Title')

        logging.info('Loading - data into a table GenreTitle')
        for row in DictReader(
            io.open('static/data/genre_title.csv', mode='r', encoding='utf-8')
        ):
            title = Title.objects.get(pk=row['title_id'])
            genre = Genre.objects.get(pk=row['genre_id'])
            GenreTitle.objects.get_or_create(
                title=title,
                genre=genre
            )
        logging.info('Successfully - loading data into table - GenreTitle')

        logging.info('Loading - data into a table ReviewUser')
        for row in DictReader(
            io.open('static/data/users.csv', mode='r', encoding='utf-8')
        ):
            ReviewUser.objects.get_or_create(
                id=row['id'],
                username=row['username'],
                email=row['email'],
                role=row['role'],
                bio=row['bio'],
                first_name=row['first_name'],
                last_name=row['last_name']
            )
        logging.info('Successfully - loading data into table - ReviewUser')

        logging.info('Loading - data into a table - Review')
        for row in DictReader(
            io.open('static/data/review.csv', mode='r', encoding='utf-8')
        ):
            title = Title.objects.get(pk=row['title_id'])
            author = ReviewUser.objects.get(pk=row['author'])
            Review.objects.get_or_create(
                title=title,
                text=row['text'],
                author=author,
                score=row['score'],
                pub_date=row['pub_date']
            )
        logging.info('Successfully - loading data into table - Review')

        logging.info('Loading - data into a table - Comment')
        for row in DictReader(
            io.open('static/data/comments.csv', mode='r', encoding='utf-8')
        ):
            review = Review.objects.get(pk=row['review_id'])
            author = ReviewUser.objects.get(pk=row['author'])
            Comment.objects.get_or_create(
                review=review,
                text=row['text'],
                author=author,
                pub_date=row['pub_date']
            )
        logging.info('Successfully - loading data into table - Comment')
