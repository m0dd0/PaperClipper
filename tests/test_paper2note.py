import pytest
import shutil
from tempfile import TemporaryDirectory
from pathlib import Path

from pdf2bib import pdf2bib

from paper2note.paper2note import paper2note

SAMPLE_PAPERS_PATH = Path(__file__).parent / "sample_papers"
PDF_FILES = [p.stem for p in SAMPLE_PAPERS_PATH.glob("*.pdf")]


@pytest.fixture
def pdf_folder():
    with TemporaryDirectory() as temp_dir:
        for path in SAMPLE_PAPERS_PATH.glob("*.pdf"):
            shutil.copy(path, temp_dir)

        yield temp_dir


class TestPaper2Note:
    @pytest.mark.parametrize("pdf_stem", PDF_FILES)
    def test_default(self, pdf_stem, pdf_folder):
        pdf_folder = Path(pdf_folder)
        pdf_path = pdf_folder / f"{pdf_stem}.pdf"

        paper2note(pdf_path)

        assert (pdf_path.parent / f"{pdf_path.stem}.md").exists()
        assert pdf_path.exists()
        # print(list(pdf_folder.glob("*")))

    def test_note_exists_already(self, pdf_folder):
        pdf_folder = Path(pdf_folder)

        pdf_path = next(pdf_folder.glob("*.pdf"))
        existing_note_path = pdf_folder / f"{pdf_path.stem}.md"
        with existing_note_path.open("w") as f:
            f.write("existing note")

        paper2note(pdf_path)

        assert existing_note_path.exists()
        assert existing_note_path.read_text() == "existing note"

    def test_renamed_pdf_exists_already(self, pdf_folder):
        pdf_folder = Path(pdf_folder)

        pdf_path = next(pdf_folder.glob("*.pdf"))
        renamed_pdf_path = pdf_folder / "renamed.pdf"
        with renamed_pdf_path.open("w") as f:
            f.write("existing renamed pdf")

        # Call the paper2note function
        paper2note(pdf_path, pdf_rename_pattern="renamed")

        assert renamed_pdf_path.exists()
        assert renamed_pdf_path.read_text() == "existing renamed pdf"
        assert pdf_path.exists()
        assert (pdf_folder / "renamed.md").exists()

    # def test_pdf_rename_pattern(self, pdf_folder):
    #     pdf_folder = Path(pdf_folder)
    #     pdf_path = pdf_folder / "liu23d.pdf"

    #     paper2note(pdf_path, pdf_rename_pattern="{title} ({year}) {author}")

    #     # Assert that the PDF file was renamed
    #     assert not pdf_path.exists()
    #     print(list(pdf_folder.glob("*")))
    #     assert False
    # assert (pdf_folder / "pdf (2020) author.pdf").exists(

    # def test_note_target_folder(self, pdf_folder):
    #     pdf_folder = Path(pdf_folder)
    #     pdf_path = pdf_folder / "pdf.pdf"
    #     note_target_folder = pdf_folder / "notes"

    #     # Call the paper2note function with a note target folder
    #     paper2note(pdf_path, note_target_folder=note_target_folder)

    #     # Assert that the note file was created in the target folder
    #     assert (note_target_folder / "pdf.md").exists()

    # def test_no_doi_found(pdf_folder):
    #     pdf_folder = Path(pdf_folder)
    #     pdf_path = pdf_folder / "pdf.pdf"

    #     # Call the paper2note function with a PDF that has no DOI
    #     paper2note(pdf_path)

    #     # Assert that no note file was created
    #     assert not (pdf_path.parent / "pdf.md").exists()

    # def test_pdf_is_not_a_pdf(pdf_folder):
    #     pdf_folder = Path(pdf_folder)
    #     non_pdf_path = pdf_folder / "non_pdf.txt"

    #     # Call the paper2note function with a non-PDF file
    #     paper2note(non_pdf_path)

    #     # Assert that no note file was created
    #     assert not (non_pdf_path.parent / "non_pdf.md").exists()

    # def test_pdf_does_not_exist(pdf_folder):
    #     pdf_folder = Path(pdf_folder)
    #     non_existing_pdf_path = pdf_folder / "non_existing_pdf.pdf"

    #     # Call the paper2note function with a non-existing PDF file
    #     paper2note(non_existing_pdf_path)

    #     # Assert that no note file was created
    #     assert not (non_existing_pdf_path.parent / "non_existing_pdf.md").exists()

    # def test_note_template_path(pdf_folder):
    #     pdf_folder = Path(pdf_folder)
    #     pdf_path = pdf_folder / "pdf.pdf"
    #     note_template_path = pdf_folder / "template.md"

    #     # Call the paper2note function with a note template path
    #     paper2note(pdf_path, note_template_path=note_template_path)

    #     # Assert that the note file was created using the template
    #     assert (pdf_path.parent / "pdf.md").exists()

    # def test_note_template_does_not_exist(pdf_folder):
    #     pdf_folder = Path(pdf_folder)
    #     pdf_path = pdf_folder / "pdf.pdf"
    #     non_existing_template_path = pdf_folder / "non_existing_template.md"

    #     # Call the paper2note function with a non-existing note template path
    #     paper2note(pdf_path, note_template_path=non_existing_template_path)

    #     # Assert that the note file was created without using a template
    #     assert (pdf_path.parent / "pdf.md").exists()


class TestDOIExtraction:
    @pytest.mark.parametrize(
        "pdf_stem, expected_title",
        [
            (
                "2303.04137",
                "Diffusion Policy: Visuomotor Policy Learning via Action Diffusion",
            ),
            (
                "NeurIPS-2023-cross-episodic-curriculum-for-transformer-agents-Paper-Conference",
                "Cross-Episodic Curriculum for Transformer Agents",
            ),
            (
                "NeurIPS-2023-modelling-cellular-perturbations-with-the-sparse-additive-mechanism-shift-variational-autoencoder-Paper-Conference",
                "Modelling Cellular Perturbations with the Sparse Additive Mechanism Shift Variational Autoencoder",
            ),
            ("NIPS-2017-attention-is-all-you-need-Paper", "Attention Is All You Need"),
            ("nova23a", "Gradient-Free Structured Pruning with Unlabeled Data"),
            (
                "wang23ao",
                "Learning to Bid in Repeated First-Price Auctions with Budgets",
            ),
        ],
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

        # print(result["metadata"]["title"].lower())
        # print(expected_title.lower())
        # print(result["method"])
        assert result["metadata"]["title"].lower() == expected_title.lower()
