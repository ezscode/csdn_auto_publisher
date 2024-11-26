# csdn_auto_publisher

csdn_auto_publisher 是一个 CSDN 自动发布脚本。

无需繁琐的配置，一页代码实现 自动登录、发布博文、定时发布等功能。

***

### requirements

本人电脑 Python 为 3.11.5，未在其他版本测试

依赖包版本： 

```shell
pip install pyperclip==1.9.0 
pip install selenium==4.26.1 
```



***

## 使用

1、输入你的账号密码 实现发布前的自动登录；

2、目前主要针对 markdown 格式进行发布，且提取第一行作为标题 

3、文章分类，需要输入已有的分类文本；标签也是必须的（一定等级才能自定义标签）；



***

### 简单发布示例

```python

# 简单发布一个文件
def test_simple_pub():
    file_path = '/Users/xx/Documents/xxx/tool.md' 
    article = Article(file_path) 
    article.tags = ['python'] 
    article.cover_img_path = '/Users/xx/Pictures/存图/exo-logo.png_b.png'
    article.categories = ['Python'] 
    # article.categories = ['Python'] 
    print('-- title : ', article.title) 
    # print(article.content) 
    ret = csdn_publisher(driver, article)
```

定时发布、发布整个文件夹 示例，详见脚本中的 `test_simple_pub`, `test_scheduled_pub`, `test_dir_pub` 方法。

***

### 注意事项

- 多篇文章发布，需要注意间隔，否则平台会提示`频繁操作` 而发布失败
- 定时发布，只能发布当前时间往后算 7 天内。



