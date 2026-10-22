"""Document ingestion pipeline.

Reads files from InputDocs/ → parses (docling for PDF, plain read for
txt/md) → chunks (~512 tokens, 50 overlap) → embeds via Ollama
nomic-embed-text → stores in ChromaDB Knowledge Base with metadata.

Can be run standalone:
    python -m bd.knowledge.ingest [--dir DIR] [--reset]
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import ollama

from agent.commun.config import settings
from bd.knowledge.kb import KnowledgeBase

logger = logging.getLogger(__name__)

def _w(*words: str) -> str:
    """Motif qui ne reconnait que des MOTS ENTIERS dans un nom de fichier.

    Correctif du code de reference : ``\\b`` ne separe pas les mots relies par
    un tiret bas (``UK_National`` n'etait pas reconnu comme Royaume-Uni) et les
    motifs sans frontiere matchaient a l'interieur des mots (``Opportunities``
    contient ``niti`` et etait classe... Inde).
    """
    return r"(?i)(?<![a-z])(?:" + "|".join(words) + r")(?![a-z])"


# Source type inference from filename patterns
_SOURCE_TYPE_PATTERNS: list[tuple[str, str]] = [
    # Textes juridiques contraignants (lois, codes, decrets) : ajoute pour le
    # domaine de la protection des mineurs en ligne.
    (_w("loi", "law", "act", "code", "decret", "decree", "ordonnance", "regulation",
        "reglement", "rule", "directive"), "legislation"),
    (_w("ITU", "AI4G", "sandbox") + r"|Y\.3172", "standards_document"),
    (_w("UNESCO", "OECD", "Oxford", "UNCTAD", "CCIA", "Turing", "UNICEF", "UN"), "international_org_report"),
    (r"(?i)national.*(strategy|plan)|(?<![a-z])(?:NAIS|SDAIA|EBIA|PBIA)(?![a-z])", "national_strategy"),
    (_w("policy", "governance", "guidelines", "guide"), "policy_document"),
    (r"(?i)sample_national", "national_strategy"),
    (r"(?i)AI_Ready_Framework", "international_org_report"),
]

# Country inference from filename (mots entiers uniquement, voir _w)
_COUNTRY_PATTERNS: list[tuple[str, str]] = [
    (_w("cameroun", "cameroon", "cmr"), "Cameroon"),
    (_w("ethiopia"), "Ethiopia"),
    (_w("saudi", "SDAIA", "NSDAI"), "Saudi Arabia"),
    (_w("egypt"), "Egypt"),
    (_w("kenya"), "Kenya"),
    (_w("zambia"), "Zambia"),
    (_w("rwanda"), "Rwanda"),
    (_w("nigeria", "NITDA"), "Nigeria"),
    (_w("brazil", "PBIA", "EBIA"), "Brazil"),
    (_w("india", "NITI"), "India"),
    (_w("singapore", "NAIS"), "Singapore"),
    (_w("japan"), "Japan"),
    (_w("china"), "China"),
    (_w("korea"), "South Korea"),
    (_w("peru"), "Peru"),
    (_w("estonia"), "Estonia"),
    (_w("spain"), "Spain"),
    (_w("turkiye", "turkey"), "Turkiye"),
    (_w("france"), "France"),
    (_w("australia", "esafety"), "Australia"),
    (_w("UAE", "emirates"), "United Arab Emirates"),
    (_w("US", "USA", "united.states", "americas?", "COPPA"), "United States"),
    (_w("UK", "united.kingdom", "britain", "british"), "United Kingdom"),
    (_w("EU", "european.union", "GDPR", "RGPD", "DSA"), "European Union"),
    (_w("african.union", "AU"), "African Union"),
]


# ------------------------------------------------------------------
# Parsing
# ------------------------------------------------------------------

def parse_file(filepath: Path) -> str:
    """Parse a file into plain text.

    Uses docling for PDFs (with fallback to PyMuPDF), plain read for
    text files.
    """
    suffix = filepath.suffix.lower()

    if suffix == ".pdf":
        return _parse_pdf(filepath)
    elif suffix in (".txt", ".md", ".csv"):
        return filepath.read_text(encoding="utf-8", errors="replace")
    elif suffix == ".html":
        return _strip_html(filepath.read_text(encoding="utf-8", errors="replace"))
    else:
        logger.warning("Unknown file type '%s' for %s — reading as text", suffix, filepath.name)
        return filepath.read_text(encoding="utf-8", errors="replace")


def _parse_pdf(filepath: Path) -> str:
    """Parse PDF, trying docling first, then PyMuPDF fallback."""
    # Try docling
    try:
        from docling.document_converter import DocumentConverter
        converter = DocumentConverter()
        result = converter.convert(str(filepath))
        text = result.document.export_to_markdown()
        if text and len(text.strip()) > 100:
            logger.info("Parsed %s with docling (%d chars)", filepath.name, len(text))
            return text
    except ImportError:
        logger.debug("docling not installed, trying PyMuPDF")
    except Exception as e:
        logger.warning("docling failed for %s: %s — trying PyMuPDF", filepath.name, e)

    # Fallback: PyMuPDF
    try:
        import fitz
        doc = fitz.open(str(filepath))
        pages = []
        for page in doc:
            pages.append(page.get_text())
        text = "\n\n".join(pages)
        logger.info("Parsed %s with PyMuPDF (%d chars, %d pages)", filepath.name, len(text), len(pages))
        return text
    except ImportError:
        logger.error("Neither docling nor PyMuPDF installed — cannot parse PDF %s", filepath.name)
        return ""
    except Exception as e:
        logger.error("PyMuPDF failed for %s: %s", filepath.name, e)
        return ""


def _strip_html(html: str) -> str:
    """Crude HTML tag stripping."""
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# ------------------------------------------------------------------
# Chunking
# ------------------------------------------------------------------

def chunk_text(
    text: str,
    chunk_size: int = settings.chunk_size,
    overlap: int = settings.chunk_overlap,
    max_chars: int = 2000,
) -> list[str]:
    """Split text into overlapping chunks by word count.

    Uses paragraph boundaries when possible, falling back to word-level
    splitting.  Each chunk is also hard-capped at *max_chars* characters
    to stay within embedding model context limits (nomic-embed-text has
    an 8192 token context; 6000 chars ≈ ~1500 tokens, well within limit).
    """
    if not text or not text.strip():
        return []

    # Split into paragraphs first
    paragraphs = re.split(r"\n\s*\n", text)
    paragraphs = [p.strip() for p in paragraphs if p.strip()]

    chunks: list[str] = []
    current_words: list[str] = []

    for para in paragraphs:
        words = para.split()
        for word in words:
            current_words.append(word)
            if len(current_words) >= chunk_size:
                chunks.append(" ".join(current_words))
                # Keep overlap words for next chunk
                current_words = current_words[-overlap:] if overlap > 0 else []

    # Don't forget the last chunk
    if current_words:
        last_chunk = " ".join(current_words)
        # Only add if it has meaningful content (> 20 words)
        if len(current_words) > 20 or not chunks:
            chunks.append(last_chunk)
        elif chunks:
            # Append short trailing text to last chunk
            chunks[-1] = chunks[-1] + " " + last_chunk

    # Hard-cap: split any chunk that exceeds max_chars
    safe_chunks: list[str] = []
    for chunk in chunks:
        if len(chunk) <= max_chars:
            safe_chunks.append(chunk)
        else:
            # Split oversized chunk into max_chars pieces by character
            for i in range(0, len(chunk), max_chars):
                piece = chunk[i : i + max_chars].strip()
                if piece:
                    safe_chunks.append(piece)

    return safe_chunks


# Debut d'article dans les textes juridiques camerounais :
# « ARTICLE 42.- », « Article 1er.- », « Article 5. - », « Article 7 ».
_ARTICLE_RX = re.compile(r"(?m)^[ \t]*(?:ARTICLE|Article)[ \t]+(\d+|premier|PREMIER)(?:er)?[ \t]*\.?[ \t]*[-–­]?")


def _article_number(raw: str) -> int:
    """« premier » (textes europeens) vaut 1."""
    return 1 if raw.lower() == "premier" else int(raw)
_PAGE_RX = re.compile(r"\[PAGE (\d+)[^\]]*\]")


def chunk_legal_text(text: str, max_chars: int = 2000) -> list[dict[str, str]]:
    """Decoupe un texte juridique ARTICLE PAR ARTICLE.

    Ajout au code de reference : le decoupage par nombre de mots melangeait
    plusieurs articles dans un meme morceau, ce qui degradait la recherche
    (un article court etait noye parmi ses voisins) et empechait les agents de
    citer un article precis.

    - La premiere ligne du fichier (titre officiel du texte) est repetee en
      tete de chaque morceau, pour que l'extrait reste identifiable seul.
    - Le preambule (visas, avant l'article 1) forme un morceau distinct.
    - Un article plus long que ``max_chars`` est scinde en parties, chacune
      gardant le titre et le numero d'article.
    - Les marqueurs ``[PAGE n]`` (voir scripts/split_recueil.py) servent a
      retrouver la page ou commence chaque article.

    Retourne une liste de dicts : text, article, page.
    """
    title = text.strip().splitlines()[0].strip() if text.strip() else ""

    def page_at(pos: int) -> str:
        pages = _PAGE_RX.findall(text[:pos])
        return pages[-1] if pages else ""

    def clean(s: str) -> str:
        s = _PAGE_RX.sub(" ", s)
        s = re.sub(r"(?m)^\s*\d{1,3}\s*$", "", s)          # numeros de page isoles
        return re.sub(r"[ \t]+", " ", re.sub(r"\n{2,}", "\n", s)).strip()

    # On ne garde que les debuts d'article qui se SUIVENT (1, 2, 3...) : dans
    # un texte organise en « sections » (ex. lois britanniques), les lignes
    # commencant par « Article » sont des renvois a d'autres textes (« Article 8
    # de la Convention... ») et ne doivent pas servir de points de coupe.
    starts = []
    last = 0
    for m in _ARTICLE_RX.finditer(text):
        num = _article_number(m.group(1))
        if num == last + 1 or (last and num in (last, last + 2)):
            starts.append(m)
            last = num
    if len(starts) < 5:
        starts = []   # pas de vraie structure en articles : blocs de taille fixe
    pieces: list[tuple[str, str, int]] = []                 # (article, contenu, position)
    if not starts:
        pieces.append(("", text, 0))
    else:
        preamble = text[: starts[0].start()]
        if len(clean(preamble)) > 100:
            pieces.append(("preambule", preamble, 0))
        for k, m in enumerate(starts):
            end = starts[k + 1].start() if k + 1 < len(starts) else len(text)
            pieces.append((str(_article_number(m.group(1))), text[m.start():end], m.start()))

    chunks: list[dict[str, str]] = []
    for article, body, pos in pieces:
        body = clean(body)
        if not body:
            continue
        label = f"Article {article}" if article.isdigit() else article
        head = f"[{title}]" + (f" — {label}" if label else "")
        room = max(200, max_chars - len(head) - 1)
        parts = [body[i:i + room] for i in range(0, len(body), room)] or [body]
        for j, part in enumerate(parts):
            suffix = f" (partie {j + 1}/{len(parts)})" if len(parts) > 1 else ""
            chunks.append({"text": f"{head}{suffix}\n{part}", "article": article, "page": page_at(pos)})
    return chunks


# ------------------------------------------------------------------
# Embedding
# ------------------------------------------------------------------

def embed_texts(
    texts: list[str],
    model: str = settings.embed_model,
    base_url: str = settings.ollama_base_url,
) -> list[list[float]]:
    """Embed a list of texts using Ollama.

    Truncates any text over 7500 chars (~1800 tokens) to stay within
    nomic-embed-text's 8192 token context.  Falls back to one-at-a-time
    embedding if a batch call fails.
    """
    client = ollama.Client(host=base_url)
    max_text_chars = 2000  # conservative limit for nomic-embed-text (8192 token ctx)

    # Pre-truncate long texts
    safe_texts = [t[:max_text_chars] if len(t) > max_text_chars else t for t in texts]

    embeddings: list[list[float]] = []
    batch_size = 16

    for i in range(0, len(safe_texts), batch_size):
        batch = safe_texts[i : i + batch_size]
        try:
            response = client.embed(model=model, input=batch)
            embeddings.extend(response["embeddings"])
        except Exception:
            # Fallback: embed one at a time
            logger.warning("Batch embed failed at offset %d, falling back to one-at-a-time", i)
            for j, text in enumerate(batch):
                try:
                    resp = client.embed(model=model, input=[text])
                    embeddings.extend(resp["embeddings"])
                except Exception as e2:
                    # Last resort: truncate aggressively
                    logger.warning("Single embed failed for chunk %d (len=%d), truncating to 4000 chars", i + j, len(text))
                    resp = client.embed(model=model, input=[text[:4000]])
                    embeddings.extend(resp["embeddings"])

    return embeddings


# ------------------------------------------------------------------
# Metadata inference
# ------------------------------------------------------------------

def infer_source_type(filename: str) -> str:
    """Infer source type from filename patterns."""
    for pattern, source_type in _SOURCE_TYPE_PATTERNS:
        if re.search(pattern, filename):
            return source_type
    return "international_org_report"


def infer_country(filename: str) -> str:
    """Infer country from filename patterns. Returns 'global' if unknown."""
    for pattern, country in _COUNTRY_PATTERNS:
        if re.search(pattern, filename):
            return country
    return "global"


def build_metadata(
    filepath: Path,
    chunk_index: int,
    total_chunks: int,
    extra: Optional[dict[str, Any]] = None,
) -> dict[str, str]:
    """Build metadata dict for a document chunk."""
    meta: dict[str, str] = {
        "source_file": filepath.name,
        "source_type": infer_source_type(filepath.name),
        "country": infer_country(filepath.name),
        "chunk_index": str(chunk_index),
        "total_chunks": str(total_chunks),
        "ingested_at": datetime.utcnow().isoformat(),
    }
    if extra:
        for k, v in extra.items():
            meta[k] = str(v)
    return meta


# ------------------------------------------------------------------
# Main ingestion
# ------------------------------------------------------------------

def ingest_file(
    filepath: Path,
    kb: KnowledgeBase,
    collection_name: Optional[str] = None,
    extra_metadata: Optional[dict[str, Any]] = None,
) -> int:
    """Ingest a single file into the Knowledge Base.

    Returns the number of chunks stored.
    """
    logger.info("Ingesting %s ...", filepath.name)

    # Parse
    text = parse_file(filepath)
    if not text.strip():
        logger.warning("No text extracted from %s — skipping", filepath.name)
        return 0

    # Chunk : les textes juridiques sont decoupes article par article (un
    # morceau = un article, citable tel quel) ; les autres documents gardent
    # le decoupage par nombre de mots du code de reference.
    per_chunk_meta: list[dict[str, Any]] = []
    if infer_source_type(filepath.name) == "legislation":
        legal = chunk_legal_text(text)
        chunks = [c["text"] for c in legal]
        per_chunk_meta = [{"article": c["article"], "page": c["page"]} for c in legal]
    else:
        chunks = chunk_text(text)
    if not chunks:
        logger.warning("No chunks produced from %s — skipping", filepath.name)
        return 0

    logger.info("  %d chunks from %s", len(chunks), filepath.name)

    # Embed
    embeddings = embed_texts(chunks)

    # Build metadata per chunk
    metadatas = []
    for i in range(len(chunks)):
        extra = dict(extra_metadata or {})
        if per_chunk_meta:
            extra.update(per_chunk_meta[i])
        metadatas.append(build_metadata(filepath, i, len(chunks), extra))

    # Store
    kb.add_documents(
        texts=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
        collection_name=collection_name,
    )

    logger.info("  Stored %d chunks from %s", len(chunks), filepath.name)
    return len(chunks)


def ingest_directory(
    directory: Path,
    kb: KnowledgeBase,
    collection_name: Optional[str] = None,
    skip_manifest: bool = True,
) -> dict[str, int]:
    """Ingest all supported files from a directory (recursively).

    Subdirectories are used as document categories. For example files
    under ``InputDocs/AI_Strategies/`` get ``document_category: AI_Strategies``
    in their metadata, while ``InputDocs/AI_Use_Cases/`` get
    ``document_category: AI_Use_Cases``.

    Returns {relative_path: chunk_count} mapping.
    """
    supported = {".pdf", ".txt", ".md", ".csv", ".html"}
    results: dict[str, int] = {}

    # Collect files: top-level + all subdirectories
    all_files: list[tuple[Path, str]] = []  # (filepath, category)
    for item in sorted(directory.iterdir()):
        if item.is_dir():
            category = item.name  # e.g. "AI_Strategies", "AI_Use_Cases"
            for sub_file in sorted(item.iterdir()):
                if sub_file.is_file():
                    all_files.append((sub_file, category))
        elif item.is_file():
            all_files.append((item, "general"))

    for filepath, category in all_files:
        if filepath.suffix.lower() not in supported:
            continue
        if skip_manifest and filepath.name.lower() == "inputs.md":
            continue

        # Build a display key like "AI_Strategies/India_National_AI_Strategy_NITI.pdf"
        display_key = f"{category}/{filepath.name}" if category != "general" else filepath.name
        extra_meta = {"document_category": category}

        try:
            count = ingest_file(filepath, kb, collection_name, extra_metadata=extra_meta)
            results[display_key] = count
        except Exception as e:
            logger.error("Failed to ingest %s: %s", display_key, e)
            results[display_key] = 0

    return results


def ingest_framework_definitions(kb: KnowledgeBase) -> int:
    """Load dimensions.json into the kb_framework collection.

    Each dimension becomes one document with its full description
    and metric list embedded for retrieval.
    """
    dims_path = settings.framework_dir / "dimensions.json"
    if not dims_path.exists():
        logger.error("dimensions.json not found at %s", dims_path)
        return 0

    with open(dims_path) as f:
        data = json.load(f)

    texts: list[str] = []
    metadatas: list[dict[str, str]] = []

    # Add each dimension as a document
    for dim in data["dimensions"]:
        metrics_text = "\n".join(
            f"- {m['name']}: {m['description']}" for m in dim["metrics"]
        )
        doc_text = (
            f"Dimension {dim['id']}: {dim['name']}\n\n"
            f"{dim['description']}\n\n"
            f"Mapped Factors: {', '.join(dim['mapped_factors'])}\n\n"
            f"Metrics:\n{metrics_text}"
        )
        texts.append(doc_text)
        metadatas.append({
            "dimension_id": str(dim["id"]),
            "dimension_name": dim["name"],
            "short_name": dim["short_name"],
            "source_type": "framework_definition",
            "entity_type": "dimension",
            "factors": ",".join(dim["mapped_factors"]),
        })

    # Add each factor as a document
    for factor in data["factors"]:
        texts.append(
            f"Factor: {factor['name']}\n\n{factor['description']}"
        )
        metadatas.append({
            "factor_id": factor["id"],
            "factor_name": factor["name"],
            "source_type": "framework_definition",
            "entity_type": "factor",
        })

    embeddings = embed_texts(texts)

    kb.add_documents(
        texts=texts,
        embeddings=embeddings,
        metadatas=metadatas,
        collection_name=settings.kb_framework_collection,
    )

    logger.info("Loaded %d framework definitions into kb_framework", len(texts))
    return len(texts)


# ------------------------------------------------------------------
# CLI entry point
# ------------------------------------------------------------------

def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
    )

    parser = argparse.ArgumentParser(
        description="Ingest documents into the AI Readiness Knowledge Base"
    )
    parser.add_argument(
        "--dir",
        type=Path,
        default=settings.input_docs_dir,
        help="Directory containing documents to ingest",
    )
    parser.add_argument(
        "--file",
        type=Path,
        default=None,
        help="Ingest a single file",
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Reset the Knowledge Base before ingesting",
    )
    parser.add_argument(
        "--framework-only",
        action="store_true",
        help="Only load framework definitions (dimensions.json)",
    )
    args = parser.parse_args()

    # Ensure directories exist
    settings.chromadb_dir.mkdir(parents=True, exist_ok=True)

    kb = KnowledgeBase()

    if args.reset:
        logger.warning("Resetting Knowledge Base...")
        kb.reset()

    # Always load framework definitions
    logger.info("Loading framework definitions...")
    fw_count = ingest_framework_definitions(kb)
    print(f"Framework definitions: {fw_count} documents loaded")

    if args.framework_only:
        print("\nDone (framework only).")
        print(f"KB stats: {kb.stats()}")
        return

    if args.file:
        count = ingest_file(args.file, kb)
        print(f"\n{args.file.name}: {count} chunks ingested")
    else:
        doc_dir = args.dir
        if not doc_dir.exists():
            print(f"ERROR: Directory not found: {doc_dir}")
            sys.exit(1)

        print(f"\nIngesting all documents from: {doc_dir}")
        results = ingest_directory(doc_dir, kb)

        print("\n--- Ingestion Results ---")
        total = 0
        for filename, count in sorted(results.items()):
            status = f"{count} chunks" if count > 0 else "SKIPPED"
            print(f"  {filename:50s} {status}")
            total += count
        print(f"\nTotal: {total} chunks from {len(results)} files")

    print(f"\nKB stats: {kb.stats()}")


if __name__ == "__main__":
    main()
