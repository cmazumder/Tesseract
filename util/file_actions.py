from os import path, remove, rename, walk
from shutil import move, copy2


def append_text_to_file(file_path, *args):
    if path.isdir(file_path):
        print "Cannot write to dir: {}".format(file_path)
    else:
        try:
            with open(file_path, "a+") as version_file:
                for statement in args:
                    version_file.write(str(statement))
                version_file.write("\n")
            version_file.close()
        except IOError as err:
            print "Message: {}\n Args: {}".format(err.message, err.args)
            raise IOError


def file_exists(file_path):
    if path.isfile(file_path):
        return True
    else:
        return False


def delete_file(file_path):
    if file_exists(file_path):
        try:
            remove(file_path)
        except WindowsError as E:
            print E.message
    else:
        print "{} not present, and cannot delete".format(file_path)


def move_from_to_file(source, destination):
    delete_file(destination)
    try:
        move(source, destination)
    except WindowsError as E:
        print E.message


def find_replace_text(file_path, find_text, replace_text):
    if file_exists(file_path):
        file_root = path.dirname(file_path)

        original_file = open(file_path, "r")

        temp_file_name = path.basename(file_path) + ".TMP"
        temp_file_name = path.join(file_root, temp_file_name)
        temp_file = open(temp_file_name, "w")

        for line in original_file:
            if find_text in line:
                temp_file.write(line.replace(find_text, replace_text))
            else:
                temp_file.write(line)
        original_file.close()
        temp_file.close()
        delete_file(file_path)
        rename(temp_file_name, file_path)


def find_replace_text_many(file_path, find_text, replace_text):
    if file_exists(file_path):
        file_root = path.dirname(file_path)

        original_file = open(file_path, "r")

        temp_file_name = path.basename(file_path) + ".TMP"
        temp_file_name = path.join(file_root, temp_file_name)
        temp_file = open(temp_file_name, "w")

        for line in original_file:
            if any(word in line for word in find_text):
                if find_text[0] in line:
                    temp_file.write(line.replace(find_text[0], replace_text[0]))
                elif find_text[1] in line:
                    temp_file.write(line.replace(find_text[1], replace_text[1]))
                elif find_text[2] in line:
                    temp_file.write(line.replace(find_text[2], replace_text[2]))
                elif find_text[3] in line:
                    temp_file.write(line.replace(find_text[3], replace_text[3]))
            else:
                temp_file.write(line)
        original_file.close()
        temp_file.close()
        delete_file(file_path)
        rename(temp_file_name, file_path)


def copy_from_to_file(source, destination):
    if file_exists(source) and path.isdir(path.dirname(destination)):
        if path.basename(source) == path.basename(destination) and file_exists(destination):
            delete_file(destination)
        try:
            copy2(source, destination)
            return True
        except OSError as E:
            print E.message
            return False


def search_file_first_occurrence(search_path, filename):
    result = r''
    # Waking top-down from the root
    for root, dir, files in walk(search_path):
        if filename in files:
            result = path.join(root, filename)
            return result


def search_file_all_occurrence(filename, search_path):
    result = []
    # Waking top-down from the root
    for root, dir, files in walk(search_path):
        if filename in files:
            result.append(path.join(root, filename))
    return result


def create_file(file_path):
    with open(file_path, "w") as file_write:
        file_write.close()
