import os
from langchain_community.document_loaders import TextLoader,DirectoryLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma # chroma can be hosted locally so i am using chroma db 
from dotenv import load_dotenv

load_dotenv()





def load_documents(docs_path="docs"):
    """Load all the files form the docs directory"""
    print (f"loading documerns form {docs_path}...")

    #constrent check if directory exist or not 
    if not os.path.exists(docs_path):
        raise FileNotFoundError(f"the directory{docs_path} does not exist. Please create it and add it to your company file")
    
    #load all .text files form the doc directory
    loader=DirectoryLoader(
        path=docs_path,
        glob="*.txt",
        loader_cls=TextLoader
    )

    documents= loader.load()

    if len(documents)==0:
        raise FileNotFoundError(f"there is no .txt file in {docs_path} . Please adOpenAIEmbeddingsd it to your company file")
    
    for i, doc in enumerate(documents[:2]):
        print(f"\n Document {i+1}")
        print(f"\n Source: {doc.metadata['source']} ")
        print(f"\n content length: {len(doc.page_content)} characters")
        print(f"\n content preview: {doc.page_content[:100]}...")
        print(f"\n metadata: {doc.metadata}")

    return documents

def split_documents(documents, chunk_size=1000, chunk_overlap=0):
     """split documents into smaller chunks with overlap""" 
     print("splitting documents into chunk")
     text_splitter = CharacterTextSplitter(         # basic text spliter in langcahne
     chunk_size=chunk_size,
     chunk_overlap=chunk_overlap)

     chunks=text_splitter.split_documents(documents)
     
     if chunks:
         for i, chunk in enumerate(chunks[:5]):
             print(f"\n -----chunk {i+1} ----")
             print(f"Source: {chunk.metadata['source']} ")
             print(f"length: {len(chunk.page_content)} characters")
             print(f"content:")
             print(chunk.page_content)
             print("_"*50)

             if len(chunks)>5:
                 print(f"\n ... and {len(chunks)-5 } more chunks")
     return chunks


def create_vector_store(chunks, persist_directory="db/chroma_db"):
    """create and presist ChromaDB vectore store"""
    print('creating. embedding and storing in ChromaDB')

    embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

    print("---creating vector store---")
    vectorestore =Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=persist_directory, # store locally
        collection_metadata={"hnsw:space":"cosine"} # algo used to retrive the top result (more on this afterwards)
    )

    print("---Finished creating vector store---")
    print(f"vectore store created and saved to {persist_directory}")
    return vectorestore




#loadign the file
def main():
    print("Main Function")

    documents= load_documents(docs_path="docs")

#2 chunking the file
    chunks=split_documents(documents)

#3Embedding the sorting the vector DB
    vectorestore=create_vector_store(chunks)



if __name__=="__main__":
    main()




