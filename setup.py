"""clean up build files"""
import atexit
import shutil
from setuptools import setup, find_packages


def cleanup():
    """Remove build files."""
    shutil.rmtree('build', ignore_errors=True)
    shutil.rmtree('dist', ignore_errors=True)
    shutil.rmtree('repo_relay.egg-info', ignore_errors=True)


atexit.register(cleanup)

setup(
    name='repo_relay',
    version='0.1.0',
    url='https://github.com/jmelowry/repo_relay',
    author='Jamie Lowry',
    author_email='08.hockey_stalls@icloud.com',
    description='''
        A Python-based CLI tool that condenses entire codebases \
        into a single markdown or text file for efficient review and analysis.''',
    packages=find_packages(),
    install_requires=[
        'pathspec',
        'gitignore-parser',
        'markdown2'   # library to convert markdown to html
    ],
    entry_points={
        'console_scripts': [
            'repo-relay = repo_relay.main:main',
        ],
    },
)
