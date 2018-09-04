# 功能模块说明
# author ziling
# date 2018-07-02

### 功能： 该脚本是云识图大数据平台中将人脸报警数据和车辆滞留情况的信息同步到大数据平台数据库中。
### 运行环境 python3.5 ubuntu14.04， 大数据平台网站中的内容。
### 本功能主要包括以下几个方面
1. 脚本功能syncCarData, syncFaceData
2. 脚本监控并重启的shell脚本，carSyncDispatchFunction.sh
3. 为系统添加自启动的方式。
4. 数据库的配置信息及时间持久化的文本
另外：
4. 针对功能模块进行的单元测试，集成测试，形成一个范例。
5. 完整交互整个功能。

步骤三：
1. 添加service并设置开机自起
2. 添加软连接
sudo ln -s  ~/Corsface/readme/assist/carSyncDispatchFunction.sh /etc/init.d/carSyncDispatchFunction
3. 添加自启动
sudo update-rc.d Corsface defaults

### 注，其中一些路径的安排需要自行更正。