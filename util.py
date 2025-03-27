import requests
from bs4 import BeautifulSoup
import re
import cohere
import configparser
from langchain.text_splitter import CharacterTextSplitter

class WikipediaContentFetcher:
    def __init__(self, url):
        self.url = url

    def get_full_wikipedia_content(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            content_div = soup.find(id="mw-content-text")
            paragraphs = content_div.find_all('p')
            full_text = '\n\n'.join([para.get_text() for para in paragraphs])
            full_text = re.sub(r'\[\d+\]', '', full_text)
            return full_text.strip()
        except requests.RequestException as e:
            return f"Error fetching page: {str(e)}"

class TextPreprocessor:
    @staticmethod
    def combine_strings(original_list, chunk_size=3):
        return [''.join(original_list[i:i + chunk_size]) for i in range(0, len(original_list), chunk_size)]

    @staticmethod
    def preprocess(text):
        text = text.replace('\n', '')
        lis = text.split(".")
        combined = TextPreprocessor.combine_strings(lis)
        text = "".join([i + "\n\n\n" for i in combined])
        return text

class DocumentSplitter:
    def __init__(self, chunk_size=200):
        self.chunk_size = chunk_size
        self.text_splitter = CharacterTextSplitter(separator='\n\n\n', chunk_size=self.chunk_size)

    def create_chunks(self, text):
        return self.text_splitter.create_documents([text])

class CohereReranker:
    def __init__(self, api_key, model):
        self.co = cohere.Client(api_key)
        self.model = model

    def rerank_documents(self, query, document_texts):
        rerank_results = self.co.rerank(model=self.model, query=query, documents=document_texts, top_n=2)
        context = "".join([document_texts[result.index] + "\n=======================\n" for result in rerank_results.results])
        return context

class GroqGenerator:
    def __init__(self, api_key, model):
        self.api_key = api_key
        self.model = model

    def generate_answer(self, context, query):
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        template = f"""
            Use the following CONTEXT to answer the QUESTION at the end.
            If you don't know the answer, just say that "I DONT KNOW", don't try to make up an answer.
            Also remember don't use any external knowledge and only refer to this CONTEXT to answer question.
            Consider this CONTEXT as the ultimate truth.

            CONTEXT: {context}
            QUESTION: {query}
        """
        data = {
            "model": self.model,
            "messages": [{"role": "system", "content": "You are a helpful assistant."},
                         {"role": "user", "content": template}]
        }
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return "Server error"

class KnowledgeBase:
    def __init__(self, config, url=None):
        self.config = config
        # If no URL is passed, it will fall back to config (which is from UI now)
        self.fetcher = WikipediaContentFetcher(url)
        self.preprocessor = TextPreprocessor()
        self.splitter = DocumentSplitter()
        self.reranker = CohereReranker(self.config.get('API', 'cohere_api_key'), self.config.get('Models', 'cohere_model'))
        self.generator = GroqGenerator(self.config.get('API', 'groq_api_key'), self.config.get('Models', 'groq_model'))

    def fetch_and_process(self):
        raw_content = self.fetcher.get_full_wikipedia_content()
        processed_text = self.preprocessor.preprocess(raw_content)
        documents = self.splitter.create_chunks(processed_text)
        document_texts = [doc.page_content for doc in documents]
        return document_texts

    def answer_query(self, query):
        document_texts = self.fetch_and_process()
        context = self.reranker.rerank_documents(query, document_texts)
        answer = self.generator.generate_answer(context, query)
        return answer
