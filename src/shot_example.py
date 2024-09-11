import json
import os
from langchain_community.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
#from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder,FewShotChatMessagePromptTemplate,PromptTemplate


def get_example_selector():
    #load_dotenv()
    root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    json_file_path = os.path.join(root_folder, 'utils', 'examples.json')
    #read the example shots
    with open(json_file_path, 'r') as file:
            data = json.load(file)
        
    vectorstore = Chroma()
    vectorstore.delete_collection()
    example_selector = SemanticSimilarityExampleSelector.from_examples(
        data,
        HuggingFaceEmbeddings(),
        vectorstore,
        k=2,
        input_keys=["input"],
    )
    return example_selector
#print(example_selector.select_examples({"Question": "how many logs are we have in the table?"}))

