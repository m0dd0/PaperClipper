from setuptools import setup

setup(
    name="paper2note",
    version="0.1",
    packages=["paper2note"],
    license="MIT",
    description="",
    long_description=open("README.md").read(),
    install_requires=["pdf2bib", "context_menu"],
    extras_require={"dev": ["pytest", "black"]},
    entry_points={
        "console_scripts": [
            "paper2note = paper2note.main:main",
            "paper2note-context-menu = paper2note.create_context_menu_entry:main",
        ],
    },
    # url='http://github.com/yourusername/your-app-name',
    author="Moritz Hesche",
    author_email="mo.hesche@gmail.com",
)
