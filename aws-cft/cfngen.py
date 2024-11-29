"""
This module provides a set of functions and utilities to process template files
containing placeholders, replacing them with content from referenced files, and
saving the processed output as YAML files in a target directory.

The module operates on a source directory, searching recursively for files with
the name "template.yaml". It reads and processes each template, identifying and
replacing placeholders of the form "{{ file_name.extension }}" with the content
from the corresponding file located in the same directory as the template.

Key Features:
- Handles indentation to properly integrate included file content within YAML.
- Supports file inclusion for different formats, with custom handling for YAML.
- Provides robust error handling for missing or empty files.

Main Functions:
- `read_file_content`: Reads the content of a file as a list of lines.
- `match_placeholder`: Identifies and extracts placeholders in a line.
- `process_placeholder`: Replaces placeholders with the content of referenced
  files, applying proper formatting and indentation.
- `generate_processed_content`: Processes all lines of a template file to
  replace placeholders with file content.
- `save_yaml_template`: Saves the processed content to a YAML file.
- `process_templates`: Processes all "template.yaml" files in the source
  directory and saves the results in the target directory.

Classes:
- `EmptyFileError`: A custom exception raised when a referenced file is empty.

The script can be executed directly to process templates by running the main
`process_templates` function. It prints feedback about the source and target
directories, as well as the paths of processed files.

Example Usage:
    python cfngen.py

"""

import os
import re

INDENTATION_SIZE = 2
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
SOURCE_DIR = os.path.join(BASE_DIR, "src")
TARGET_DIR = os.path.join(BASE_DIR, "template")


class EmptyFileError(Exception):
    """
    Exception raised when an operation attempts to process an empty file.

    This exception signals that a file is unexpectedly empty and cannot be
    processed. It is typically raised when a file is expected to contain data
    but is found empty.

    Example:
        if file_size == 0:
            raise EmptyFileError("The file is empty and cannot be processed.")
    """


def read_file_content(file_path):
    """
    Reads the contents of a file and returns its lines as a list.

    This function checks if the file exists at the specified path before
    attempting to read it. If the file does not exist, a FileNotFoundError
    is raised with a descriptive message.

    Args:
        file_path (str): The path to the file to be read.

    Returns:
        list: A list of lines in the file, where each line is a string.

    Raises:
        FileNotFoundError: If the file at the specified path does not exist.

    Example:
        file_contents = read_file_content("example.txt")
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File '{file_path}' not found.")

    with open(file_path, "r", encoding="utf-8") as file:
        return list(file)


def match_placeholder(line):
    """
    Searches for placeholders in the format "{{ file_name.extension }}" within
    a given line.

    This function looks for a placeholder pattern that matches a file name with
    an extension surrounded by curly braces and double quotation marks. If
    found, it extracts the file name, extension, and the indentation level of
    the placeholder, then returns this information in a dictionary.

    Args:
        line (str): The line of text to be searched for a placeholder.

    Returns:
        dict: A dictionary containing:
            - 'line_truncated' (str): The line with the placeholder removed.
            - 'file_name' (str): The extracted file name with its extension.
            - 'indentation' (int): The number of spaces before the placeholder.
        None: If no placeholder is found in the line.

    Example:
        result = match_placeholder('    "{{ example.txt }}" some text')
        # result will be:
        # {
        #    'line_truncated': 'some text',
        #    'file_name': 'example.txt',
        #    'indentation': 4
        # }
    """

    pattern = r'"{{\s*(\S+)\.(\w+)\s*}}"'
    match = re.search(pattern, line)

    if match:
        placeholder = match.group(0)
        file_name = f"{match.group(1)}.{match.group(2)}"
        indentation = len(line) - len(line.lstrip()) + INDENTATION_SIZE

        return {
            "line_truncated": line.replace(placeholder, ""),
            "file_name": file_name,
            "indentation": indentation,
        }
    return None


def process_placeholder(root, file_name, line_truncated, indentation):
    """
    Replaces a placeholder with the content from the referenced file, handling
    indentation.

    This function processes a placeholder by replacing it with the content of
    the referenced file. The content is inserted in place of the placeholder
    in the original line, with proper indentation applied to each line of the
    file content. If the referenced file is empty, an `EmptyFileError` is
    raised.

    Args:
        root (str): The root directory where the referenced file is located.
        file_name (str): The name and extension of the referenced file.
        line_truncated (str): The line with the placeholder removed, where the
            content will be inserted.
        indentation (int): The number of spaces/tabs for indentation to be
            applied to the content of the file.

    Returns:
        list: A list of lines with the placeholder replaced by the content of
            the referenced file.
            - If the file contains one line, the placeholder is replaced with
              that line.
            - If the file contains multiple lines, each line is prepended with
              the appropriate indentation.

    Raises:
        EmptyFileError: If the referenced file is empty or only contains
            whitespace.

    Example:
        result = process_placeholder("/path/to/files", "example.txt", "Some
            text here", 4)
        # result will be:
        # ['Some text here|', '    First line of example.txt',
        #    '    Second line of example.txt']
    """

    file_path = os.path.join(root, file_name)
    file_content = read_file_content(file_path)
    file_ext = os.path.splitext(file_name)[1].lstrip(".")
    if not file_content or all(line.strip() == "" for line in file_content):
        raise EmptyFileError(f"File '{file_path}' is empty.")

    if len(file_content) == 1:
        return [
            line_truncated.replace(
                "\n", f"{(file_content[0]).replace("\n","")}\n"
            )
        ]

    if not file_content[-1].endswith("\n"):
        file_content[-1] += "\n"

    if file_ext.lower() in ["yaml", "yml"]:
        formatted_content = [line_truncated]

        if file_content[0] == "---\n":
            file_content = file_content[1:]

        for line in file_content:
            formatted_line = (
                (" " * indentation + line) if line.strip() else "\n"
            )
            formatted_content.append(formatted_line)
        return formatted_content

    return [line_truncated.replace("\n", "|\n")] + [
        ((" " * indentation) + line if line.lstrip() else "\n")
        for line in file_content
    ]


def generate_processed_content(root, file_content):
    """
    Processes a list of file content lines by replacing any placeholders with
    the content from the referenced files.

    This function iterates over each line in the provided file content,
    searches for placeholders, and processes them by replacing the
    placeholders with the corresponding content from the referenced file.
    Lines without placeholders are retained unchanged.

    Args:
        root (str): The root directory where the referenced files are located.
        file_content (list): A list of lines representing the content of the
            file to be processed.

    Returns:
        list: A list of lines with any placeholders replaced by the content
            from the referenced files.
            - Lines without placeholders are kept as-is.
            - Placeholders are replaced with the content of the referenced
                file, including proper indentation.

    Example:
        processed_content = generate_processed_content("/path/to/files", [
            'Some text {{ example.txt }} more text.',
            'Another line.',
        ])
        # processed_content will be a list with placeholders replaced by the
        # content of 'example.txt'.
    """

    processed_lines = []

    for line in file_content:
        match = match_placeholder(line)

        if match:
            processed_lines.extend(process_placeholder(root, **match))
        else:
            processed_lines.append(line)

    return processed_lines


def save_yaml_template(content, target_file):
    """
    Saves the processed content to a specified YAML file.

    This function ensures that the target directory exists, creating it if
    necessary, and then writes the provided content to the target YAML file.
    The content is expected to be a list of strings, which are concatenated
    and written to the file in UTF-8 encoding.

    Args:
        content (list): A list of strings representing the processed content
            to save to the YAML file.
        target_file (str): The file path where the YAML file will be saved.

    Raises:
        OSError: If there is an issue with creating directories or writing to
            the file.

    Example:
        save_yaml_template(['key: value', 'another_key: another_value'],
            'output/template.yaml')
        # The content is written to 'output/template.yaml'.
    """

    os.makedirs(os.path.dirname(target_file), exist_ok=True)

    with open(target_file, "w", encoding="utf-8") as file:
        file.write("".join(content))


def process_templates():
    """
    Processes the template file in the source directory and saves the
    processed content to the target directory.

    Example:
        process_templates()
        # This will process the "template.yaml" in the SOURCE_DIR,
        # replace the placeholders, and save the results in TARGET_DIR.
    """

    template_path = os.path.join(SOURCE_DIR, "template.yaml")
    output_path = os.path.join(TARGET_DIR, "template.yaml")

    relative_output_path = os.path.relpath(output_path, TARGET_DIR)

    yaml_content = read_file_content(template_path)
    processed_content = generate_processed_content(SOURCE_DIR, yaml_content)
    save_yaml_template(processed_content, output_path)

    print(
        "\n---\nTemplate generated at "
        + f"{TARGET_DIR}/{relative_output_path}.\n---"
    )


if __name__ == "__main__":
    process_templates()
