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


if __name__ == '__main__':

    example_ts = 1679406361592

    example_ddtm = convert_timestamp_to_datetime(example_ts)
    print(example_ddtm)

    unacceptable_string = 'Python 🐍'

    acceptable_string = remove_invalid_windows_chars_and_emojis(
        unacceptable_string)

    print(unacceptable_string)
    print(acceptable_string+'.md')