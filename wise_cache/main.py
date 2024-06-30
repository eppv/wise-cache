import os
from wise_cache.providers.backend import load_backend
from wise_cache.core.configparse import read_config
from wise_cache.core.export import (
    get_all_articles,
    export_article_with_children,
    obsidize_links
)


if __name__ == '__main__':

    if config_filepath := os.getenv('CONFIG_FILE'):
        CONFIG = read_config(config_filepath)
    else:
        CONFIG = read_config('config.yml')

    if provider_name := os.getenv('DEFAULT_BACKEND_PROVIDER'):
        provider = load_backend(provider_name)
    else:
        provider_name = CONFIG['source']['provider']
        provider = load_backend(provider_name)

    TOKEN = provider.token

    all_articles = get_all_articles(provider=provider, page_size=460)

    upper_level_article_ids = CONFIG['source']['articles']

    print(upper_level_article_ids)

    root = CONFIG['destination']['root']

    example_article = all_articles[upper_level_article_ids[0]]

    for upper_level_article_id in upper_level_article_ids:
        export_article_with_children(
            provider=provider,
            articles=all_articles,
            article_id=upper_level_article_id,
            export_path=root,
            obsidian_style=True
        )

    # obsidize_links(articles=all_articles, article=example_article)
    #
    # exporter = provider.exporter(root)

    #
    # for id_readable, link in yt_links.items():
    #     obsidian_style_link = f'[[{all_articles[id_readable].summary}]]'
    #
    #     print(f'"{link}" converted to ""{obsidian_style_link}"')
    #
    #     content = replace_exact_links(content, link, obsidian_style_link)

    # exporter.export_article(
    #     example_article,
    #     include_extras=True,
    #     obsidian_style_meta=True
    # )
