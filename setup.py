import os
from setuptools import setup

CWD = os.path.abspath(os.path.dirname(__file__))

def get_requirements():
    requirements = None
    req_txt = os.path.join(
        CWD,
        'requirements.txt'
    )

    with open(req_txt, 'r') as f:
        requirements = f.readlines()

    return list(map(
        lambda r: r.rstrip('\n'),
        requirements
    ))

setup(
    install_requires=get_requirements(),
    entry_points={
        'gui_scripts': [
            'auger = auger.__main__:main',
        ],
    }
)
