TRANSLATION_PROMPT = """
    Given text '{text}', respond with the following information:
    1. Provide short definition of '{text}' using simple english, no need to mention `{text}`?
    2. Provide english transcription.
    3. Translate to russian.
    4. Give an example of using it in a sentence.
    5. Fix the requested text if you spot any mistakes (and case as well)
     Respond with the following json format:
    {{
        "explanation": <explanation>,
        "transcription": <transcription>,
        "translation": <translation>,
        "text": <requested text>,
        "example": <example>
    }}
    No further question, just do.
    """
