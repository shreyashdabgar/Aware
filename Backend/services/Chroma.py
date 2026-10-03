from Backend.services.chunk import Embeddings, chunks
from Backend.services.Video_preprocessing import SpeechToText, extract_audio
import chromadb
import ollama

client = chromadb.PersistentClient(path = "D:\Aware\Backend\instance")


def chromaDB(chunks_list,que_embeddings):
    try:
        text_field = [i['text'] for i in chunks_list]

        collection = client.get_or_create_collection(name="Aware_Collection")

        # Create embeddings for the text field
        embeddings = Embeddings(chunks_list)
        collection.add(
            embeddings=embeddings,
            documents=text_field,
            metadatas=[{"start_time": i['start_time'], "end_time": i['end_time']} 
                       for i in chunks_list],
            ids = [str(i) for i in range(len(chunks_list))]
        )

        '''question simlirity search'''
        result = collection.query(
           query_embeddings=que_embeddings,
            n_results=3
        )

        retrievd_text  = result['documents'][0]#parsing only text from result
        context = " ".join(retrievd_text)# making the one sentence of piece of chunks

        return context

    
    except Exception as e:
        print("There is an error in chromaDB:", e)
        return False
