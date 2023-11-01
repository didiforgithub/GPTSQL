from django.shortcuts import render
import json
from django.shortcuts import render,redirect
from django.views import View
from django.http import HttpResponse,JsonResponse
from .import models
from django.db import connection
from django.db.models import Count
import os
import openai
from dotenv import load_dotenv
import requests
from . import tools

# API-1 获取数据库表与属性信息

def get_table_name(request):
    if request.method == 'GET':
        result = tools.table_information_get()

    return JsonResponse(result,safe=False)



# API-2 自然语言转SQL语句（API-2key版本，无需给服务器配梯子）
def gpt_sql(request):
    if request.method == 'POST':

        json_str_bytes = request.body
        json_str = json_str_bytes.decode()
        question_dict = json.loads(json_str,strict=False)

        questions = question_dict['question']
        prompt = "You need to design a system that can convert natural language into SQL statements. This system should be capable of parsing natural language input from the user, converting it into an SQL query statement, and returning the corresponding results. To ensure the accuracy of the output SQL statement, you must provide a JSON-formatted text in the request containing the keywords and meanings present in the natural language. When outputting the SQL statement, convert the natural language text with similar meanings to the text in JSON format to ensure the SQL statement's accuracy. Finally, your system should return a string starting with 'SQL you need is:' followed by the generated SQL statement. Do not appear a newline symbol in the return"
        prompt = prompt + "JSON is" + str(tools.table_information_get())
        
        url = "https://openai.api2d.net/v1/chat/completions"
        headers = {
            'Content-Type': 'application/json',
            'Authorization':  
        }
        data = {"model": "gpt-3.5-turbo","messages": 
                [{"role":"system","content":prompt},
                {"role":"assistant","content":"Here's what I need" + questions}]
                }

        response = requests.post(url, headers=headers, json=data)
        GET_sql = response.json()
    # 访问choices中包含的content
        content = GET_sql['choices'][0]['message']['content']
        return JsonResponse(content,safe = False)

# API-2 自然语言转SQL语句（OpenAI版本，需给服务器配梯子）
def gpt_sql_OPenai(request):
    if request.method == 'POST':

        json_str_bytes = request.body
        json_str = json_str_bytes.decode()
        question_dict = json.loads(json_str,strict=False)

        questions = question_dict['question']
        prompt = "You need to design a system that can convert natural language into SQL statements. This system should be capable of parsing natural language input from the user, converting it into an SQL query statement, and returning the corresponding results. To ensure the accuracy of the output SQL statement, you must provide a JSON-formatted text in the request containing the keywords and meanings present in the natural language. When outputting the SQL statement, convert the natural language text with similar meanings to the text in JSON format to ensure the SQL statement's accuracy. Finally, your system should return a string starting with 'SQL you need is:' followed by the generated SQL statement. Do not appear a newline symbol in the return"
        # prompt = "你需要设计一个用于将自然语言转化为SQL语句的系统。这个系统需要能够解析用户的自然语言输入，将其转化为SQL查询语句，并返回相应的结果。为了确保输出的SQL语句是准确的，你需要在请求中提供一个JSON格式的文本，其中包含了自然语言中所涉及的关键词和意义。在输出SQL语句时，请将自然语言中意义相近的文本转化为JSON格式中的文本，以确保SQL语句的准确性。最终，你的系统需要返回一个以'SQL you need is:'开头的字符串，后面紧跟着生成的SQL语句。"
        prompt = prompt + "JSON is" + str(tools.table_information_get())
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
            {"role":"system","content":prompt},
            {"role":"assistant","content":"Here's what I need" + questions}
        ]   
        )

#API2 11/1 更新Prompt
def gpt_sql_new(request):
    if request.method == 'POST':

        json_str_bytes = request.body
        json_str = json_str_bytes.decode()
        question_dict = json.loads(json_str,strict=False)

        question = question_dict['question']
        table_name = "SmartPension"
        table_information = str(tools.table_information_get())


        prompt = f"""
        You are a data scientist, you are good at convert natural language into SQL statements.
        The table's name is {table_name} and it has a structure {table_information}.
        You need to wrting SQL Statements to answer this question {question}.

        Response Format:
        You must respond in JSON format as described below:
        {
            "result": SQL Statement
        }

        Ensure the response can be parsed by Python json.loads
        """

        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
            {"role":"user","content":prompt}
        ]
        )
        return completion["choices"][1]["content"]

# API3 获取SQL语句后，执行语句，返回数据
def Info_get(request):
    if request.method == 'POST':

        json_str_bytes = request.body
        json_str = json_str_bytes.decode()
        SQL_dict = json.loads(json_str,strict=False)
        SQL = SQL_dict['SQL']

        result = tools.SQL_get(SQL)
        return JsonResponse(result,safe=False)

# API4 自然语言输入，数据输出，通过自然语言无感知获取数据
def zero_info_get(request):

    if request.method == 'POST':

        json_str_bytes = request.body
        json_str = json_str_bytes.decode()
        question_dict = json.loads(json_str,strict=False)

        questions = question_dict['question']
        print(questions)
        prompt = "You need to design a system that can convert natural language into SQL statements. This system should be capable of parsing natural language input from the user, converting it into an SQL query statement, and returning the corresponding results. To ensure the accuracy of the output SQL statement, you must provide a JSON-formatted text in the request containing the keywords and meanings present in the natural language. When outputting the SQL statement, convert the natural language text with similar meanings to the text in JSON format to ensure the SQL statement's accuracy.Please include only SQL statements in the returned results and no other information.Do not appear a newline symbol in the return.Do not return any text other than SQL statements!"
        prompt = prompt + "JSON is" + str(tools.table_information_get())
        
        url = "https://openai.api2d.net/v1/chat/completions"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer fk191879-6SnGzMicBhN0HOOoSM3DXvTpUHFKSXcL' 
        }

        data = {"model": "gpt-3.5-turbo","messages": 
	        [{"role":"system","content":prompt},
	        {"role":"assistant","content":f"""
            This is the information I need to query the database using SQL statements+ ```{questions}```"""}]
        }

        response = requests.post(url, headers=headers, json=data)
        GET_sql = response.json()
    # 访问choices中包含的content
        content = GET_sql['choices'][0]['message']['content']

        result = tools.SQL_get(content)
        return JsonResponse(result,safe=False)
