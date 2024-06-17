import os

def remove_key_recursive(data, key_to_remove='$type'):
    if isinstance(data, dict):
        # Create a new dictionary without the key to remove
        return {
            key: remove_key_recursive(value, key_to_remove)
            for key, value in data.items()
            if key != key_to_remove
        }
    elif isinstance(data, list):
        # Process each item in the list
        return [remove_key_recursive(item, key_to_remove) for item in data]
    else:
        # Return the data as is if it's neither a dict nor a list
        return data


def create_dir(path):

    if os.path.exists(path):
        if not os.path.isdir(path):
            path, tail = os.path.split(path)
    else:
        print(f'Directory already exists: {path}')

    path = './' if path == '' else path

    try:
        os.makedirs(path)
        print(f'A directory created by given path: {path}')
        return path
    except FileExistsError:
        print(f'Directory already exists: {path}')
        return None

