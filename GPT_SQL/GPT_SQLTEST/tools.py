from django.db import connection

# Tool 1 执行SQL语句获取表信息
def table_information_get():

    with connection.cursor() as cursor:
        cursor.execute("SELECT table_name, column_name FROM information_schema.columns WHERE table_schema = 'SmartPension';")
        rows = cursor.fetchall()

        result = {}
        for row in rows:
            table_name = row[0]
            column_name = row[1]
            if table_name not in result:
                result[table_name] = []
            result[table_name].append(column_name)
            
        result = remove_keys(result)
        final = []
        for k,y in result.items():
            a ={}
            a['label']= k 
            b = []
            for i in y:
                b.append({'label':i})
            a['children']= b
            final.append(a)

    return final

# Tool 2 去除Django中自带的属性表
def remove_keys(result):
    keys_to_remove = ["django_admin_log", "auth_group", "auth_group_permissions", "auth_permission", "auth_user", "auth_user_groups", "auth_user_user_permissions","django_content_type","django_migrations"]
    for key in keys_to_remove:
        result.pop(key, None)
    return result

# Tool 3 执行SQL语句获取表数据
def SQL_execute(SQL):
    with connection.cursor() as cursor:
            
        cursor.execute(SQL)
        # 获取列表名
        colname =[]
        for i in cursor.description:
            colname.append(i[0])
        rows = cursor.fetchall()
        result = []
        result.append(colname)
        for row in rows:
            result.append(row)
    return result

# 弃用工具
# def table_SQL():

#     with connection.cursor() as cursor:

#         rows = cursor.fetchall()
#         result = {}
#         for row in rows:
#             table_name = row[0]
#             column_name = row[1]
#             if table_name not in result:
#                 result[table_name] = []
#             result[table_name].append(column_name)
            
#             result = remove_keys(result)

#     return result