from setuptools import setup, find_packages

setup(
    name="Block_Bricks",
    version="2.0",
    author="Gabryel-lima",
    author_email="gabbryellimasi@gmail.com",
    description="Block-Bricks is a 2D puzzle game implemented in Python using Pygame. It draws inspiration from classic 2D block games, challenging players to clear the board by eliminating groups of blocks. Have fun and test your puzzle-solving skills in this addictive game!",
    long_description=open('./README.md').read(),
    long_description_content_type='./Block-Bricks.md',
    url="https://github.com/Gabryel-lima/Block-Bricks-Public",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "tensorflow>=2.0",
        "pygame-ce",
        "numpy"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            #'block-bricks=block_bricks.main:main',
        ],
    },
)
