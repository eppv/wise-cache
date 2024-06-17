import os
from providers.backend import load_backend

provider = load_backend('youtrack')


TOKEN = provider.token

if __name__ == '__main__':

    fields = [
        'id',
        # 'attachments',
        'childArticles(idReadable)',
        # 'comments(id)',
        'content',
        'created',
        # 'externalArticle',
        'hasChildren',
        # 'hasStar',
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
        # 'visibility'
    ]

    extractor = provider.extractor(fields=fields)
    exporter = provider.exporter(root=os.getenv('URI'))

    article_dicts = extractor.get_articles_data(token=TOKEN,
                                                skip=0, top=50)

    i = 0
    for article in article_dicts:
        i += 1
        print(f'Article {i} {article["summary"]}: {article}')

    print(article_dicts[0])

    articles = [article for article in provider.extractor.create_articles_objects(data=article_dicts)]

    example_article = articles[0]
    print(example_article.parent_article)

    exporter.export_article(example_article, include_extras=True)



