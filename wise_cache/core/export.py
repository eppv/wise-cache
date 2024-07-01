
from wise_cache.core.formats import replace_exact_links, replace_invalid_filename_chars


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

    articles_dict = {}
    for article in articles:
        setattr(article, 'summary', replace_invalid_filename_chars(filename=article.summary, replacement='.'))
        articles_dict[article.id_readable] = article

    return articles_dict


def obsidize_links(articles: dict, article):
    if article.content is None or article.content == "":
        return
    native_links = article.extract_native_links()
    for id_readable, link_parts in native_links.items():
        link = link_parts['link']
        alias = link_parts['alias']
        try:
            summary = articles[id_readable].summary
            obsidian_style_link = f'[[{summary}]]' if summary == alias else f'[[{summary}|{alias}]]'
        except KeyError:
            obsidian_style_link = f'[[{link.split('/')[-1][:-1]}|{alias}]]'
        print(f'"{link}" converted to ""{obsidian_style_link}"')
        modified_content = replace_exact_links(article.content, link, obsidian_style_link)
        setattr(article, 'content', modified_content)


def export_article_with_children(
        provider,
        articles: dict,
        article_id: str,
        export_path: str = None,
        obsidian_style: bool = False,
):

    article_to_export = articles[article_id]
    exporter = provider.exporter(export_path)
    print(f'Saving {article_to_export.id_readable} '
          f'to {exporter.root}/{article_to_export.summary}')

    if obsidian_style:
        print('Converting format to obsidian-style:')
        obsidize_links(articles, article_to_export)

    exporter.export_article(
        article_to_export,
        export_path,
        obsidian_style_meta=obsidian_style
    )
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
                export_path=child_export_path,
                obsidian_style=True
            )


def save_md_file(path: str, content: str):
    try:
        with open(path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"File '{path}' has been saved successfully.")
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")
