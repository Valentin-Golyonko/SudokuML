import logging

import google.generativeai as genai
from google.generativeai.types import GenerateContentResponse

logger = logging.getLogger(__name__)


class Gemini:
    """
    api_key = ""

    from help_scripts.gemini.gemini_try import Gemini
    Gemini(api_key).single_input()

    from help_scripts.gemini.gemini_try import Gemini
    Gemini(api_key).chat()

    from help_scripts.gemini.gemini_try import Gemini
    Gemini(api_key).list_all_models()

    from help_scripts.gemini.gemini_try import Gemini
    Gemini(api_key).single_input_with_config()
    """

    def __init__(self, google_api_key: str):
        genai.configure(api_key=google_api_key)

        generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }

        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
        ]

        self.model = genai.GenerativeModel(
            model_name="gemini-pro",
            generation_config=generation_config,
            safety_settings=safety_settings,
        )

        """
        model_name = Model(
            name='models/gemini-pro',
            base_model_id='',
            version='001',
            display_name='Gemini Pro',
            description='The best model for scaling across a wide range of tasks',
            input_token_limit=30720,
            output_token_limit=2048,
            supported_generation_methods=['generateContent', 'countTokens'],
            temperature=0.9,
            top_p=1.0,
            top_k=1,
        )
        """

    @staticmethod
    def list_all_models() -> None:
        for count, model_data in enumerate(genai.list_models(), 1):
            logger.debug(f"{count}: {model_data = }")

        return None

    def single_input(self) -> None:

        response = self.model.generate_content("Describe yourself.")
        self.debug_response(response)

        return None

    def chat(self) -> None:

        chat = self.model.start_chat(history=[])

        try:
            response_1 = chat.send_message("What's more: 4 or 8?")
        except Exception as ex:
            # StopCandidateException
            logger.error(f"{ex = }")
            return None
        self.debug_response(response_1)

        try:
            response_2 = chat.send_message("Ok, what about 7 and 2?")
        except Exception as ex:
            logger.error(f"{ex = }")
            return None
        self.debug_response(response_2)

        for message in chat.history:
            logger.info(f"role: {message.role}, text: {message.parts[0].text}")

        return None

    def single_input_with_config(self) -> None:

        response = self.model.generate_content(
            "Tell me a story about a magic backpack.",
            generation_config=genai.types.GenerationConfig(
                candidate_count=1,
                stop_sequences=None,  #
                max_output_tokens=2048,
                temperature=0.9,
                top_p=1.0,
                top_k=1,
            ),
        )

        self.debug_response(response)

        return None

    @staticmethod
    def debug_response(response: GenerateContentResponse) -> None:

        logger.info(f"response: {response.text}")

        for safety_rating in response.prompt_feedback.safety_ratings:
            logger.info(
                f"category: {safety_rating.category.name} = {safety_rating.category.value} | "
                f"probability: {safety_rating.probability.name} = {safety_rating.probability.value} | "
                f"blocked: {safety_rating.blocked}"
            )

        for candidate in response.candidates:
            logger.info(
                f"index: {candidate.index} | "
                f"role: {candidate.content.role} | "
                f"text: {candidate.content.parts[0].text} | "
                f"finish_reason: {candidate.finish_reason.name} = {candidate.finish_reason.value}"
            )
            for safety_rating in candidate.safety_ratings:
                logger.info(
                    f"category: {safety_rating.category.name} = {safety_rating.category.value} | "
                    f"probability: {safety_rating.probability.name} = {safety_rating.probability.value} | "
                    f"blocked: {safety_rating.blocked}"
                )

        return None
