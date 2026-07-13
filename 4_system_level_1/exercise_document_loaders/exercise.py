from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Document:
    title: str
    author: str
    content: str


class PdfDocumentLoader:
    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path

    def load_document(self) -> Document:
        print(f"Loading PDF from {self.file_path}")

        raw_data = self._read_file()

        return self._parse_document(raw_data)

    def document_type(self) -> str:
        return "pdf"

    def _read_file(self) -> bytes:
        # Pretend we're reading a PDF.
        return b"%PDF..."

    def _parse_document(self, raw_data: bytes) -> Document:
        return Document(
            title="Python Design",
            author="Alice",
            content="Content extracted from a PDF...",
        )


class WordDocumentLoader:
    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path

    def load_document(self) -> Document:
        print(f"Loading Word document from {self.file_path}")

        raw_data = self._read_file()

        return self._parse_document(raw_data)

    def document_type(self) -> str:
        return "word"

    def _read_file(self) -> bytes:
        # Pretend we're reading a DOCX.
        return b"PK..."

    def _parse_document(self, raw_data: bytes) -> Document:
        return Document(
            title="Meeting Notes",
            author="Bob",
            content="Content extracted from a Word document...",
        )


class GoogleDocsLoader:
    def __init__(self, document_id: str) -> None:
        self.document_id = document_id

    def load_document(self) -> Document:
        print(f"Downloading Google Doc {self.document_id}")

        raw_data = self._download_document()

        return self._parse_document(raw_data)

    def document_type(self) -> str:
        return "google_docs"

    def _download_document(self) -> dict[str, str]:
        # Pretend we're calling the Google Docs API.
        return {
            "title": "Project Proposal",
            "author": "Carol",
            "body": "Content downloaded from Google Docs...",
        }

    def _parse_document(self, raw_data: dict[str, str]) -> Document:
        return Document(
            title=raw_data["title"],
            author=raw_data["author"],
            content=raw_data["body"],
        )


def summarize_document(loader: PdfDocumentLoader) -> None:
    document = loader.load_document()

    print(f"Summary of '{document.title}'")
    print(document.content[:40] + "...")


def main() -> None:
    loader = PdfDocumentLoader(Path("design.pdf"))

    summarize_document(loader)


if __name__ == "__main__":
    main()
