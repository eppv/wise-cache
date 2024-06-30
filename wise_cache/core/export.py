
def get_all_articles(provider, page_size: int = 50):
    skip = 0
    top = page_size
    current_page_size = page_size

    extractor = provider.extractor()

    articles: list[provider.Article] = []
    while page_size <= current_page_size:
        current_page = extractor.get_articles_data(
            token=provider.token,
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


def export_article_with_children(
        provider,
        articles: dict,
        article_id: str,
        export_path: str = None):

    article_to_export = articles[article_id]
    exporter = provider.exporter(export_path)
    print(f'Saving {article_to_export.id_readable} '
          f'to {exporter.root}/{article_to_export.summary}')
    exporter.export_article(article_to_export, export_path)
    if article_to_export.has_children:
        print(f'Parent dir: {article_to_export.parent_dir}')
        for child in article_to_export.child_articles:
            child_id = child['idReadable']
            print(child_id)
            child_to_export = articles[child_id]
            child_export_path = article_to_export.parent_dir
            export_article_with_children(
                provider,
                articles,
                child_to_export.id_readable,
                export_path=child_export_path)


def save_md_file(path: str, content: str):
    try:
        with open(path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"File '{path}' has been saved successfully.")
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")
