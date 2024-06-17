
from wise_cache.providers import youtrack

provider_mapping = {
    'youtrack': youtrack
}


class Provider(object):
    def __init__(self, provider_package):
        self.extractor = provider_package.Extractor
        self.exporter = provider_package.Exporter
        self.url = provider_package.SERVICE_URL
        self.token = provider_package.TOKEN


def load_backend(provider_name: str):

    package = provider_mapping[provider_name]

    return Provider(package)

