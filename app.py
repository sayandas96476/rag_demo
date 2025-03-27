import streamlit as st
import util 

# Initialize session state
if "step" not in st.session_state:
    st.session_state["step"] = 1
if "documents" not in st.session_state:
    st.session_state["documents"] = None
if "documented_texts" not in st.session_state:
    st.session_state["documented_texts"] = None
if "urls" not in st.session_state:
    st.session_state["urls"] = []

st.title("Web Search RAG")

# Input Box 1 - Add Multiple URLs
new_url = st.text_input("Enter a URL to add:", key="new_url")
if st.button("Add URL"):
    if new_url:
        st.session_state["urls"].append(new_url)
    else:
        st.warning("Please enter a URL before adding.")

st.write("### Added URLs:")
st.write(st.session_state["urls"])

if st.button("Process URLs"):
    if st.session_state["urls"]:
        text = ""
        st.write("Processing URLs...")
        for url in st.session_state["urls"]:
            text += util.WikipediaContentFetcher(url).get_full_wikipedia_content()
        
        # Preprocessing and chunking
        text = util.TextPreprocessor.preprocess(text)
        documents = util.DocumentSplitter().create_chunks(text)
        documented_texts = [doc.page_content for doc in documents]
        st.write(documented_texts)

        # Store processed data in session state
        st.session_state["documents"] = documents
        st.session_state["documented_texts"] = documented_texts
        st.session_state["step"] = 2
    else:
        st.warning("Please add at least one URL before processing.")

# Input Box 2 (Always Visible)
input2 = st.text_input("Enter second input:", key="input2")
if st.button("Submit"):
    if input2:
        if st.session_state["documents"] and st.session_state["documented_texts"]:
            query = input2
            # Pass the dynamically added URL from UI into KnowledgeBase
            kb = util.KnowledgeBase(st.session_state.get('config'), url=st.session_state["urls"][-1] if st.session_state["urls"] else None)
            CONTEXTS = kb.reranker.rerank_documents(query, st.session_state["documented_texts"])
            answer = kb.generator.generate_answer(CONTEXTS, query)
            st.write(answer)
        else:
            st.warning("Please complete step 1 first.")
    else:
        st.warning("Please enter text before submitting.")
