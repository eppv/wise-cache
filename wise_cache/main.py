import os
from providers.backend import load_backend

provider = load_backend('youtrack')


TOKEN = provider.token


def get_all_articles(extractor, page_size: int = 50):
    skip = 0
    top = page_size
    current_page_size = page_size

    articles: list[provider.Article] = []
    while page_size <= current_page_size:
        current_page = extractor.get_articles_data(
            token=TOKEN,
            skip=skip,
            top=top)
        current_page_size = len(current_page)
        skip += page_size
        top += page_size
        current_page_articles = provider.extractor.create_articles_objects(
            data=current_page)
        articles.extend(current_page_articles)

    articles_dict = {article.id_readable: article for article in articles}

    return articles_dict


def export_article_with_children(articles, article_id: str, export_path: str = None):

    article_to_export = articles[article_id]
    exporter = provider.exporter(export_path)
    print(f'Saving {article_to_export.id_readable} to {exporter.root}/{article_to_export.summary}')
    exporter.export_article(article_to_export, export_path)
    if article_to_export.has_children:
        print(f'Parent dir: {article_to_export.parent_dir}')
        for child in article_to_export.child_articles:
            child_id = child['idReadable']
            print(child_id)
            child_to_export = articles[child_id]
            child_export_path = article_to_export.parent_dir
            export_article_with_children(articles, child_to_export.id_readable, export_path=child_export_path)

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

    root = os.getenv('URI')

    example_extractor = provider.extractor(fields=fields)
    example_exporter = provider.exporter(root=os.getenv('URI'))

    all_articles = get_all_articles(extractor=example_extractor, page_size=450)

    upper_level_article_ids = ['PRVT-A-1', 'PRVT-A-10', 'BSNS-A-107']

    for upper_level_article_id in upper_level_article_ids:
        export_article_with_children(articles=all_articles, article_id=upper_level_article_id, export_path=root)

    # exporter.export_article(example_article, include_extras=True)



