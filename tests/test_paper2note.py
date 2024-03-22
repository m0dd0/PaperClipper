import pytest
import shutil
from tempfile import TemporaryDirectory
from pathlib import Path

from pdf2bib import pdf2bib

from paper2note.paper2note import paper2note

SAMPLE_PAPERS_PATH = Path(__file__).parent / "sample_papers"
PDF_STEMS = [p.stem for p in SAMPLE_PAPERS_PATH.glob("*.pdf")]
PDF_STEMS_TO_TITLE = {
    "2303.04137": "Diffusion Policy: Visuomotor Policy Learning via Action Diffusion",
    "NeurIPS-2023-modelling-cellular-perturbations-with-the-sparse-additive-mechanism-shift-variational-autoencoder-Paper-Conference": "Modelling Cellular Perturbations with the Sparse Additive Mechanism Shift Variational Autoencoder",
    "NIPS-2017-attention-is-all-you-need-Paper": "Attention Is All You Need",
    "nova23a": "Gradient-Free Structured Pruning with Unlabeled Data",
    "wang23ao": "Learning to Bid in Repeated First-Price Auctions with Budgets",
    # for the following paper the wrong title is extracted
    "NeurIPS-2023-cross-episodic-curriculum-for-transformer-agents-Paper-Conference": "Cross-Episodic Curriculum for Transformer Agents",
}
DEFAULT_TEST_PDF_STEM = "2303.04137"


@pytest.fixture
def pdf_folder():
    with TemporaryDirectory() as temp_dir:
        for path in SAMPLE_PAPERS_PATH.glob("*.pdf"):
            shutil.copy(path, temp_dir)

        yield temp_dir


class TestPaper2Note:
    def test_default(self, pdf_folder: str):
        pdf_folder = Path(pdf_folder)
        pdf_path = pdf_folder / f"{DEFAULT_TEST_PDF_STEM}.pdf"

        paper2note(pdf_path)

        assert (pdf_path.parent / f"{pdf_path.stem}.md").exists()
        assert pdf_path.exists()

    def test_note_target_folder(self, pdf_folder: str):
        pdf_folder = Path(pdf_folder)
        pdf_path = pdf_folder / f"{DEFAULT_TEST_PDF_STEM}.pdf"
        note_target_folder = pdf_folder / "notes"

        paper2note(pdf_path, note_target_folder=note_target_folder)

        assert (note_target_folder / f"{DEFAULT_TEST_PDF_STEM}.md").exists()

    def test_note_template(self, pdf_folder: str):
        pdf_folder = Path(pdf_folder)
        pdf_path = pdf_folder / f"{DEFAULT_TEST_PDF_STEM}.pdf"

        note_template_path = pdf_folder / "template.md"
        with note_template_path.open("w") as f:
            f.write("the content of the note is {title} - {year} - {author_1}")

        paper2note(pdf_path, note_template_path=note_template_path)

        assert (pdf_path.parent / f"{pdf_path.stem}.md").exists()
        assert (
            pdf_path.parent / f"{pdf_path.stem}.md"
        ).read_text() == "the content of the note is Diffusion Policy: Visuomotor Policy Learning via Action Diffusion - 2023 - Cheng Chi"

    def test_pdf_rename_pattern(self, pdf_folder: str):
        pdf_folder = Path(pdf_folder)
        pdf_path = pdf_folder / f"{DEFAULT_TEST_PDF_STEM}.pdf"

        paper2note(pdf_path, pdf_rename_pattern="{title} ({year}) {author_1}")

        assert not pdf_path.exists()
        assert (
            pdf_folder
            / "Diffusion Policy Visuomotor Policy Learning via Action Diffusion (2023) Cheng Chi.pdf"
        ).exists()


class TestPaper2NoteEdgeCases:
    def test_note_exists_already(self, pdf_folder: str):
        pdf_folder = Path(pdf_folder)
        pdf_path = pdf_folder / f"{DEFAULT_TEST_PDF_STEM}.pdf"

        existing_note_path = pdf_folder / f"{DEFAULT_TEST_PDF_STEM}.md"
        with existing_note_path.open("w") as f:
            f.write("existing note")

        paper2note(pdf_path)

        assert existing_note_path.exists()
        assert existing_note_path.read_text() == "existing note"

    def test_renamed_pdf_exists_already(self, pdf_folder: str):
        pdf_folder = Path(pdf_folder)
        pdf_path = pdf_folder / f"{DEFAULT_TEST_PDF_STEM}.pdf"

        renamed_pdf_path = pdf_folder / "renamed.pdf"
        with renamed_pdf_path.open("w") as f:
            f.write("existing renamed pdf")

        paper2note(pdf_path, pdf_rename_pattern="renamed")

        assert renamed_pdf_path.exists()
        assert renamed_pdf_path.read_text() == "existing renamed pdf"
        assert pdf_path.exists()
        assert (pdf_folder / "renamed.md").exists()

    def test_no_doi_found(self, pdf_folder: str):
        pdf_folder = Path(pdf_folder)
        pdf_path = pdf_folder / "empty_document.pdf"

        paper2note(pdf_path, pdf_rename_pattern="renamed")

        assert not (pdf_path.parent / "pdf.md").exists()
        assert not (pdf_path.parent / "renamed.md").exists()
        assert not (pdf_path.parent / "renamed.pdf").exists()
        assert pdf_path.exists()

    def test_pdf_is_not_a_pdf(self, pdf_folder: str):
        pdf_folder = Path(pdf_folder)
        non_pdf_path = pdf_folder / "non_pdf.pdf"

        with non_pdf_path.open("w") as f:
            f.write("this is not a pdf")

        paper2note(non_pdf_path, pdf_rename_pattern="renamed")

        assert not (non_pdf_path.parent / "non_pdf.md").exists()
        assert not (non_pdf_path.parent / "renamed.md").exists()
        assert not (non_pdf_path.parent / "renamed.pdf").exists()
        assert non_pdf_path.exists()

    def test_pdf_does_not_exist(self, pdf_folder: str):
        pdf_folder = Path(pdf_folder)
        non_existing_pdf_path = pdf_folder / "non_existing_pdf.pdf"

        with pytest.raises(FileNotFoundError):
            paper2note(non_existing_pdf_path, pdf_rename_pattern="renamed")

        assert not (non_existing_pdf_path.parent / "non_existing_pdf.md").exists()
        assert not (non_existing_pdf_path.parent / "renamed.md").exists()
        assert not (non_existing_pdf_path.parent / "renamed.pdf").exists()
        assert not non_existing_pdf_path.exists()

    def test_note_template_does_not_exist(self, pdf_folder: str):
        pdf_folder = Path(pdf_folder)
        pdf_path = pdf_folder / f"{DEFAULT_TEST_PDF_STEM}.pdf"
        non_existing_template_path = pdf_folder / "non_existing_template.md"

        with pytest.raises(FileNotFoundError):
            paper2note(pdf_path, note_template_path=non_existing_template_path)

        assert not (pdf_path.parent / f"{pdf_path.stem}.md").exists()
        assert not non_existing_template_path.exists()
        assert pdf_path.exists()
        assert not (pdf_path.parent / f"{DEFAULT_TEST_PDF_STEM}.md").exists()

    def test_invalid_placeholders(self, pdf_folder: str):
        pdf_folder = Path(pdf_folder)
        pdf_path = pdf_folder / f"{DEFAULT_TEST_PDF_STEM}.pdf"

        invalid_template_path = pdf_folder / "invalid_template.md"
        with invalid_template_path.open("w") as f:
            f.write("the content of the note is {invalid_placeholder} {title}")

        paper2note(pdf_path, note_template_path=invalid_template_path)

        assert (pdf_path.parent / f"{pdf_path.stem}.md").exists()
        assert pdf_path.exists()
        assert (
            pdf_path.parent / f"{pdf_path.stem}.md"
        ).read_text() == "the content of the note is <'invalid_placeholder' IS AN INVALID PLACEHOLDER> Diffusion Policy: Visuomotor Policy Learning via Action Diffusion"


class TestDOIExtraction:
    @pytest.mark.parametrize(
        "pdf_stem, expected_title",
        [(pdf_stem, title) for pdf_stem, title in PDF_STEMS_TO_TITLE.items()],
    )
    def test_correct_title(
        self,
        pdf_stem: str,
        expected_title: str,
        pdf_folder: str,
    ):
        pdf_folder = Path(pdf_folder)
        pdf_path = pdf_folder / f"{pdf_stem}.pdf"

        result = pdf2bib(str(pdf_path))

        assert result["metadata"]["title"].lower() == expected_title.lower()

    # def test_print_metadata(self, pdf_folder:str):
    #     pdf_folder = Path(pdf_folder)
    #     pdf_path = pdf_folder / f"{DEFAULT_TEST_PDF_STEM}.pdf"

    #     result = pdf2bib(str(pdf_path))
    #     import json

    #     json.dump(result, open("result.json", "w"))

    #     print(result["metadata"])
    #     print(result)
    #     print(result["method"])
    #     print("----------------------------------------------------------------")
