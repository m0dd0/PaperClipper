import pytest
import os
import shutil
from tempfile import TemporaryDirectory
from pathlib import Path

from paper2note.paper2note import paper2note

SAMPLE_PAPERS_PATH = Path(__file__).parent / "sample_papers"
ALL_PAPERS = list(SAMPLE_PAPERS_PATH.glob("*.pdf"))


@pytest.fixture
def pdf_folder():
    with TemporaryDirectory() as temp_dir:
        for path in ALL_PAPERS:
            shutil.copy(path, temp_dir)

        yield temp_dir


class TestPaper2Note:
    @pytest.mark.parametrize("pdf", ALL_PAPERS)
    def default(self, pdf):
        paper2note(pdf)

        assert (pdf.parent / f"{pdf.stem}.md").exists()
        assert set(ALL_PAPERS) == set(SAMPLE_PAPERS_PATH.glob("*.pdf")) - set(
            pdf.parent / f"{pdf.stem}.md"
        )

    def note_exists_already(self):
        pass

    def renamed_pdf_exists_already(self):
        pass

    def pdf_rename_pattern(self):
        pass

    def note_target_folder(self):
        pass

    def no_doi_found(self):
        pass

    def pdf_is_not_a_pdf(self):
        pass

    def pdf_does_not_exist(self):
        pass

    def note_template_path(self):
        pass

    def note_template_does_not_exist(self):
        pass
