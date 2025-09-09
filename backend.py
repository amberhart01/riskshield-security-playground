# backend.py
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.text_splitter import TokenTextSplitter
from dotenv import load_dotenv
from fpdf_table.main import PDFTable
from azure.storage.blob import BlobServiceClient
import os
import re
import unicodedata
import pandas as pd
from fpdf_table.main import PDFTable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import tempfile
from cryptography.fernet import Fernet
from encryption_utils import decrypt_file

# Add this near the top of your file where other imports are
pdfmetrics.registerFont(TTFont('DejaVuSans', 'fonts/DejaVuSans.ttf'))

load_dotenv()
# print("OpenAI Key Loaded:", os.getenv("OPENAI_API_KEY"))

# Load environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")



# 1. Load the file
def load_file(file_path):
    ENCRYPTION_KEY = os.environ.get("ENCRYPTION_KEY")
    if not ENCRYPTION_KEY:
        raise ValueError("Missing ENCRYPTION_KEY")

    # Read and decrypt file
    with open(file_path, "rb") as f:
        encrypted_bytes = f.read()
    decrypted_bytes = decrypt_file(encrypted_bytes, ENCRYPTION_KEY.encode())

    # Determine file extension
    ext = os.path.splitext(file_path)[1].lower()

    # Write decrypted bytes to a temp file and load it
    with tempfile.NamedTemporaryFile(delete=True, suffix=ext) as tmp_file:
        tmp_file.write(decrypted_bytes)
        tmp_file.flush()  # Make sure content is written

        if ext == ".pdf":
            loader = PyPDFLoader(tmp_file.name)
        elif ext == ".docx":
            loader = Docx2txtLoader(tmp_file.name)
        elif ext == ".txt":
            loader = TextLoader(tmp_file.name)
        else:
            raise ValueError("Unsupported file type")

        return loader.load()

# 2. Chunk and clean
def chunk_docs(documents):
    # TokenTextSplitter uses tiktoken under the hood (much faster than pure‐Python)
    splitter = TokenTextSplitter(chunk_size=1000, chunk_overlap=150)
    return splitter.split_documents(documents)

# 3. Embed into Vector DB
def embed_docs(chunks, persist_directory="chroma_db"):
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    #vectordb.persist()
    return vectordb

# 4. Set up QA chain
def build_qa_chain(vectordb):
    llm = ChatOpenAI(
        temperature=0,
        model_name="gpt-4",
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    retriever = vectordb.as_retriever(search_kwargs={"k": 4})

# 1) Define the template
    template = """
        You are a cybersecurity assessor. Use the CONTEXT to answer the QUESTION below.
        After your explanation, add exactly one final line in this format:

            Rating: <Pass|Partial|Fail>

        CONTEXT:
        {context}

        QUESTION:
        {question}

        RESPONSE:
        """

    prompt = PromptTemplate(
            input_variables=["context", "question"],
            template=template
        )
    
    #retriever = vectordb.as_retriever(search_kwargs={"k": 4})
    
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt}
        #prompt=prompt
    )
    return qa


def assess_controls(qa_chain, control_df):
    results = []

    for row in control_df.itertuples():
        question = row.Question
        category = row.Category

        try:
            response = qa_chain.invoke({"query": question})  # <- fixed here
            answer = response["result"]

            rating_line = [line for line in answer.split("\n") if line.strip().lower().startswith("rating:")]
            rating = rating_line[0].strip() if rating_line else "Rating: Incomplete - No clear rating found."

            results.append({
                "Category": category,
                "Question": question,
                "AI Response": answer,
                "Rating": rating
            })

        except Exception as e:
            results.append({
                "Category": category,
                "Question": question,
                "AI Response": f"Error during processing: {str(e)}",
                "Rating": "Rating: Incomplete - Error occurred."
            })

    return results


def wrap_text(text, max_line_length=100):
    # Normalize and clean invisible characters
    text = unicodedata.normalize("NFKD", text)
    text = text.replace("\u00A0", " ")  # Replace non-breaking spaces
    text = re.sub(r"[^\x20-\x7E]", "", text)  # Remove non-printable characters

    # Now break up long words
    words = text.split()
    wrapped = []
    for word in words:
        if len(word) > max_line_length:
            word = ' '.join([word[i:i + max_line_length] for i in range(0, len(word), max_line_length)])
        wrapped.append(word)
    return ' '.join(wrapped)

def export_results_to_pdf(results, filename="AI_Control_Assessment_Results.pdf"):
    pdf = PDFTable()  # adds page, sets defaults
        
    # Register DejaVu Sans font with Unicode support
    font_path = "./fonts/DejaVuSans.ttf"
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Add the font with Unicode support enabled
    pdf.add_font("DejaVu", "", font_path, uni=True)
    pdf.add_font("DejaVu", "B", font_path, uni=True)
    
    # Set the font immediately after adding it
    pdf.set_font("DejaVu", size=12)
    
    
    for res in results:
        # ————— calculate column widths —————
        usable_w = pdf.w - pdf.l_margin - pdf.r_margin
        w_cat    = usable_w * 0.20   # 20%
        w_qst    = usable_w * 0.60   # 60%
        w_rate   = usable_w * 0.20   # 20%

# Access dictionary values with square bracket notation
        category = str(res['category']).strip()
        question = str(res['question']).strip()
        rating = str(res['rating']).strip()
        explanation = str(res['explanation']).strip()

        # ————— First row header + data —————
        pdf.table_header(
            ["Category", "Control Question", "Rating"],
            [w_cat, w_qst, w_rate],
            align=['L', 'L', 'C']
        )
        # Add row with the custom font
        pdf.table_row(
            [category, question, rating],
            [w_cat, w_qst, w_rate],
            align=['L', 'L', 'C']
        )
        
        # Add explanation with the custom font
        if explanation:
            pdf.multi_cell(0, 10, f"\nExplanation:\n{explanation}\n")
            pdf.ln(5)

        # ————— Second row header + data —————
        total = w_cat + w_qst + w_rate
        pdf.table_header(
            ["Response"],
            [total],
            align=['L']
        )
        pdf.table_row(
            [res["AI Response"]],
            [total],
            option="responsive",
            align=['L']
        )

        # small gap before next record
        pdf.ln(pdf.row_height_cell)

    pdf.output(filename)
    print(f"Results exported to {filename}")
    
    pdf.output("test_output.pdf")


def upload_to_azure(file_path, container_name="reports", blob_name=None):
    connection_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    if not connection_str:
        raise Exception("Azure Storage connection string is not set.")
    blob_service_client = BlobServiceClient.from_connection_string(connection_str)
    container_client = blob_service_client.get_container_client(container_name)
    
    # Create the container if it doesn't exist
    try:
        container_client.create_container()
    except Exception:
        pass  # Container likely already exists

    # Use file name if blob_name not provided
    if blob_name is None:
        blob_name = os.path.basename(file_path)
    
    with open(file_path, "rb") as data:
        container_client.upload_blob(name=blob_name, data=data, overwrite=True)
    
    # Generate a public URL (if container is public or using SAS tokens)
    blob_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{container_name}/{blob_name}"
    return blob_url



if __name__ == "__main__":
    #Process your document to  build the QA chain:
    nist_file = "Test Files/SANS_Acceptable_Encryption_Standard_April2025.pdf"
    company_file="Test Files/sample_company_policy.txt"
    
    #Load the NIST Document
    print(f"Loading NIST file: {nist_file}")
    nist_docs = load_file(nist_file)
    print(f"Loaded {len(nist_docs)} document(s) from NIST file")

    # Load Company Policy Document
    print(f"Loading Company Policy file: {company_file}")
    company_docs = load_file(company_file)
    print(f"Loaded {len(company_docs)} document(s) from Company Policy")

    #Combine documents from both sources
    docs = nist_docs + company_docs
    print(f"total loaded documents: {len(docs)} document(s)")
   
    chunks = chunk_docs (docs)
    print(f"Split into {len(chunks)} chunks")

    vectordb = embed_docs(chunks)
    print("Embedded into vector store")

    qa = build_qa_chain(vectordb)

    # Load control questions
  
    control_df = pd.read_excel("Template.xlsx", skiprows=3)
    control_df = control_df[["CATEGORY", "QUESTIONS"]].rename(
        columns={"CATEGORY": "Category", "QUESTIONS": "Question"}
    ).dropna(subset=["Question"])

    control_df = control_df.ffill()

    # Run control assessment
    results = assess_controls(qa, control_df)

    print("n\✅ AI Control Assessment REsults:")
    for r in results:
        print(f"\nCategory: {r['Category']}")
        print(f"\nQuestion: {r['Question']}")
        print(f"\nResponse: {r['AI Response']}")
        print(f"Rating: {r['Rating']}")
    
    # Export the results to a PDF file
    export_results_to_pdf(results)

    report_filename = "AI_Control_Assessment_Results.pdf"
    export_results_to_pdf(results, filename=report_filename)
    blob_url = upload_to_azure(report_filename)
    print(f"Report uploaded to Azure! Download at: {blob_url}")

   