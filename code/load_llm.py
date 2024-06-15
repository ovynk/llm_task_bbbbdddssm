import os
import enhance_data

from llama_index.llms.openai import OpenAI
from llama_index.core import (Settings,
                              SimpleDirectoryReader,
                              VectorStoreIndex,
                              StorageContext,
                              load_index_from_storage)


os.environ["OPENAI_API_KEY"] = "YOUR API KEY"
Settings.llm = OpenAI(temperature=0.5, model="gpt-3.5-turbo")
RUN_TEST_QUERIES = True


def create_save_data(excel_path, name_dir='enhance_data_indexed'):
    enhance_data.enhance_data(excel_path, save_to='../output/')

    data = SimpleDirectoryReader(input_files=['../output/enhanced_data.txt'], errors='replace').load_data()
    index = VectorStoreIndex.from_documents(data)
    index.storage_context.persist(persist_dir=f"../output/{name_dir}")


def load_chat_engine(dir_path):
    storage_context = StorageContext.from_defaults(persist_dir=dir_path)
    return load_index_from_storage(storage_context).as_chat_engine()


def main():
    # once created, use load_chat_engine
    # create_save_data('../merged_data_test_task.xlsx')

    if RUN_TEST_QUERIES:
        chat_engine = load_chat_engine('../output/enhance_data_indexed')

        print(chat_engine.chat('Say price and currency of G63 in BeringCars'), '\n')
        chat_engine.reset()

        print(chat_engine.chat('Where to find Audi RS6 in Spain.'), '\n')
        chat_engine.reset()

        print(chat_engine.chat('List me SUV in Italy.'), '\n')
        chat_engine.reset()

        print(chat_engine.chat('List me Audi RS6 in Spain.'), '\n')
        print(chat_engine.chat('Give me variants of Audi RS6 in Italy.'), '\n')
        print(chat_engine.chat('Give me a list of 3 cars with lowest price in both locations.'), '\n')
        chat_engine.reset()

        # bonus questions
        print(chat_engine.chat('Find me cars for an off-road weekend in Spain'), '\n')
        chat_engine.reset()
        print(chat_engine.chat('Offer me a car from a company founded in 1939 in Italy'), '\n')
        chat_engine.reset()


if __name__ == "__main__":
    main()
