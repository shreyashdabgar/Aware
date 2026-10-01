def chunks(transcript):
    try:
        max_chars = 1000

        chunks = []
        current_chunk = []
        current_len = 0
        current_start = 0.0
        current_end = 0.0

        for i in transcript:
            Text = i['text']
            Start = i['start']
            End = i['end']

            # First segment of a new chunk
            if not current_chunk:# check that current chunk is empty
                current_start = Start

            # Every segment updates the latest end time
            current_end = End

            current_chunk.append([Text, Start, End])

            length = len(Text)
            current_len += length

            # Chunk is complete
            if current_len >= max_chars:
                chunks.append({
                    'text': ' '.join(segment[0] for segment in current_chunk),
                    'start_time': current_start,
                    'end_time': current_end
                })

                current_chunk = []
                current_len = 0
                current_start = 0.0
                current_end = 0.0

        # Add remaining chunk
        if current_chunk:
            chunks.append(current_chunk)
        return chunks

    except Exception as e:
        print("There is an error in chunks:", e)
        return []