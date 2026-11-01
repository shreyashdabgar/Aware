import ollama 
import time
from lingua import Language, LanguageDetectorBuilder




def llm(prompt: dict, mode="answer"):
    try:
        start = time.perf_counter()

        if mode == "classify":
            response = ollama.chat(
                model="qwen2.5:3b",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Classify the user's message. "
                            "Return only 'general' for greetings, "
                            "small talk, gratitude, or farewells. "
                            "Return only 'video' for questions or "
                            "requests about the uploaded video. "
                            "If uncertain, return 'video'. "
                            "Do not explain."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt["question"]
                    }
                ],
                keep_alive=-1,
                options={
                    "temperature": 0,
                    "num_predict": 5
                }
            )

        elif mode == "general":
            response = ollama.chat(
                model="qwen2.5:3b",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are Aware, a friendly video assistant. "
                            "Respond naturally and warmly to greetings, "
                            "thanks, small talk, and farewells. "
                            "Keep replies concise. "
                            "Do not pretend to have feelings or experiences."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt["question"]
                    }
                ],
                keep_alive=-1,
                options={
                    "temperature": 0.7,
                    "num_predict": 100
                }
            )

        elif mode == "answer":
            response = ollama.chat(
                model="qwen2.5:3b",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a helpful assistant answering questions about a video. "
                            "Use ONLY the provided context as your source of truth. "
                            "Do not use outside knowledge or make assumptions. "
                            "If the context contains an explicit statement that answers "
                            "the question, follow it exactly. "
                            "If the answer cannot be determined from the context, "
                            "say 'I don't know'. "
                            "Answer clearly and concisely in a maximum of 2-3 sentences."
                        )
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Context:\n{prompt['context']}\n\n"
                            f"Question: {prompt['question']}"
                        )
                    }
                ],
                keep_alive=-1,
                options={
                    "temperature": 0,
                    "num_predict": 120
                }
            )

        else:
            raise ValueError(f"Unknown LLM mode: {mode}")

        print("\n--- OLLAMA PERFORMANCE ---")
        print(f"Total: {response.get('total_duration', 0) / 1e9:.2f}s")
        print(f"Model load: {response.get('load_duration', 0) / 1e9:.2f}s")
        print(f"Prompt tokens: {response.get('prompt_eval_count', 0)}")
        print(f"Prompt evaluation: {response.get('prompt_eval_duration', 0) / 1e9:.2f}s")
        print(f"Generated tokens: {response.get('eval_count', 0)}")
        print(f"Generation time: {response.get('eval_duration', 0) / 1e9:.2f}s")

        result = response["message"]["content"].strip()

        if mode == "classify":
            result = result.lower()

        print(f"LLM ({mode}) time: {time.perf_counter() - start:.2f}s")

        return result

    except Exception as e:
        print(f"LLM ({mode}) error:", e)
        raise


def semantic_normalization(transcript : list):
    try:
        normalize = []

        for i in range(0, len(transcript), 10):
            group = transcript[i:i + 10]
            text = " ".join(j["text"] for j in group)

            call_start = time.perf_counter()

            response = ollama.chat(
                model="qwen2.5:3b",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You normalize speech transcripts into clear English. "
                            "Preserve the speaker's exact meaning and all factual details. "
                            "Do not summarize, explain, or add information. "
                            "Preserve names, numbers, negation, technical terms, and uncertainty. "
                            "Return only the normalized transcript. "
                            "No introduction, headings, bullet points, commentary, or questions. "
                            "If the text is already clear, make minimal changes."
                        )
                    },
                    {"role": "user", "content": text}
                ]
            )

            call_time = time.perf_counter() - call_start
            print(f"Qwen call {i // 10 + 1}: {call_time:.2f} seconds")

            semantic_normalization = response["message"]["content"]

            if group:
                start = group[0]["start"]
                end = group[-1]["end"]
                normalize.append({"start": start, "end": end, "semantic_text": semantic_normalization, "text" : text})

        return normalize
    except Exception as e:
        print("there is the error in semantic normalzation services", repr(e))
        return False




