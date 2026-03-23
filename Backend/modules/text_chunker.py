def chunk_text(text, chunk_size=1500):
    """
    Split text into chunks of given word size.
    Used only for LLM processing.
    """

    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks
