import os
import argparse
import glob
from pathlib import Path
import pathspec
import mimetypes
import markdown2
import html


def write_to_file_or_print(filename: str, content: str, output_option: str):
    console_formats = ['txt', 'md', 'html']
    if output_option in console_formats:
        print(content)
    elif output_option:
        with open(output_option, 'w') as file:
            file.write(content)
    else:
        print(content)


def get_gitignore(dirpath):
    # Parse .gitignore if present.
    gitignore_file = os.path.join(dirpath, ".gitignore")
    if os.path.isfile(gitignore_file):
        with open(gitignore_file) as f:
            spec = pathspec.PathSpec.from_lines('gitwildmatch', f)
            return spec
    return None


def create_content(dirpath: str, output_option: str):
    content = ""
    gitignore = get_gitignore(dirpath)

    for root, dirs, files in os.walk(dirpath):
        dirs[:] = [d for d in dirs if d != '.git' and d != '__pycache__']
        path = root.split('/')
        indent = len(path) - len(dirpath.split('/')) + 1

        if root != dirpath:
            if gitignore and gitignore.match_file(root):
                continue
            pref = '' if indent <= 0 else '#' * indent + ' '
            folder_line = '{}📂 **{}**\n'.format(pref, os.path.basename(root))
            folder_line_html = markdown2.markdown(folder_line)
            if output_option == 'md':
                content += folder_line
            else:
                content += folder_line_html

        for file in files:
            if gitignore and gitignore.match_file(os.path.join(root, file)):
                continue
            file_line = '📄 **{}**\n'.format(file)
            file_line_html = markdown2.markdown(file_line)
            if output_option == 'md':
                content += file_line
            else:
                content += file_line_html

            mimetype, _ = mimetypes.guess_type(os.path.join(root, file))
            if mimetype and not mimetype.startswith('text'):
                content += ' (binary file)\n'
            else:
                with open(os.path.join(root, file), 'r', errors='ignore') as f:
                    file_content = f.read()
                    if file_content.strip():
                        if output_option == 'md':
                            content += '\n\n```\n{}\n```\n'.format(
                                file_content)
                        else:
                            # Escape markdown special characters and wrap content in HTML code block
                            escaped_content = html.escape(file_content)
                            content += '\n<pre><code>\n{}\n</code></pre>\n'.format(
                                escaped_content)
                    else:
                        content += '\n<pre><code>\n<empty file>\n</code></pre>\n'

    if output_option == 'html':
        stylesheet = """\
        <style>
            body {
                font-family: Arial, sans-serif;
            }
            code, pre {
                background-color: #f2f2f2;
                padding: 2px 4px;
                font-size: 90%;
            }
        </style>
        """
        return '<!DOCTYPE html>\n<html>\n<head>\n' + stylesheet + '\n</head>\n<body>\n' + content + '\n</body>\n</html>'
    else:
        return "# 📂 **{}**\n{}".format(dirpath.split("/")[-1], content)


def main():
    parser = argparse.ArgumentParser(description="Summarize a codebase.")
    parser.add_argument('-d', '--dirpath', default=os.getcwd(),
                        help='Path to the directory')
    parser.add_argument('-o', '--output', help='Output format or output file')

    args = parser.parse_args()

    content = create_content(args.dirpath, args.output)
    write_to_file_or_print(args.output, content, args.output)


if __name__ == "__main__":
    main()
