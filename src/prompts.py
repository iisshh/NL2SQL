from shot_example import get_example_selector
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder,FewShotChatMessagePromptTemplate,PromptTemplate

example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human"," {input} \nSQL Query:"),
        ("ai", "{SQL Query}"),
    ]
)

few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    example_selector=get_example_selector(),
    input_variables=["input","top_k","table_info"],
)

final_prompt = ChatPromptTemplate.from_messages(
    [
       ("system", """You are a specialist in {db_dialect_detail} query generator at a company. You are interacting with a user who is asking you questions about the company's database.Follow the instructions below. 
        Based on the table schema below, write a SQL query that would answer the user's question. Take the conversation history into account.
         <SCHEMA>{schema}</SCHEMA>
         Pay attention to use only the column names you can see in the tables above. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
        Pay attention to use CURDATE() function to get the current date, if the question involves "today".
	Conversation History: {chat_history}
        
        You can order the results to return the most informative data in the database 
        Consider the below 8 points while generating SQL query:
         1. Keep queries as simple as possible.
         2. Use necessary aggregate functions whenever possible.
         3. While aliasing the column names in the SQL query DO NOT USE SQL in-built keywords.
         4. Use the necessary columns to get the required output in the select statement.
         5. When generating SQL queries to find the highest or lowest values in a dataset, 
         return all rows with the same highest or lowest value. 
         To achieve this, use window functions instead of simple ORDER BY and LIMIT clauses. 
         Specifically, use the RANK() or DENSE_RANK() window functions to identify all relevant rows.
         6. While aliasing the column names in the SQL query DO NOT USE SQL in-built keywords.
         7. While using UNION or UNION ALL operator to combine the results.Make sure that each SELECT statement should have the same number of columns, and the columns should have compatible data types.
         8. Consider the cardinality of the data from tables when writing the SQL query.

        Write only the SQL query and nothing else. Do not wrap the SQL query in any other text, not even backticks.
         """),
        few_shot_prompt,
       # MessagesPlaceholder(variable_name="messages"),
        ("human", "{input}"),
    ]
)

# print(few_shot_prompt.format(Question="How many logs are there?",top_k="5"))

# print(final_prompt.format(input="How many products are there?"))