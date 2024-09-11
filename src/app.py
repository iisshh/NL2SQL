from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain.chains import create_sql_query_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from prompts import final_prompt
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from decimal import Decimal
import datetime


st.set_page_config(page_title="LLAMA model 3 70B  for Natural language to SQL", page_icon=":speech_balloon:")

def init_database(user: str, password: str, host: str, port: str, database: str) -> SQLDatabase:
    try:
        db_uri = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
        db_connect=SQLDatabase.from_uri(db_uri)
        return db_connect
    except:
        return None


def get_sql_chain(db):
    template = """
        You are a specalisit in {db_dialect_detail} query generator  at a company. You are interacting with a user who is asking you questions about the company's database.
        You can tell about yourself.When you have asked about the following instructions below. 
        Based on the table schema below, write a SQL query that would answer the user's question. Take the conversation history into account.
         <SCHEMA>{schema}</SCHEMA>
    
        Conversation History: {chat_history}

        Write only the SQL query and nothing else. Do not wrap the SQL query in any other text, not even backticks.
        
        For example:
        Question: "List all customers in France with a credit limit over 20,000.",
        SQL Query: "SELECT * FROM customers WHERE country = 'France' AND creditLimit > 20000;"
        Question: "Get the highest payment amount made by any customer.",
        SQL Query: "SELECT MAX(amount) FROM payments;"
        Question: "Show product details for products in the 'Motorcycles' product line.",
        SQL Query: "SELECT * FROM products WHERE productLine = 'Motorcycles';"
        Question: "Retrieve the names of employees who report to employee number 1002.",
        SQL Query: "SELECT firstName, lastName FROM employees WHERE reportsTo = 1002;"
        Question: "List all products with a stock quantity less than 7000.",
        SQL Query: "SELECT productName, quantityInStock FROM products WHERE quantityInStock < 7000;"
        Question:"what is price of `1968 Ford Mustang`",
        SQL Query: "SELECT `buyPrice`, `MSRP` FROM products  WHERE `productName` = '1968 Ford Mustang' LIMIT 1;"   
        Question: "List all orders with their associated customer names and order dates."
        SQL Query:"SELECT orders.orderNumber, customers.customerName, orders.orderDate FROM orders JOIN customers ON orders.customerNumber = customers.customerNumber;"
        Question: "Show the details of employees and their offices."
        SQL Query:"SELECT employees.employeeNumber, employees.firstName, employees.lastName, offices.city, offices.country FROM employees
        JOIN offices ON employees.officeCode = offices.officeCode;"
        Question: "List all products in each order along with order dates."
        SQL Query:"SELECT orders.orderNumber, orders.orderDate, orderdetails.productCode, orderdetails.quantityOrdered FROM orders JOIN orderdetails ON orders.orderNumber = orderdetails.orderNumber;"
        Question: "Find the total sales amount for each customer."
        SQL Query:"SELECT customerNumber, SUM(amount) AS totalSales FROM payments GROUP BY customerNumber";
        Question: "Count the number of orders placed by each customer."
        SQL Query:"SELECT customerNumber, COUNT(orderNumber) AS orderCount FROM orders GROUP BY customerNumber";
        Question: "Find the average credit limit for customers in each country."
        SQL Query:"SELECT country, AVG(creditLimit) AS avgCreditLimit FROM customers GROUP BY country;"
        Question: "List customers with total payments exceeding 50,000."
        SQL Query:"SELECT customerNumber, SUM(amount) AS totalPayments FROM payments GROUP BY customerNumber HAVING SUM(amount) > 50000;"
        Question: "Find products with total sales quantity exceeding 1000." 
        SQL Query:"SELECT productCode, SUM(quantityOrdered) AS totalQuantity FROM orderdetails GROUP BY productCode HAVING SUM(quantityOrdered) > 1000;"
        Question: "Find the highest payment amount made by any customer."
            SQL Query: "WITH MaxPayment AS (
                SELECT MAX(amount) AS maxAmount
                FROM payments
            )
            SELECT maxAmount
            FROM MaxPayment;"
        Question: "Get the total sales amount by product line."
        SQL Query:"WITH ProductSales AS (
            SELECT products.productLine, SUM(orderdetails.priceEach * orderdetails.quantityOrdered) AS totalSales
            FROM products
            JOIN orderdetails ON products.productCode = orderdetails.productCode
            GROUP BY products.productLine
        )
        SELECT productLine, totalSales
        FROM ProductSales;"
        Question: "Retrieve the top 3 most expensive products in each product line."
        SQL Query:"SELECT productLine, productName, buyPrice
        FROM (
            SELECT productLine, productName, buyPrice,
                ROW_NUMBER() OVER (PARTITION BY productLine ORDER BY buyPrice DESC) AS rank
            FROM products
        ) ranked_products
        WHERE rank <= 3;"
        Question: "Calculate the running total of payments for each customer."
        SQL Query:"SELECT customerNumber, paymentDate, amount,
            SUM(amount) OVER (PARTITION BY customerNumber ORDER BY paymentDate) AS runningTotal
        FROM payments;"
        Question: "Rank customers based on their total payment amounts."
        SQL Query:"SELECT customerNumber, SUM(amount) AS totalPayments,
            RANK() OVER (ORDER BY SUM(amount) DESC) AS paymentRank
        FROM payments
        GROUP BY customerNumber; "
        Question: "List the total number of orders and total amount spent by each customer."
        SQL Query:"SELECT customers.customerNumber, customers.customerName, COUNT(orders.orderNumber) AS orderCount, SUM(orderdetails.priceEach * orderdetails.quantityOrdered) AS totalSpent
        FROM customers
        JOIN orders ON customers.customerNumber = orders.customerNumber
        JOIN orderdetails ON orders.orderNumber = orderdetails.orderNumber
        GROUP BY customers.customerNumber, customers.customerName;"
        Question: "Show the total quantity ordered for each product."
        SQL Query:"SELECT products.productCode, products.productName, SUM(orderdetails.quantityOrdered) AS totalQuantity
        FROM products
        JOIN orderdetails ON products.productCode = orderdetails.productCode
        GROUP BY products.productCode, products.productName; "
        Question: "Find the average order value for each customer."
        SQL Query:"SELECT customers.customerNumber, customers.customerName, AVG(orderdetails.priceEach * orderdetails.quantityOrdered) AS avgOrderValue
        FROM customers
        JOIN orders ON customers.customerNumber = orders.customerNumber
        JOIN orderdetails ON orders.orderNumber = orderdetails.orderNumber
        GROUP BY customers.customerNumber, customers.customerName;"
        Question: "Retrieve the top 3 customers based on total payments in each country."
        SQL Query:"SELECT country, customerName, totalPayments
        FROM (
            SELECT customers.country, customers.customerName, SUM(payments.amount) AS totalPayments,
                ROW_NUMBER() OVER (PARTITION BY customers.country ORDER BY SUM(payments.amount) DESC) AS rank
            FROM customers
            JOIN payments ON customers.customerNumber = payments.customerNumber
            GROUP BY customers.country, customers.customerName
        ) ranked_customers
        WHERE rank <= 3;"
        Question: "List employees and their total sales, ranking them within their office."
        SQL Query:"SELECT employees.officeCode, employees.firstName, employees.lastName, SUM(orderdetails.priceEach * orderdetails.quantityOrdered) AS totalSales,
            RANK() OVER (PARTITION BY employees.officeCode ORDER BY SUM(orderdetails.priceEach * orderdetails.quantityOrdered) DESC) AS salesRank
        FROM employees
        JOIN orders ON employees.employeeNumber = orders.salesRepEmployeeNumber
        JOIN orderdetails ON orders.orderNumber = orderdetails.orderNumber
        GROUP BY employees.officeCode, employees.firstName, employees.lastName;"
        Question: "Calculate the cumulative sales for each product over time."
        SQL Query:"SELECT productCode, orderDate, quantityOrdered,
            SUM(quantityOrdered) OVER (PARTITION BY productCode ORDER BY orderDate) AS cumulativeSales
        FROM orderdetails
        JOIN orders ON orderdetails.orderNumber = orders.orderNumber; "
        Question: "List the total number of orders and total sales amount for each employee."
        SQL Query:"WITH EmployeeSales AS (
            SELECT employees.employeeNumber, employees.firstName, employees.lastName, COUNT(orders.orderNumber) AS orderCount, SUM(orderdetails.priceEach * orderdetails.quantityOrdered) AS totalSales
            FROM employees
            JOIN orders ON employees.employeeNumber = orders.salesRepEmployeeNumber
            JOIN orderdetails ON orders.orderNumber = orderdetails.orderNumber
            GROUP BY employees.employeeNumber, employees.firstName, employees.lastName
        )
        SELECT employeeNumber, firstName, lastName, orderCount, totalSales
        FROM EmployeeSales;"
        
        Your turn:
        
        Question: {question}
        SQL Query:
        """
    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatGroq(model="llama3-70b-8192", temperature=0)
  
    def get_schema(_):
        #print(db.get_table_info())
        return db.get_table_info()
    
    def get_dbdialect(_):
        #print(db.dialect)
        return db.dialect
    
    
    return (
    RunnablePassthrough.assign(schema=get_schema) |
    RunnablePassthrough.assign(db_dialect_detail=get_dbdialect) |
     prompt
    | llm
    | StrOutputParser()
  )


def get_sql_chain_example_shot(db):
    
    llm = ChatGroq(model="llama3-70b-8192", temperature=0)
    print("Creating chain")
    #print(final_prompt.format(input="How many products are there?"))
    generate_query = create_sql_query_chain(llm, db,final_prompt)
    def get_schema(_):
        #print(db.get_table_info())
        return db.get_table_info()
    
    def get_dbdialect(_):
        #print(db.dialect)
        return db.dialect
    
    chain=(RunnablePassthrough.assign(schema=get_schema) |
    RunnablePassthrough.assign(db_dialect_detail=get_dbdialect) |
    generate_query | StrOutputParser())
    
    return chain



if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
      AIMessage(content="Hello! I'm a SQL assistant. I can help you write queries."),
    ]


load_dotenv()

def execute_query(query, db):
    try:
        result = db.run(query, fetch='cursor')
        result1 = result.fetchall()
        df = pd.DataFrame(result1)
        df.index = df.index + 1
        return  df
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

st.title(" Natural language to SQL")
with st.sidebar:
    st.subheader("Settings")
    st.write("Connect to the database and start chatting.")
    
    st.text_input("Host", value="localhost", key="Host")
    st.text_input("Port", value="3306", key="Port")
    st.text_input("User", value="root", key="User")
    st.text_input("Password", type="password", value="admin1234", key="Password")
    st.text_input("Database", value="classicmodels", key="Database")
    
    if st.button("Connect"):
        with st.spinner("Connecting to database..."):
            db = init_database(
                st.session_state["User"],
                st.session_state["Password"],
                st.session_state["Host"],
                st.session_state["Port"],
                st.session_state["Database"]
            )
            st.session_state.db = db
            if (st.session_state.db is None):
                st.error("Connection failed. Please check your settings and try again.")
            else:
                st.success("Connected to database!")
if "db" in st.session_state and st.session_state.db is not None:    
    for message in st.session_state.chat_history:
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.markdown(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.markdown(message.content)

    user_query = st.chat_input("Type a message...")
    if user_query is not None and user_query.strip() != "":
        st.session_state.chat_history.append(HumanMessage(content=user_query))           

        with st.chat_message("Human"):
            st.markdown(user_query)
        
        with st.spinner("Generating response..."):
            with st.chat_message("AI"):
                #get_sql_chain= get_sql_chain_example_shot(st.session_state.db)
                chain=get_sql_chain_example_shot(st.session_state.db)
                response=chain.invoke({"input": user_query,"top_k":5,"table_info":"some table","question":user_query,
                                    "chat_history":st.session_state.chat_history})
                st.markdown(f"```sql\n{response}\n```")
                df = execute_query(response, st.session_state.db)

                st.dataframe(df)

            st.session_state.chat_history.append(AIMessage(content=response))

else:
    st.warning("Please connect to the database to start chatting.")