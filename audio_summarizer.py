from langchain.document_loaders.parsers import OpenAIWhisperParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders.generic import GenericLoader
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from dotenv import load_dotenv
load_dotenv()

class AudioSummarizer:

    def __init__(self, loader_path = "/tmp/", glob_pattern="*.ogg") -> None:
        self.parser = self._create_parser()
        self.llm = self._create_llm()
        self.loader = self._create_loader(loader_path, glob_pattern)
        self.llm_chain = self._create_llm_chain()
        self.map_chain = self._create_map_chain()
        self.text_splitter = self._create_text_splitter(token_chunk_size = 4000)

    def _create_text_splitter(self, token_chunk_size):
        # one token = 4 characters, therefore multiply the token chunk size by 4
        # RecursiveCharacterTextSplitter measures the leght with len(), therefore
        # we have to take character length into account
        return RecursiveCharacterTextSplitter(chunk_size = token_chunk_size * 4)

    def _create_llm(self):
        return OpenAI(temperature=0)

    def _create_parser(self):
        return OpenAIWhisperParser()

    def _create_loader(self, path, glob_pattern):
        return GenericLoader.from_filesystem(
            path = path,
            glob = glob_pattern,
            suffixes = [".ogg"],
            show_progress = True,
            parser = self.parser
        )

    def _create_prompt(self, input_variables, template):
        return PromptTemplate(
            input_variables=input_variables,
            template=template
        )

    def _create_llm_chain(self):

        llm_chain_prompt = self._create_prompt(["text"], """
                    The following text is a transcribed voice message or audio file.
                    Write summary of it in the same language as the text is.
                    It is important to as much information as possible.
                    If questions are asked, return these questions. 
                    If possible make a bullet point summary.
                    Answer in the same language as the text.
                    Here comes the text:{text}""")

        return LLMChain(
            llm = self.llm,
            prompt = llm_chain_prompt,
            verbose = True
        )

    def _create_map_chain(self):

        map_prompt = self._create_prompt(input_variables=["text"], 
                                        template = """
                                            The following text is a part of a transcribed voice message or audio file.
                                            Write summary of it in the same language as the text is.
                                            It is important to as much information as possible.
                                            Here comes the text:
                                            "{text}"
                                            SUMMARY:
                                            """)
        
        combine_prompt = self._create_prompt(input_variables=["text"],
                                             template ="""
                                                Write a summary of the following text, which consists of summaries of parts from a transcribed
                                                voice message or audio file. Sumarize in the same language as the text is.
                                                It is important to keep as much information as possible.
                                                Here comes the text:
                                                "{text}"
                                                SUMMARY:    
                                                """)

        return load_summarize_chain(
            llm = self.llm,
            chain_type = "map_reduce",
            verbose = True,
            map_prompt = map_prompt,
            combine_prompt = combine_prompt,
        )

    def summarize(self):
        transcribed_documents = self.loader.load()
        documents = self.text_splitter.transform_documents(transcribed_documents)
        if len(documents) > 1:
            summary = self.map_chain.run(input_docuemnts = documents)
        else:
            summary = self.llm_chain.run(text = documents[0].page_content)
        return {"summary": summary, "full_text": transcribed_documents[0].page_content}