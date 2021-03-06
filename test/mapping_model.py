#-- coding:UTF-8 --
import json
class User(object):
    def __init__(self,id,password,nickname,age):
        self.id = id # 用户ID
        self.password = password # 密码
        self.nickname = nickname # 昵称
        self.age = age # 年龄
class Comment(object):
    def __init__(self, id, user, text):
        self.id = id # 留言ID
        self.user = user # 用户ID
        self.text = text # 留言内容

def get_user(user_id):
    """ 返回用户对象的函数
    """
    # 实际开发时应该访问数据库
    user = User(id=user_id,password='hoge',nickname='tokibito',age=26)
    return user
def get_comment(comment_id):
    """ 返回留言对象的函数
    """
    # 实际开发时应该访问数据库
    comment = Comment(id=comment_id,user=get_user('bp12345'),text=u'Hello, world!')
    return comment

def mapping_user(user):
    """
        User 模型与API 的映射
    """
    return {'user_id': user.id, 'user_nickname': user.nickname}

def mapping_user_2(user):
    """
    User 模型与API 的映射2
    """
    return {'user_id': user.id,'user_nickname': user.nickname,'user_age': user.age}

def mapping_comment(comment):
    """
    Comment 模型与API 的映射
    """
    return {'user': mapping_user(comment.user), 'text': comment.text}
def api_user_json(user_id):
    """ 以JSON 格式返回用户数据的API
    """
    user = get_user(user_id) # 获取User 对象
    user_dict = mapping_user(user) # 映射到字典
    return json.dumps(user_dict, indent=2) # 以JSON 格式返回
def api_user_detail_json(user_id):
    """ 以JSON 格式返回用户详细数据的API
    """
    user = get_user(user_id) # 获取User 对象
    user_dict = mapping_user_2(user) # 映射到字典
    return json.dumps(user_dict, indent=2) # 以JSON 格式返回

def api_comment_json(comment_id):
    """ 
    以JSON 格式返回留言数据的API
    """
    comment = get_comment(comment_id) # 获取Comment 对象
    comment_dict = mapping_comment(comment) # 映射到字典
    return json.dumps(comment_dict, indent=2) # 以JSON 格式返回

def convert_user_to_json(user):
    """ 获取一个User 对象并返回JSON
    """
    #生成用于转换格式的字典对象
    user_dict = {
        'user_id': user.id, # 使用名为user_id 的键
        'user_nickname': user.nickname, # 使用名为user_nickname 的键
    }
    return json.dumps(user_dict) # 转换为JSON
def main():
    # 获取用户数据的JSON 并显示
    print("--- api_user_json ---")
    print(api_user_json('bp12345'))
    # 获取用户数据（详细）的JSON 并显示
    print("--- api_user_detail_json ---")
    print(api_user_detail_json('bp12345'))
    # 获取留言数据的JSON 并显示
    print("--- api_comment_json ---")
    print(api_comment_json('cm54321'))
if __name__ == '__main__':
    main()