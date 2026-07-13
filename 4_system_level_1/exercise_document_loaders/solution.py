from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


@dataclass(frozen=True)
class Document:
    title: str
    author: str
    content: str


class DocumentLoader(Protocol):
    def load_document(self) -> Document: ...

    def document_type(self) -> str: ...


class FileDocumentLoader(ABC):
    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path

    def load_document(self) -> Document:
        print(f"Loading {self.document_type()} from {self.file_path}")

        raw_data = self.read_file()

        return self.parse_document(raw_data)

    def read_file(self) -> bytes:
        return self.file_path.read_bytes()

    @abstractmethod
    def parse_document(self, raw_data: bytes) -> Document: ...

    @abstractmethod
    def document_type(self) -> str: ...


class PdfDocumentLoader(FileDocumentLoader):
    def parse_document(self, raw_data: bytes) -> Document:
        return Document(
            title="Python Design",
            author="Alice",
            content="Content extracted from a PDF document.",
        )

    def document_type(self) -> str:
        return "PDF"


class WordDocumentLoader(FileDocumentLoader):
    def parse_document(self, raw_data: bytes) -> Document:
        return Document(
            title="Meeting Notes",
            author="Bob",
            content="Content extracted from a Word document.",
        )

    def document_type(self) -> str:
        return "Word document"


class GoogleDocsClient:
    def download_document(self, document_id: str) -> dict[str, str]:
        return {
            "title": "Project Proposal",
            "author": "Carol",
            "body": "Content downloaded from Google Docs.",
        }


class GoogleDocsLoader:
    def __init__(
        self,
        document_id: str,
        client: GoogleDocsClient,
    ) -> None:
        self.document_id = document_id
        self.client = client

    def load_document(self) -> Document:
        print(f"Downloading Google Doc {self.document_id}")

        raw_data = self.client.download_document(self.document_id)

        return Document(
            title=raw_data["title"],
            author=raw_data["author"],
            content=raw_data["body"],
        )

    def document_type(self) -> str:
        return "Google Docs"


def summarize_document(loader: DocumentLoader) -> None:
    document = loader.load_document()

    print(f"\nSummary of '{document.title}'")
    print(f"Author: {document.author}")
    print(document.content[:40] + "...")
    print()


def main() -> None:
    loaders: list[DocumentLoader] = [
        PdfDocumentLoader(Path("design.pdf")),
        WordDocumentLoader(Path("meeting-notes.docx")),
        GoogleDocsLoader(
            document_id="doc-123",
            client=GoogleDocsClient(),
        ),
    ]

    for loader in loaders:
        summarize_document(loader)


if __name__ == "__main__":
    main()
