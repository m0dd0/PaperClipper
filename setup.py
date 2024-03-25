from setuptools import setup

setup(
    name="paper2note",
    version="0.1",
    packages=["paper2note"],
    license="MIT",
    description="",
    long_description=open("README.md").read(),
    install_requires=[
        "pdf2bib",
        "pdf2doi @ git+https://github.com/m0dd0/pdf2doi.git",  # use the forked version which excludes the document_text method
        "pathvalidate",
    ],
    extras_require={"dev": ["pytest", "black"]},
    entry_points={
        "console_scripts": [
            "paper2note = paper2note.paper2note:commandline_entrypoint",
            "paper2note-context-menu = paper2note.context_menu:commandline_entrypoint",
        ],
    },
    package_data={'': ["templates/*"]},
    include_package_data=True,
    url="https://github.com/m0dd0/paper2note",
    author="Moritz Hesche",
    author_email="mo.hesche@gmail.com",
)
