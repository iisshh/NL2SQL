Create v env, python3 -m venv myenv

    * source myenv/bin/activate -a activate

Install mysql: port 3306
brew install mysql
mysql_secure_installation -> To set password
To start mysql now and restart at login:
  brew services start mysql
Or, if you don't want/need a background service you can just run:
  /opt/homebrew/opt/mysql/bin/mysqld_safe --datadir\=/opt/homebrew/var/mysql


* Indtalling dependencies:  pip install -r requirements.txt
* requirements.txt
* streamlit
* langchain
* langchain-community
* langchain-groq
* langchain-core
* mysql-connector-python
* groq
* langchain-groq
* python-dotenv
* to run the file:streamlit run app.py




Docker:
Install docker and create acc
create the docker file
run docker build -t nl2sql-streamlit-app . to create the docker image
access the container: docker exec -it <container_id> /bin/bash


