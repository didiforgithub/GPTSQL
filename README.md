# 业务语言查询数据库系统

项目使用Django restful framework 完成，启动方法如下：

```
cd GPT_SQL
pip install -r requirements.txt
python manage.py runserver
```
主要模块
1. Tools，与数据库相关的操作封装在这一模块中
2. Views，对外提供的API封装在这一模块中

对外提供的API主要是4个功能
1. 获取数据库表信息
2. 自然语言转SQL（Openai版本与非Openai版本）
3. SQL函数执行并返回结果
4. 自然语言直接执行查询数据

之后需要修改的话，主要是在2进行修改，需要写一个Prompt抽取业务流程

需要补充的部分，主要是
1. 知识库的baseid连接 —— 用户选中某个固定的base之后根据问题在这个知识库进行检索
2. 检索知识与数据知识的连接
3. 用户系统连接

