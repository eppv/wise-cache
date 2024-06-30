import os
from wise_cache.providers.backend import load_backend
from wise_cache.core.configparse import read_config
from wise_cache.core.export import (
    get_all_articles,
    export_article_with_children
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

    all_articles = get_all_articles(provider=provider, page_size=450)

    upper_level_article_ids = CONFIG['source']['articles']

    print(upper_level_article_ids)

    root = CONFIG['destination']['root']

    for upper_level_article_id in upper_level_article_ids:
        export_article_with_children(
            provider=provider,
            articles=all_articles,
            article_id=upper_level_article_id,
            export_path=root)

    # exporter.export_article(example_article, include_extras=True)
