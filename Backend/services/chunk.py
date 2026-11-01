import time
import ollama


MODEL_NAME = "nomic-embed-text"


def chunks(transcript):
    try:
        max_chars = 1000

        result_chunks = []
        current_chunk = []
        current_len = 0

        current_start = 0.0
        current_end = 0.0

        for segment in transcript:
            text = segment["text"]
            start = segment["start"]
            end = segment["end"]
            semantic_text = segment["semantic_text"]

            if not current_chunk:
                current_start = start

            current_end = end

            current_chunk.append({
                "text": text,
                "start": start,
                "end": end,
                "semantic_text": semantic_text
            })

            current_len += len(semantic_text)

            if current_len >= max_chars:
                result_chunks.append({
                    "text": " ".join(
                        item["text"] for item in current_chunk
                    ),
                    "semantic_text": " ".join(
                        item["semantic_text"] for item in current_chunk
                    ),
                    "start_time": current_start,
                    "end_time": current_end
                })

                current_chunk = []
                current_len = 0
                current_start = 0.0
                current_end = 0.0

        # Add remaining segments
        if current_chunk:
            result_chunks.append({
                "text": " ".join(
                    item["text"] for item in current_chunk
                ),
                "semantic_text": " ".join(
                    item["semantic_text"] for item in current_chunk
                ),
                "start_time": current_start,
                "end_time": current_end
            })

        return result_chunks

    except Exception as e:
        print("Chunking error:", repr(e))
        raise


def Embeddings(chunks_list):
    """
    Generate embeddings for video chunks.
    Uses Ollama's default GPU placement.
    """

    try:
        if not chunks_list:
            return []

        start_time = time.perf_counter()

        response = ollama.embed(
            model=MODEL_NAME,
            input=[
                item["semantic_text"]
                for item in chunks_list
            ],
            keep_alive="10m"
        )

        embeddings = response["embeddings"]

        elapsed = time.perf_counter() - start_time

        print(
            f"Video embeddings (GPU): {elapsed:.2f} seconds"
        )

        return embeddings

    except Exception as e:
        print("Video Embeddings error:", repr(e))
        raise


def question_embedding(question):
    """
    Generate the user's question embedding.
    Requests CPU placement to reduce GPU memory contention
    with the Qwen answer-generation model.
    """

    try:
        start_time = time.perf_counter()

        response = ollama.embed(
            model=MODEL_NAME,
            input=question,
            options={
                "num_gpu": 0
            },
            keep_alive="10m"
        )

        embeddings = response["embeddings"]

        elapsed = time.perf_counter() - start_time

        print(
            f"Question embedding (CPU): {elapsed:.2f} seconds"
        )

        if not embeddings:
            raise RuntimeError(
                "Ollama returned an empty question embedding."
            )

        return embeddings

    except Exception as e:
        print("Question embedding error:", repr(e))
        raise