#
# snakepit/model/tables.py
#
# Copyright (C) 2009 Damien Churchill <damoxc@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, write to:
#       The Free Software Foundation, Inc.,
#       51 Franklin Street, Fifth Floor
#       Boston, MA    02110-1301, USA.
#

from sqlalchemy import MetaData, Table, Column
from sqlalchemy import ForeignKeyConstraint, PrimaryKeyConstraint, UniqueConstraint
from sqlalchemy import Boolean, Date, DateTime, Integer, String, Text, Float, BLOB

meta = MetaData()

changes = Table('changes', meta,
    Column('id', Integer),
    Column('changeset_id', Integer),
    Column('action', String(1)),
    Column('path', String(255)),
    Column('from_path', String(255), nullable=True),
    Column('from_revision', String(255), nullable=True),
    Column('revision', String(255), nullable=True),
    Column('branch', String(255), nullable=True),
    PrimaryKeyConstraint('id')
)

changesets = Table('changesets', meta,
    Column('id', Integer),
    Column('repository_id', Integer),
    Column('revision', String(255)),
    Column('committer', String(255)),
    Column('committed_on', DateTime),
    Column('comments', Text),
    Column('commit_date', Date, nullable=True),
    Column('scmid', String(255), nullable=True),
    Column('user_id', Integer, nullable=True),
    PrimaryKeyConstraint('id'),
    UniqueConstraint('repository_id', 'revision')
)

changeset_issues = Table('changeset_issues', meta,
    Column('changeset_id', Integer),
    Column('issue_id', Integer),
    UniqueConstraint('changeset_id', 'issue_id')
)

comments = Table('comments', meta,
    Column('id', Integer),
    Column('commented_type', String(30)),
    Column('commented_id', Integer),
    Column('author_id', Integer),
    Column('comments', Text),
    Column('created_on', DateTime),
    Column('updated_on', DateTime),
    PrimaryKeyConstraint('id')
)

enabled_modules = Table('enabled_modules', meta,
    Column('id', Integer),
    Column('project_id', Integer),
    Column('name', String(255)),
    PrimaryKeyConstraint('id')
)

issue_categories = Table('issue_categories', meta,
    Column('id', Integer),
    Column('project_id', Integer),
    Column('name', String(30)),
    Column('assigned_to_id', Integer),
    PrimaryKeyConstraint('id')
)

issue_relations = Table('issue_relations', meta,
    Column('id', Integer),
    Column('issue_from_id', Integer),
    Column('issue_to_id', Integer),
    Column('relation_type', String(255)),
    Column('delay', Integer),
    PrimaryKeyConstraint('id')
)

issue_statuses = Table('issue_statuses', meta,
    Column('id', Integer),
    Column('name', String(30)),
    Column('is_closed', Boolean),
    Column('is_default', Boolean),
    Column('position', Integer),
    PrimaryKeyConstraint('id')
)

issues = Table('issues', meta,
    Column('id', Integer),
    Column('tracker_id', Integer),
    Column('project_id', Integer),
    Column('subject', String(255)),
    Column('description', Text),
    Column('due_date', Date),
    Column('category_id', Integer),
    Column('status_id', Integer),
    Column('assigned_to_id', Integer),
    Column('priority_id', Integer),
    Column('fixed_version_id', Integer),
    Column('author_id', Integer),
    Column('lock_version', Integer),
    Column('created_on', DateTime),
    Column('updated_on', DateTime),
    Column('start_date', Date),
    Column('done_ratio', Integer),
    Column('estimated_hours', Float),
    PrimaryKeyConstraint('id')
)

journal_details = Table('journal_details', meta,
    Column('id', Integer),
    Column('journal_id', Integer),
    Column('property', String(30)),
    Column('prop_key', String(30)),
    Column('old_value', String(255)),
    Column('value', String(255)),
    PrimaryKeyConstraint('id')
)

journals = Table('journals', meta,
    Column('id', Integer),
    Column('journalized_id', Integer),
    Column('journalized_type', String(30)),
    Column('user_id', Integer),
    Column('notes', Text),
    Column('created_on', DateTime),
    PrimaryKeyConstraint('id')
)

news = Table('news', meta,
    Column('id', Integer),
    Column('project_id', Integer),
    Column('title', String(60)),
    Column('summary', String(255)),
    Column('description', Text),
    Column('author_id', Integer),
    Column('created_on', DateTime),
    Column('comments_count', Integer),
    PrimaryKeyConstraint('id')
)

projects = Table('projects', meta,
    Column('id', Integer),
    Column('name', String(30)),
    Column('description', Text),
    Column('homepage', String(255)),
    Column('is_public', Boolean),
    Column('parent_id', Integer),
    Column('projects_count', Integer),
    Column('created_on', DateTime),
    Column('updated_on', DateTime),
    Column('identifier', String(20)),
    Column('status', Integer),
    PrimaryKeyConstraint('id')
)

projects_trackers = Table('projects_treackers', meta,
    Column('project_id', Integer),
    Column('tracker_id', Integer)
)

queries = Table('queries', meta,
    Column('id', Integer),
    Column('project_id', Integer),
    Column('name', String(255)),
    Column('filters', Text),
    Column('user_id', Integer),
    Column('is_public', Boolean),
    Column('column_names', Text),
    PrimaryKeyConstraint('id')
)

repositories = Table('repositories', meta,
    Column('id', Integer),
    Column('project_id', Integer),
    Column('url', String(255)),
    Column('login', String(60)),
    Column('password', String(60)),
    Column('root_url', String(255)),
    Column('type', String(255)),
    PrimaryKeyConstraint('id')
)

roles = Table('roles', meta,
    Column('id', Integer),
    Column('name', String(30)),
    Column('position', Integer),
    Column('assignable', Boolean),
    Column('builtin', Integer),
    Column('permissions', Text),
    PrimaryKeyConstraint('id')
)

settings = Table('settings', meta,
    Column('id', Integer),
    Column('name', String(30)),
    Column('value', Text),
    Column('updated_on', DateTime),
    PrimaryKeyConstraint('id')
)

trackers = Table('trackers', meta,
    Column('id', Integer),
    Column('name', String(30)),
    Column('is_in_chlog', Boolean),
    Column('position', Integer),
    Column('is_in_roadmap', Boolean),
    PrimaryKeyConstraint('id')
)

user_preferences = Table('user_preferences', meta,
    Column('id', Integer),
    Column('user_id', Integer),
    Column('others', Text),
    Column('hide_mail', Boolean),
    Column('time_zone', String(255)),
    PrimaryKeyConstraint('id')
)

users = Table('users', meta,
    Column('id', Integer),
    Column('login', String(40)),
    Column('hashed_password', String(40)),
    Column('firstname', String(30)),
    Column('lastname', String(30)),
    Column('mail', String(60)),
    Column('mail_notification', Integer(1)),
    Column('admin', Boolean),
    Column('status', Integer),
    Column('last_login_on', DateTime),
    Column('language', String(5)),
    Column('auth_source_id', Integer),
    Column('created_on', DateTime),
    Column('updated_on', DateTime),
    Column('type', String(255)),
    PrimaryKeyConstraint('id')
)

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

watchers = Table('watchers', meta,
    Column('id', Integer),
    Column('watchable_type', String(255)),
    Column('watchable_id', Integer),
    Column('user_id', Integer)
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
    PrimaryKeyConstraint('id')
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
    PrimaryKeyConstraint('id')
)

workflows = Table('workflows', meta,
    Column('id', Integer),
    Column('tracker_id', Integer),
    Column('old_status_id', Integer),
    Column('new_status_id', Integer),
    Column('role_id', Integer),
    PrimaryKeyConstraint('id')
)