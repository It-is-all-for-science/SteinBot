import os
from docx import Document
import fitz  # pymupdf
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings  # ИСПРАВЛЕН ИМПОРТ
from langchain_chroma import Chroma

def extract_text(path):
    ext = path.lower().split('.')[-1]
    if ext == 'txt':
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    if ext == 'docx':
        doc = Document(path)
        return '\n'.join([p.text for p in doc.paragraphs])
    if ext == 'pdf':
        doc = fitz.open(path)
        return '\n'.join(page.get_text() for page in doc)
    raise ValueError("Неподдерживаемый формат")

def ingest_all(docs_dir="docs", db_dir="data/chroma_db"):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    emb = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = Chroma(collection_name="steinbot_kb", embedding_function=emb, persist_directory=db_dir)
    for fn in os.listdir(docs_dir):
        path = os.path.join(docs_dir, fn)
        text = extract_text(path)
        chunks = splitter.split_text(text)
        db.add_texts(chunks)
    print("Ингест завершён")

def search_context(query, db_dir="data/chroma_db"):
    print("[DEBUG] search_context: start", flush=True)
    try:
        emb = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        db = Chroma(collection_name="steinbot_kb", embedding_function=emb, persist_directory=db_dir)
        docs = db.similarity_search(query, k=4)
        print("[DEBUG] search_context: got docs", flush=True)
        return "\n\n".join([d.page_content for d in docs]) if docs else ""
    except Exception as e:
        print(f"[ERROR] search_context: {e}", flush=True)
        raise