# A chatbot that interprets natural language input, converts it into SQL queries, executes those queries, and presents the results.
A Natural Language to SQL (NL2SQL) converter is a powerful tool that significantly enhances data interaction by making it more accessible and efficient. It allows non-technical users to query databases using natural language, leading to increased efficiency, productivity, error reduction, and enhanced data exploration.
This project provides a comprehensive introduction to using the Llama 3 70B model within the realm of generative AI, demonstrating its application in converting natural language into  SQL queries(MYSQL database).
Please refer to the YouTube video below for a demonstration.For this demonstration i have used sample database from [Sample Mysql database](https://www.mysqltutorial.org/getting-started-with-mysql/mysql-sample-database/)


<a href="https://youtu.be/NYlC8PhgFUA">
    <img src="https://img.youtube.com/vi/NYlC8PhgFUA/maxresdefault.jpg" alt="Watch the video" width="400"/>
</a>


## Table of Contents

- [Main Features](#main-features)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Step 1: Clone the Repository](#step-1-clone-the-repository)
  - [Step 2: Create and Activate a Conda Environment](#step-2-create-and-activate-a-conda-environment)
  - [Step 3: Install the Required Packages](#step-3-install-the-required-packages)
  - [Step 4: Create an .env File and Add Necessary API Keys](#step-4-create-an-env-file-and-add-necessary-api-keys)
- [Usage](#usage)
- [Design details and working](#design-details-and-working)



## Main Features
- **Natural Language Processing**: Uses Llama 3 70B model to interpret and respond to user queries in natural language.
- **SQL Query Generation and execution**: It seamlessly connects to a MySQL database, automatically generates SQL queries, executes them, and displays the results based on the user's natural language input. .
- **Streamlit GUI**: Features a user-friendly interface provides a real-time interactivity, where changes in the application or user inputs are immediately reflected in the UI.


## Installation
To get started with this project, follow the steps below to set up your environment using Conda.

### Prerequisites

Ensure that you have Conda installed on your machine. If not, you can install it from the [official website](https://docs.conda.io/en/latest/miniconda.html).
Additionally, ensure you have access to a MySQL database along with the necessary connection credentials.

### Step 1: Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/harshith-np/NL2SQL.git
cd NL2SQL
```
### Step 2: Create and Activate a Conda Environment
Create a new Conda environment and activate it:
```bash
conda create --name nl2sql_env python=3.8
conda activate nl2sql_env
```

### Step 3:Install the required packages:

```bash
pip install -r requirements.txt
```

### Step 3:Create an .env file add necessary api keys:

```bash
OPENAI_API_KEY=[your-openai-api-key]
GROQ_API_KEY=[your-openai-api-key]
LANGCHAIN_API_KEY=[your-openai-api-key]
HUGGINGFACEHUB_API_KEY=[your-openai-api-key]
LANGCHAIN_TRACING_V2=[true or false]
```

## Usage
To launch the Streamlit app and interact with the chatbot:

```bash
streamlit run app.py
```

## Design details and working

![Chatbot Architecture](./uploads/architecture_nl2sql.png)
### Design Phase
- In the design phase, I am utilizing a pre-configured MySQL database with a pre-loaded schema.
- I will connect to the Llama 3 model using ChatGroq.
- LangChain simplifies the creation of NL2SQL models by providing a flexible framework that integrates seamlessly with existing databases and natural language processing (NLP) models.
- Additionally, I leverage message history to adjust the prompts sent to the model for SQL query generation. This adjustment includes details from prior queries and responses, aiding the model in grasping the context of subsequent questions. The system will then return the corresponding SQL query for each natural language question.
- Finally the query is run and it generates the output.
### Implementation Phase
- To build the NL2SQL model with LangChain, ensure that LangChain is installed and connected to your database.
- For demonstration purposes, I am using MySQL, but LangChain supports various database systems, allowing users to connect to any type of database and obtain the corresponding SQL query output.You will need to use your database credentials to establish a connection that LangChain can utilize to interact with your data.
- The core of the NL2SQL process is managed by the **get_sql_chain function**, which involves three major steps:
  -  **Generating the prompt**
  -  **Passing it to the LLM**
  -  **Parsing the output**
-  We would be using LangChain’s SQL query generator method, **create_sql_query_chain**. This method uses the database instance, prompt, and LLM model as inputs to generate SQL queries.
- To set parameters for the LLM, I used **RunnablePassThrough** to specify the schema and dialect details.
- The schema information is crucial because the model needs to understand the table definitions, views, and other database structures to generate accurate SQL queries.
- The dialect parameter indicates the type of database in use; for instance, although I am using MySQL, this parameter allows specifying any database type.These schema and dialect details are included in the prompt to ensure the correct output.
- When a user asks a question, the system checks if there is any session history saved. If a session exists, its history is retrieved and used to generate the current query output. If there is no existing session, the interaction is treated as a new conversation. The response is then saved back into the chat history.
- Additionally, you can use dialect-specific prompting for prompt generation. Instead of using a generic prompt, you can create a specific prompt tailored to the SQL dialect in use, using **DSP (Dialect-Specific Prompting)**.
- **Prompt engineering** plays a crucial role in directing how the queries are generated. By providing certain questions and their corresponding answers through the prompt, the LLM learns and uses this knowledge to predict accurate queries.
- I've added a feature called **Few Shot Examples** to improve model performance, especially for complex queries, by including examples of natural language questions converted to valid SQL queries. Including all the examples in the prompt is inefficient for answering simple queries, so we need to send only the necessary examples for accurate predictions.
- Few Shot functionality processes and selects the right example queries.**Dynamic Few Shot** is similar but generates the few shot prompt during runtime. Given enough examples, we only include the most relevant ones in the prompt to avoid exceeding the model's context window or distracting it with irrelevant information.
- This is achieved using an ExampleSelector, specifically a **SemanticSimilarityExampleSelector**, which stores examples in a chosen vector database.
- At runtime, it performs a similarity search between the input and examples, returning the most semantically similar ones. By default, hugging face embeddings are used, but you can swap them for your preferred model provider.
- To further enhance the NL2SQL model, I have integrated LangSmith .**LangSmith** offers comprehensive logging and monitoring capabilities that can be done by setting environment variable **LANGCHAIN_TRACING_V2=true**. Each generated query and its performance metrics (like execution time, accuracy, etc.) are logged. This helps in identifying bottlenecks and areas of improvement in real-time. 
