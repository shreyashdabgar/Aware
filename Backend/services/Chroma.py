from Backend.services.chunk import Embeddings, chunks, question_embedding
import chromadb
import ollama
from Backend.services.LLM import llm
from flask import jsonify
import time 
import re


MODEL_NAME="nomic-embed-text"


# Making client for vector DB
client = chromadb.PersistentClient(path = r"D:\Aware\Backend\instance")

def store_chunks(embeddings, chunks_list, video_id):
    try:
        # FIX 1: Change this target key to 'semantic_text' instead of 'text'
        # This populates ChromaDB documents with clean, normalized sentences
        text_field = [i['semantic_text'] for i in chunks_list]
        
        collection = client.get_or_create_collection(name="vector_Collection")

        collection.add(
            embeddings=embeddings,
            documents=text_field, # Now stores semantic strings
            metadatas=[{
                'start_time': i['start_time'],
                'end_time': i['end_time'],
                "video_id" : video_id,
                "raw_text": i['text'] # Optional: Preserves raw transcription in metadata if needed later
            } for i in chunks_list],

            ids = [ f"video_{video_id}_chunk_{i}" for i in range(len(chunks_list))]
        )

        return True
    except Exception as e:
        print("there is error in store_chunks function:", e)
        return False


def serching_chunks(question, video_id):
    try:
        start = time.perf_counter()

        embedding_start = time.perf_counter()
        query_embedding = question_embedding(question)
        embedding_time = time.perf_counter() - embedding_start

        search_start = time.perf_counter()

        collection = client.get_or_create_collection(
            name="vector_Collection"
        )

        result = collection.query(
            query_embeddings=query_embedding,
            n_results=2,
            where={"video_id": video_id}
        )

        search_time = time.perf_counter() - search_start

        documents = result["documents"][0] if result["documents"] else []

        print(f"Question embedding: {embedding_time:.2f}s")
        print(f"Chroma search: {search_time:.2f}s")
        print(f"Total retrieval: {time.perf_counter() - start:.2f}s")

        return documents

    except Exception as e:
        print("Search error:", e)
        raise




import time

def is_general_message(question):
    general_messages = {
        "hi", "hello", "hey", "hey there",
        "good morning", "good afternoon", "good evening",
        "thanks", "thank you", "thank you so much",
        "bye", "goodbye", "see you",
        "how are you", "who are you"
    }

    return question.strip().lower().rstrip("!.?") in general_messages


def ask_question(question, video_id,conversation_history=None):
    try:
        conversation_history = conversation_history or []
        start = time.perf_counter()
        # STEP 1: Handle obvious general conversation
        if is_general_message(question):
            return llm(
                {"question": question},
                mode="general",
                history=conversation_history,
            )

        # STEP 2: Retrieve video context
        retrieval_start = time.perf_counter()

        retrieved = serching_chunks(question, video_id)

        if not retrieved:
            return "I couldn't find relevant information in this video."

        context = " ".join(retrieved)
        retrieval_time = time.perf_counter() - retrieval_start

        # STEP 3: Generate video-based answer
        llm_start = time.perf_counter()

        prompt = {
            "context": context,
            "question": question,
            "history": conversation_history
        }

        llm_response = llm(prompt, mode="answer", history= conversation_history)

        llm_time = time.perf_counter() - llm_start
        total_time = time.perf_counter() - start

        print(f"Retrieval: {retrieval_time:.2f}s")
        print(f"LLM generation: {llm_time:.2f}s")
        print(f"Total: {total_time:.2f}s")

        return llm_response

    except Exception as e:
        print("Error in ask_question:", e)
        raise
