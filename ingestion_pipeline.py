import os
from langchain_community.document_loaders import TextLoader,DirectoryLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma # chroma can be hosted locally so i am using chroma db 
from dotenv import load_dotenv

load_dotenv()





def main():
    print("main fun")
    
    



if __name__=="__main__":
    main() 