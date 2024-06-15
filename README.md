# Car sellers database chatbot <br> using LlamaIndex and Telegram bot

## Usage
To run telegram bot you need to specify your OpenAi api key  in load_llm.py and Telegram api key in tg_bot.py. Then run tb_bot.py

There is already all data and processed data as well.
But if you want to change data you need to load it in main folder. File must have same columns as 'merged_data_test_tasl.xlsx'.
Then specify it in load_llm.py and use function create_save_data in main function, so that data would be processed.
After that you can ran tg_bot.py to use telegram bot.

## Example
![example_llm_chat_bot](https://github.com/ovynk/llm_task_bbbbdddssm/assets/90598021/4d56593f-f27f-481d-8a33-82257433976a)

## Concept
Main idea is to make data more understandable. 
Read file with llama-index SimpleDirectoryReader or read pd.DataFrame performs worse than processed data.
I process data in enhance_data.py. Remove some columns, fill none values, and restructure it in custom format.
I get txt file which will be loaded with SimpleDirectoryReader.

After that I index this data and save it. Next step is to load these indexes and use chat engine for Q&A.
