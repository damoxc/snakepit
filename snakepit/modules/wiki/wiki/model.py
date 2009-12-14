from sqlalchemy import MetaData, Table, Column
from sqlalchemy import ForeignKeyConstraint, PrimaryKeyConstraint, UniqueConstraint
from sqlalchemy import Boolean, Date, DateTime, Integer, String, Text, Float, BLOB
from sqlalchemy.orm import mapper, relation, backref

from snakepit.model import meta, Project

versions = Table('versions', meta,
    Column('id', Integer),
    Column('project_id', Integer),
    Column('name', String(255)),
    Column('description', String(255)),
    Column('effective_date', Date),
    Column('created_on', DateTime),
    Column('updated_on', DateTime),
    Column('wiki_page_title', String(255)),
    PrimaryKeyConstraint('id')
)

wiki_content_versions = Table('wiki_content_versions', meta,
    Column('id', Integer),
    Column('wiki_content_id', Integer),
    Column('page_id', Integer),
    Column('author_id', Integer),
    Column('data', BLOB),
    Column('compression', String(6)),
    Column('comments', String(255)),
    Column('updated_on', DateTime),
    Column('version', Integer),
    PrimaryKeyConstraint('id')
)

wiki_contents = Table('wiki_contents', meta,
    Column('id', Integer),
    Column('page_id', Integer),
    Column('author_id', Integer),
    Column('text', Text),
    Column('comments', String(255)),
    Column('updated_on', DateTime),
    Column('version', Integer),
    PrimaryKeyConstraint('id')
)

wiki_pages = Table('wiki_pages', meta,
    Column('id', Integer),
    Column('wiki_id', Integer),
    Column('title', String(255)),
    Column('created_on', DateTime),
    Column('protected', Boolean),
    Column('parent_id', Integer),
    PrimaryKeyConstraint('id'),
    ForeignKeyConstraint(
        ['wiki_id'],
        ['wikis.id']
    )
)

wiki_redirects = Table('wiki_redirects', meta,
    Column('id', Integer),
    Column('wiki_id', Integer),
    Column('title', String(255)),
    Column('redirects_to', String(255)),
    Column('created_on', DateTime),
    PrimaryKeyConstraint('id')
)

wikis = Table('wikis', meta,
    Column('id', Integer),
    Column('project_id', Integer),
    Column('start_page', String(255)),
    Column('status', Integer),
    PrimaryKeyConstraint('id'),
    ForeignKeyConstraint(
        ['project_id'],
        ['projects.id']
    )
)

class Wiki(object):
    pass

class WikiPage(object):
    pass

mapper(WikiPage, wiki_pages)
mapper(Wiki, wikis, properties = {
    'project': relation(Project, backref=backref('wiki', uselist=False), uselist=False),
    'pages': relation(WikiPage, backref=backref('wiki', uselist=False))
})