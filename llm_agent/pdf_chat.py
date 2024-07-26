from .llm_chains.question_answering_chain import QuestionAnsweringChain
from langchain_openai.chat_models import ChatOpenAI

from config import config

class PDFChat:
    def __init__(self):

        # llm = HuggingFaceEndpoint(
        #     endpoint_url=config.hugging_face_model_api_endpoint,
        #     task="text-generation",
        #     max_new_tokens=6096,
        #     huggingfacehub_api_token=config.hugging_face_api_key
        # )

        gpt_model_id = "gpt-4o"
        llm = ChatOpenAI(openai_api_key=config.openai_api_key,model=gpt_model_id)

        self.question_answering_agent = QuestionAnsweringChain.from_llm(llm)

    def answer_question(self, pdf_content, question, chat_history):
        answer = self.question_answering_agent.run(pdf_content=pdf_content,user_question=question, chat_history=chat_history)
        return answer

pdf_chat_client = PDFChat()
