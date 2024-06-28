import os
import requests
from typing import Optional, List
from dotenv import load_dotenv

from wise_cache.core.utils import remove_key_recursive, create_dir
from wise_cache.core.formats import remove_invalid_windows_chars_and_emojis

from wise_cache.providers.youtrack.models.article import Article

load_dotenv()
YOUTRACK_SERVICE_URL = os.getenv('YOUTRACK_SERVICE_URL')


def save_md_file(path: str, content: str):
    try:
        with open(path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"File '{path}' has been saved successfully.")
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")


class Extractor:
    def __init__(self, url: Optional[str] = None, fields: Optional[List[str]] = None):
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
                       export_path: str = None):

        if not export_path:
            export_path = self.root

        if not os.path.isdir(export_path):
            create_dir(f'{export_path}/')

        meta = f"""

```yaml
id: {article.id_readable}
project: {article.project.name}
authors: [{article.reporter.name}, {article.updated_by.name}]
created: {article.created}
updated: {article.updated}
child_articles: {article.child_articles}
```

"""

        tags = ' '.join(f'#{tag}' for tag in article.tags)

        basic_text = article.content if article.content else ''

        if include_extras:
            basic_text = article.summary + meta + tags + basic_text

        # normal_article_title = remove_invalid_windows_chars_and_emojis(
        #     article.summary)
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

