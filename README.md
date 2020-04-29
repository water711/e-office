# e-office
泛微OA流程-自动化测试

## 一、准备环境
* Python：3.7  
* 浏览器：chrome v81.0.4044.129  
* chromedriver：v81.0.4044.69  
* 泛微OA：v10.0_20180903

安装selenium库  
`pip install selenium` 

[点击下载chromedriver](http://npm.taobao.org/mirrors/chromedriver/)  
  
  
## 二、目录文件说明
config/ElePath.py：存放xpath相关变量  

control_id目录：存放流程表单必填选项（文件以流程ID命名）  

例如：流程ID为70，在control_id目录下新建70.txt文件  

文件内容:

| 表单控件类型 | 控件id | 点击后的xpath路径
| ---- | ---- | ---- |
| text | DATA_5 |
| choice | DATA_4_4_2 | /html/body/div[11]/div[5] |











