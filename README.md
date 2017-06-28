# spider
spider for 豆瓣读书 and 新榜


### 使用
1. 安装模块

`sudo pip install numpy`

`sudo pip install bs4`

`sudo pip install openpyxl`

`sudo pip install selenium`

`sudo pip install pyvirtualdisplay`

2.安装驱动

爬新榜时会使用浏览器模拟登陆，所以需要下载浏览器驱动，这里用的是火狐浏览器。

`brew install geckodriver`

3.启动

进入相应目录执行
`python XX.py`

执行完毕后会将数据生成到当前文件夹下的Excel表格下。