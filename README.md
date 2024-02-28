# repo-relay

repo-relay is a command-line tool developed in Python that simplifies converting codebases into markdown or HTML documentation. It's designed to support code reviews, create documentation, and share research

## Quick Start

1. **Clone**: `git clone https://github.com/jmelowry/repo-relay.git`
2. **Install**: Navigate to `repo_relay` and run `pip install .`

## Usage

Generate project documentation with:

```bash
repo-relay -d <path/to/project> -o <md|html>
```

- `-d`: Target project directory.
- `-o`: Output format (markdown `md` or HTML `html`).

Default to console output if `-o` is not specified.

Example for HTML output:

```bash
repo-relay -d /home/user/project -o html
```

## Contribute

Open for contributions. Issues and PRs are the way to propose changes or additions.

## License

MIT License.
