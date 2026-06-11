import streamlit as st
from utils.gemini_helper import get_gemini_model, get_gemini_embeddings
from utils.vector_store import get_vector_store, get_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate


def render():
    st.title("🤖 AI Tutor")
    st.markdown("Ask questions about your uploaded PDFs or Lecture Notes.")

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display chat messages from history on app rerun
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("What would you like to know?"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            message_placeholder = st.empty()

            try:
                embeddings = get_gemini_embeddings()
                vector_store = get_vector_store(embeddings)
                retriever = get_retriever(vector_store)
                llm = get_gemini_model()

                system_prompt = (
                    "You are an AI Tutor that explains difficult concepts in simple language. "
                    "Use the following pieces of retrieved context to answer the question. "
                    "If you don't know the answer based on the context, say so but provide a helpful general answer. "
                    "Context: {context}"
                )

                prompt_template = ChatPromptTemplate.from_messages([
                    ("system", system_prompt),
                    ("human", "{input}"),
                ])

                question_answer_chain = create_stuff_documents_chain(llm, prompt_template)
                rag_chain = create_retrieval_chain(retriever, question_answer_chain)

                with st.spinner("Thinking..."):
                    response = rag_chain.invoke({"input": prompt})
                    answer = response["answer"]

                    # Display the answer
                    message_placeholder.markdown(answer)

                    # Add to history
                    st.session_state.chat_history.append({"role": "assistant", "content": answer})

                    # Optionally show sources
                    if "context" in response and response["context"]:
                        with st.expander("Sources"):
                            for i, doc in enumerate(response["context"]):
                                st.write(f"**Chunk {i+1}:**")
                                st.write(doc.page_content)
                                st.markdown("---")

            except Exception as e:
                st.error(f"Error connecting to AI Tutor: {e}. Make sure you have uploaded some documents first to populate the database.")
