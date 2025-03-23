# Web Search RAG

## Overview
This Streamlit-based web app allows users to input Wikipedia URLs, process the content, and generate answers to questions based on the processed content using AI models.

## Architecture

1. **User Input**:
   - Users provide Wikipedia URLs via the UI.

2. **Wikipedia Content Fetching**:
   - The `WikipediaContentFetcher` class fetches the content of Wikipedia pages and cleans up unnecessary references (like citation numbers).

3. **Text Preprocessing**:
   - The `TextPreprocessor` class processes the fetched text, removing unwanted line breaks and combining sentences to improve chunking.

4. **Document Splitting**:
   - The `DocumentSplitter` class splits the cleaned text into smaller chunks (documents) that are easier to manage for further processing.

5. **Embedding & Reranking**:
   - **Embedding**: Text chunks are processed into embeddings using models like Cohere for semantic understanding.
   - **Reranking**: The `CohereReranker` ranks the text chunks based on their relevance to the user's query using embeddings and semantic analysis. The model chooses the top-ranked documents to provide context for the answer.

6. **Answer Generation**:
   - The `GroqGenerator` class generates the answer based on the reranked documents. It sends a query to an AI model (hosted via the Groq API), which generates the response based solely on the relevant chunks.

## Flow Diagram:

```
User Input → WikipediaContentFetcher → Preprocessed Content
     ↑                               ↓
   Query → Embedding (Cohere) → Rerank Documents → GroqGenerator → Answer
```

### LLM Models, Embedding, and Reranking:
- **Cohere (Embedding & Reranking)**:
   - The Cohere API is used for two key tasks:
     1. **Embedding**: Converts text into vector representations (embeddings) that capture the semantic meaning of the content.
     2. **Reranking**: Given a user's query, the `CohereReranker` uses the embeddings to rank the documents based on relevance, selecting the top chunks to form context for answering the query.

- **Groq API (Answer Generation)**:
   - Once relevant chunks are selected, the `GroqGenerator` sends these to the Groq API, which uses an LLM model to generate an answer based on the context provided.

## Project Structure

```
├── app.py            # Streamlit UI
├── util.py           # Core logic (fetching, processing, generating answers)
└── requirements.txt  # Dependencies
└── config.ini        # stores api-keys, model_name
└── runtime.txt       # refers to the python version used for the deployment  
```

## Setup & Run

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the app:
   ```
   streamlit run app.py
   ```

---
