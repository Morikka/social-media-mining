# Province Analysis

`city_data_process` Group and count data by province

`ChinaMap` Visualize those data

`Prov_Analysis` Analysis those data

# Tweet Sentiment Analysis

`tweet` used to scraw data from twitter

`tf-idf` used to count the tf-idf weight of two documents

`tag_cloud` `tag_cloud_cat` `tag_cloud_dog` used to draw tag cloud picture for cat and dog

# Book Movie and Activity Analysis

analyzeFollow.py 分析豆瓣用户的粉丝，关注者及常去小组的数量，寻找相似度

getBookInfor.py “用户-偏好的书籍类型”表的数据准备，包含正规化处理

getDetails.py 针对每个用户，获取其最喜欢的100本书和电影的id

getFriends.py 针对每个用户，获取其粉丝，关注着及常去小组的数量

getMovieInfor.py “用户-偏好的电影类型”表的数据准备，包含正规化处理及机器学习算法的尝试性应用

getTags.py 针对每部电影和每本书籍，获取他们的类型和tag

getTimeStamps 针对猫和狗的小组，获取从创建开始到目前为止的帖子发布时间，分析社区活跃度

analyzeActivity.py: 由活跃度数据，绘制猫和狗小组的社区活跃度折线图

userIDCrawler.py 针对猫和狗的小组，获取每个小组中所有用户的用户id

CDPeopleDB.sqlit 包含CatPeople和DogPeople两张表，分别包含了猫和狗小组的所有用户