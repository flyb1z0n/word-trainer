TRANSLATION_PROMPT = """
    Given the text '{text}', respond with the following information:
    0. Correct the requested text for grammar, spelling, or case errors. If the corrected text is not a proper noun, always ensure it begins with a lowercase letter, 
	1.	Provide a short definition of the fixed text in simple English. Do not include the text in the definition.
	2.	Provide the English transcription (phonetic spelling) of the fixed text.
	3.	Translate the text into Russian.
	4.	Give an example sentence using the fixed text.
	5.	Correct the requested text for grammar, spelling, or case errors (if applicable).

    Respond strictly in the following JSON format:
    {{
        "explanation": "<short definition in simple English>",
        "transcription": "<phonetic transcription>",
        "translation": "<Russian translation>",
        "text": "<corrected text, if applicable>",
        "example": "<example sentence>"
    }}

    Do not ask any clarifying questions. Only respond as instructed.
    """
