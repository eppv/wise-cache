import datetime
import re
from typing import Optional


def convert_timestamp_to_datetime(timestamp: Optional[int]) -> Optional[datetime.datetime]:
    """Convert a Unix timestamp in milliseconds to a datetime object. Return None if the timestamp is invalid."""
    if timestamp is None:
        return None
    try:
        # Convert milliseconds to seconds
        return datetime.datetime.fromtimestamp(timestamp / 1000.0)
    except (OSError, ValueError) as e:
        print(f"Invalid timestamp {timestamp}: {e}")
        return None


def remove_invalid_windows_chars_and_emojis(text):
    # Regex pattern to match invalid Windows file/folder characters
    invalid_chars_pattern = re.compile(r'[<>:"/\\|?*]')

    # Regex pattern to match emojis
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002702-\U000027B0"  # dingbats
        "\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE
    )

    # First remove invalid Windows characters
    text = invalid_chars_pattern.sub('', text)
    # Then remove emojis
    text = emoji_pattern.sub('', text)

    return text.strip()


def get_code_block_meta(article):

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
    return meta


def get_obsidian_style_meta(article):
    article.tags.append('inbox')
    meta = f"""---
id: {article.id_readable}
project: {article.project.name}
authors: [{article.reporter.name}, {article.updated_by.name}]
created: {article.created}
updated: {article.updated}
child_articles: {article.child_articles}
tags: {article.tags}
---
"""
    return meta


def replace_exact_links(text, original, replacement):
    pattern = re.escape(original)
    new_text = re.sub(pattern, replacement, text)
    return new_text




if __name__ == '__main__':

    link_str = '[Knowledge Management](https://evgeniypalych.myjetbrains.com/youtrack/articles/BSNS-A-103/Knowledge-Management)'
