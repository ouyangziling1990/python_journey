1. 两个脚本应该写一起，方便控制。

2. 数据库重连机制，在数据库连接失败后主动尝试去重新连接。

3. 整个脚本的控制，采用shell脚本发现脚本失败，并再次启动该脚本。




above all; 
用最本源的数据库方式，采用触发器。
1. 不同数据库之间的同步
2. 表格的字段不一致问题。同步到另一个机器的另一个数据中。`
