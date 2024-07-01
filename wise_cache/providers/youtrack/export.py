import os
import requests
import re
from typing import Optional, List, Union
from dotenv import load_dotenv

from wise_cache.core.export import save_md_file
from wise_cache.core.utils import remove_key_recursive, create_dir
from wise_cache.core.formats import (
    remove_invalid_windows_chars_and_emojis,
    get_code_block_meta,
    get_obsidian_style_meta
)
from wise_cache.providers.youtrack.models.article import Article

load_dotenv()
YOUTRACK_SERVICE_URL = os.getenv('YOUTRACK_SERVICE_URL')
YOUTRACK_ISSUE_FIELDS = (
        'id',
        'attachments',
        'childArticles(idReadable)',
        'comments(id)',
        'content',
        'created',
        'externalArticle',
        'hasChildren',
        'hasStar',
        'idReadable',
        'ordinal',
        'parentArticle(name)',
        'pinnedComments',
        'project(name,shortName)',
        'reporter(name,email)',
        'summary',
        'tags(name)',
        'updated',
        'updatedBy(name,email)',
        'visibility'
)


class Extractor:
    def __init__(
            self,
            url: Optional[str] = None,
            fields: Union[list[str], tuple[str]] = YOUTRACK_ISSUE_FIELDS):
        self.url = url if not YOUTRACK_SERVICE_URL else YOUTRACK_SERVICE_URL
        self.fields = fields

    @staticmethod
    def create_articles_objects(data: list):
        for struct in data:
            yield Article(**struct)

    def get_articles_data(self,
                          token,
                          skip: int = None,
                          top: int = None) -> list:

        if self.url is None:
            raise ValueError('No base API URL provided')

        url = f'{self.url}/articles'
        headers = {'Authorization': 'Bearer ' + token,
                   'Content-Type': 'application/json',
                   'Accept': 'application/json'}

        params = {'fields': ','.join(self.fields),
                  '$skip': skip,
                  '$top': top
                  }

        print(f'Getting articles page from {skip} to {top}')
        response = requests.get(url, headers=headers, params=params)

        data = remove_key_recursive(response.json(), '$type')

        return data

    def get_articles(self,
                     token,
                     skip: int = None,
                     top: int = None) -> List[Article]:
        articles_data = self.get_articles_data(token=token,
                                               skip=skip, top=top)
        return [article for article in self.create_articles_objects(articles_data)]


class Exporter:
    def __init__(self, root: str):
        self.root: str = root
        self.articles: Optional[List[Article]] = []

    def export_article(self, article: Article,
                       include_extras: bool = False,
                       include_tags: bool = False,
                       obsidian_style_meta: bool = False,
                       export_path: str = None,
                       remove_emojis_from_summary=False):

        if not export_path:
            export_path = self.root

        if not os.path.isdir(export_path):
            create_dir(f'{export_path}/')

        meta = get_obsidian_style_meta(article) if obsidian_style_meta else get_code_block_meta(article)

        tags = ' '.join(f'#{tag}' for tag in article.tags)

        basic_text = article.content if article.content else ''

        if include_tags:
            meta += f'\ntags: {tags}'

        if include_extras:
            basic_text = (
                    meta
                    + basic_text
            )

        if remove_emojis_from_summary:
            normal_article_title = remove_invalid_windows_chars_and_emojis(
                article.summary)
        else:
            normal_article_title = article.summary

        filename = f'{normal_article_title}.md'
        filepath = f'{self.root}/{filename}'

        if article.has_children:
            parent_dir = f'{self.root}/{normal_article_title}'
            setattr(article, 'parent_dir', parent_dir)
            create_dir(parent_dir)
            filepath = f'{parent_dir}/{filename}'

        save_md_file(path=filepath, content=basic_text)

        return True

