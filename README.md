EmpressX
========
分布式设计， 
Empress服务器(django)负责数据的管理控制中心，
分布式的Retinue服务器（分为Web和App）作为客户端(django+celery)，接受Empress请求触发变动流程。
