
# Web Search RAG

## Overview
This Streamlit-based web app allows users to input Wikipedia URLs, process the content, and generate answers to questions based on the processed content using AI models.

## Architecture

1. **User Input**:
   - Users provide Wikipedia URLs.

2. **Wikipedia Content Fetching**:
   - The `WikipediaContentFetcher` class fetches and cleans the text from the provided URLs.

3. **Text Preprocessing**:
   - The text is cleaned and split into smaller chunks for easier processing.

4. **Document Splitting**:
   - The text is divided into smaller, manageable chunks.

5. **Reranking**:
   - The `CohereReranker` ranks the chunks based on relevance to the user's query.

6. **Answer Generation**:
   - The `GroqGenerator` generates answers based on the ranked text chunks.

## Flow Diagram:

```
User Input → WikipediaContentFetcher → Preprocessed Content
     ↑                               ↓
    Query → CohereReranker → Reranked Chunks → GroqGenerator → Answer
```

## Project Structure

```
├── app.py            # Streamlit UI
├── util.py           # Core logic (fetching, processing, generating answers)
└── requirements.txt  # Dependencies
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

This is a simplified architecture summary for your README file. Let me know if you'd like any further changes!
