# Redshift & MySQL 性能对比实验

## 实验目的

提供 Redshift 和 RDS MySQL 在千万级数据中执行联表查询的性能对比。

[![Image link china](assets/RedShift_MySQL/ChinaRegion.png)](https://console.amazonaws.cn/cloudformation/home?region=cn-north-1#/stacks/new?stackName=RedshiftvsRDS&templateURL=https://s3.cn-north-1.amazonaws.com.cn/redshift-rds/RDSvsRedshift.yaml) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[![Image link global](assets/RedShift_MySQL/GlobalRegion.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=RedshiftvsRDS&templateURL=https://s3.amazonaws.com/redshift-rds/RDSvsRedshift.yaml)

## 涉及组件

- EC2
- RedShift
- RDS
- S3
- VPC

## 实验步骤

> **重要**
>
> 本实验默认您已经拥有了 AWS 账户并创建了 IAM 用户
>
> 若未执行以上设置，可参考[这里](https://docs.aws.amazon.com/zh_cn/AWSEC2/latest/UserGuide/get-set-up-for-amazon-ec2.html#sign-up-for-aws)

### 配置 VPC

新建 VPC 安全组，具体步骤参考[适用于 Amazon VPC 的 IPv4 入门](https://docs.aws.amazon.com/zh_cn/AmazonVPC/latest/UserGuide/getting-started-ipv4.html#getting-started-create-security-group)

将安全组的**入站规则**设置为

- **Type**: ALL Traffice
- **Protocol**: ALL
- **Port Range**: ALL
- **Source**: 选择 **Custom IP**，然后键入 `0.0.0.0/0`。

> **重要**
>
> 除演示之外，建议不要使用 0.0.0.0/0，因为它允许从 Internet 上的任何计算机进行访问。在实际环境中，您需要根据自己的网络设置创建入站规则。

### 配置 RedShift

1.  为 Amazon Redshift 创建 IAM 角色

   - 登录 AWS 管理控制台 并通过以下网址打开 IAM 控制台 <https://console.aws.amazon.com/iam/>。
   - 在左侧导航窗格中，选择 **Roles**。 
   - 选择 **Create role**
   - 在 **AWS Service** 组中，选择 **Redshift**。 
   - 在 **Select your use case** 下，选择 **Redshift - Customizable**，然后选择 **Next: Permissions**。 
   - 在 **Attach permissions policies** 页面上，选择 **AdministratorAccess**，然后选择 **Next: Review**。 
   - 对于 **Role name**，为您的角色键入一个名称。在本教程中，请键入 `myRedshiftRole`。 
   - 检查信息，然后选择 **Create Role**。 
   - 选择新角色的角色名称。
   - 将 **Role ARN** 复制到您的剪贴板 — 此值是您刚刚创建的角色的 Amazon 资源名称 (ARN)。在之后的实验中（**导入数据到 RedShift**），将会使用到该值。 

2. 登录 AWS 管理控制台 并通过以下网址打开 Amazon Redshift 控制台：<https://console.aws.amazon.com/redshift/> 。

3. 在主菜单中，选择您要在其中创建群集的区域。在本教程中，请选择 **美国西部（俄勒冈）**。 ![](assets/RedShift_MySQL/rs-gsg-aws-region-selector.png)


   . 在 Amazon Redshift 仪表板上，选择 **Launch Cluster**。									“Amazon Redshift Dashboard”如下所示!![rs-gsg-clusters-launch-cluster-10.png](assets/RedShift_MySQL/rs-gsg-clusters-launch-cluster-10.png)

4. 在“Cluster Details”页面上，输入下列值，然后选择 **Continue**：

   - **Cluster Identifier**：键入 `rs-vs-mysql`。                                     
   - **Database Name**：将此框留空。Amazon Redshift 将会创建一个名为 `dev` 的默认数据库。                                     
   - **Database Port**：键入数据库将接受连接的端口号。您应该在本教程的先决条件步骤确定了端口号。在启动群集之后便无法更改端口号，因此请确保您知道防火墙中的一个开放端口号，这样才能从 SQL                                        客户端工具连接到群集中的数据库。                                     
   - **Master User Name**：键入 `masteruser`。在群集可供使用之后，您将使用此用户名和密码连接到您的数据库。                                     
   - **Master User Password** 和 **Confirm Password**：为主用户账户键入密码。

   ![](assets/RedShift_MySQL/conf-rs.jpg)

5. 在“Node Configuration”页面上，选择下列值，然后选择 **Continue**：

   - **Node Type**：**dc1.large**
   - **Cluster Type**：**Multi Node**
   - **Number of compute nodes**：**2**

   ![](assets/RedShift_MySQL/conf-rs-nodes.jpeg)

6. 在“**Additional Configuration**”页面上，

   - **Choose a VPC**：选择您在**配置 VPC**这一步骤中创建的安全组所对应的 VPC
   - **Publicly Accessible**：**Yes** 
   - **VPC Security Groups**：选择您在**配置 VPC**这一步骤中创建的安全组
   - **AvailableRoles**： 选择**myRedshiftRole**
   - **其他选项**采用**默认**选项即可

   然后选择**Continue**。

7. 在“Review”页面上，查看您进行的选择，然后选择 **Launch Cluster**。 

### 配置 RDS

1. 登录 AWS 管理控制台 并通过以下网址打开 Amazon RDS 控制台：<https://console.aws.amazon.com/rds/>。 

2. 在 Amazon RDS 控制台的右上角，选择您要在其中创建数据库实例的区域。这里为保证与之前创建 RedShift 的区域相同。 

3. 在导航窗格中，选择**实例**。 

4. 选择**启动数据库实例**。**启动数据库实例向导**在**选择引擎**页面打开。![](/conf-rds.jpeg)

5. 选择 **MySQL**，然后选择**下一步**。

6. **选择使用案例**页面询问您是否计划使用所创建的数据库实例进行生产。选择 **开发/测试**，然后选择 **下一步** 。  

7. 在**指定数据库详细信息**页面上，指定数据库实例信息。选择下列值，然后选择 **下一步**。 

   - **数据库实例类**：db.r4.xlarge
   - **存储类型**：预置 IOPS
   - **预置 IOPS**：1000
   - **数据库实例标识符**：键入 `rs-vs-mysql`。 
   - **主用户名**：键入 `masteruser`。 
   - **主密码**和**确认密码**：键入您的密码
   - **其他设置保持默认**：

   ![](assets/RedShift_MySQL/conf-rds-mysql.jpeg)![](assets/RedShift_MySQL/conf-rds-mysql-2.jpg)

8. 在**配置高级设置**页面上，提供 RDS 启动 MySQL 数据库实例所需的其他信息。选择下列值，然后选择 **下一步**。

   - **Virtual Private Cloud (VPC)**：选择您在**配置 VPC**这一步骤中创建的安全组所对应的 VPC
   - **公开可用性**：是
   - **VPC安全组**：选择现有 VPC 安全组，并且选择**配置 VPC**这一步骤中创建的安全组
   - **数据库名称**：键入`dbname`
   - **备份保留期**：1 天
   - **其他请选择默认**

### 配置 EC2

1. 启动实例

   - 打开 Amazon EC2 控制台 <https://console.aws.amazon.com/ec2/>。选择您要在其中创建EC2实例的区域。这里为保证与之前创建 RedShift、RDS 的区域相同。 

   - 从控制台控制面板中，选择 **启动实例**。

   - **Choose an Amazon Machine Image (AMI)** 页面显示一组称为 *Amazon 系统映像 (AMI)* 的基本配置，作为您的实例的模板。选择 Amazon Linux AMI 2 的 HVM 版本 AMI。 

   - 在**选择实例类型** 页面上，您可以选择实例的硬件配置。选择 `t2.small` 类型 

   - 在**配置实例详细信息**页面上，自动分配公有 IP 选择**启用**，其他选择默认

   - 在**配置安全组**页面选择**选择一个现有的安全组**，并在表格中选择**配置 VPC**这一步骤中创建的安全组

   - 在**审核**页面选择**启动**

   - 当系统提示提供密钥时，选择 **选择现有的密钥对**，然后选择合适的密钥对。若没有创建密钥对，请参考[创建密钥对](https://docs.aws.amazon.com/zh_cn/AWSEC2/latest/UserGuide/get-set-up-for-amazon-ec2.html#create-a-key-pair)

     准备好后，选中确认复选框，然后选择 **启动实例**。  

2. 连接到 EC2

   请参考[使用 SSH 连接到 Linux 实例](https://docs.aws.amazon.com/zh_cn/AWSEC2/latest/UserGuide/AccessingInstancesLinux.html)

3. 在实例中安装 MySQL

   **在连接到 EC2 实例后**，依次输入以下命令，在实例中安装 MySQL

   ```
   wget http://repo.mysql.com/mysql-community-release-el6-5.noarch.rpm
   
   sudo rpm -ivh mysql-community-release-el6-5.noarch.rpm
   
   sudo yum install mysql-community-server -y
   ```

4. 在实例中安装 psql 工具

   **在连接到 EC2 实例后**，输入以下命令，在实例中安装 psql

   ```
   sudo yum install postgresql-server -y
   ```

### 导入数据到 RDS

1. 切换目录

   输入命令

   ```
   cd ~
   ```

2. 通过 AWS 命令行界面（CLI）下载数据

   AWS CLI 已经预安装在了 Amazon Linux AMI 上，但您仍需要进行相应的配置，详情可参考[配置 AWS CLI](https://docs.aws.amazon.com/zh_cn/cli/latest/userguide/cli-chap-getting-started.html)

   在 EC2 中配置完成 AWS CLI 后，输入以下命令拷贝测试数据
   - Global
   ```
   aws s3 cp s3://rs-vs-rds/test_date/2006.csv 2006.csv
   
   aws s3 cp s3://rs-vs-rds/test_date/2007.csv 2007.csv
   
   aws s3 cp s3://rs-vs-rds/test_date/2008.csv 2008.csv
   ```
   - 中国区
   ```
   aws s3 cp s3://rs-vs-rds/2006.csv 2006.csv --source-region cn-northwest-1 --region <your region>
   
   aws s3 cp s3://rs-vs-rds/2006.csv 2007.csv --source-region cn-northwest-1 --region <your region>
   
   aws s3 cp s3://rs-vs-rds/2006.csv 2008.csv --source-region cn-northwest-1 --region <your region>
   ```
   
3. 连接到 RDS

   参考[与运行 MySQL 数据库引擎的数据库实例连接](https://docs.aws.amazon.com/zh_cn/AmazonRDS/latest/UserGuide/USER_ConnectToInstance.html)

4. 创建表格

   输入命令

   ```
   use dbname;
   ```

   ```
   CREATE TABLE demobigtable (
   	Year integer,
   	Month integer,
   	DayofMonth integer,
   	DayOfWeek varchar(255),
   	DepTIme varchar(255),
   	CRSDepTime varchar(255),
   	ArrTime varchar(255),
   	CRSArrTime varchar(255),
   	UniqueCarrier varchar(255),
   	FlightNum varchar(255),
   	TailNum varchar(255),
   	ActualElapsedTime varchar(255),
   	CRSElapsedTime varchar(255),
   	AirTime varchar(255),
   	ArrDelay varchar(255),
   	DepDelay varchar(255),
   	Origin varchar(255),
   	Dest varchar(255),
   	Distance varchar(255),
   	TaxiIn varchar(255),
   	TaxiOut varchar(255),
   	Cancelled varchar(255),
   	CancellationCode varchar(255),
   	Diverted varchar(255),
   	CarrierDelay varchar(255),
   	WeatherDelay varchar(255),
   	NASDelay varchar(255),
   	SecurityDelay varchar(255),
   	LateAircraftDelay varchar(255)
   ) ;
   ```

5. 加载数据

    执行 SQL 语句

    ```
    load data local infile '2006.csv'
    into table demobigtable
    fields terminated by ','
    lines terminated by '\n' 
    IGNORE 1 LINES;
       
    load data local infile '2007.csv'
    into table demobigtable
    fields terminated by ','
    lines terminated by '\n' 
    IGNORE 1 LINES;
       
    load data local infile '2008.csv'
    into table demobigtable
    fields terminated by ','
    lines terminated by '\n' 
    IGNORE 1 LINES;
    ```

### 测试 RDS

输入命令

```
SELECT a.Year,a.Month,a.DayofMonth,a.FlightNum,a.TailNum
FROM
      (SELECT Year,Month,DayofMonth,FlightNum,TailNum 
      FROM demobigtable 
      GROUP BY Year,Month,DayofMonth,FlightNum,TailNum) 
      AS a
LIMIT 10;
```

获取 RDS 实验结果 

### 导入数据到RedShift

1. 输入以下命令退出 RDS，若您之前已经退出了 RDS，请忽略该步骤。

   ```
   exit；
   ```

2. 连接到 RedShift

   参考[使用 psql 工具连接到您的群集](https://docs.aws.amazon.com/zh_cn/redshift/latest/mgmt/connecting-from-psql.html)

3. 创建表格

   ```
   CREATE TABLE demobigtable (
   	Year integer,
   	Month integer,
   	DayofMonth integer,
   	DayOfWeek varchar(255),
   	DepTIme varchar(255),
   	CRSDepTime varchar(255),
   	ArrTime varchar(255),
   	CRSArrTime varchar(255),
   	UniqueCarrier varchar(255),
   	FlightNum varchar(255),
   	TailNum varchar(255),
   	ActualElapsedTime varchar(255),
   	CRSElapsedTime varchar(255),
   	AirTime varchar(255),
   	ArrDelay varchar(255),
   	DepDelay varchar(255),
   	Origin varchar(255),
   	Dest varchar(255),
   	Distance varchar(255),
   	TaxiIn varchar(255),
   	TaxiOut varchar(255),
   	Cancelled varchar(255),
   	CancellationCode varchar(255),
   	Diverted varchar(255),
   	CarrierDelay varchar(255),
   	WeatherDelay varchar(255),
   	NASDelay varchar(255),
   	SecurityDelay varchar(255),
   	LateAircraftDelay varchar(255)
   ) ;
   ```

4. 加载数据

   请将以下 COPY 命令中的*<iam-role-arn>*替换为您的角色 ARN，输入至 psql 命令行中
   - Global
   ```
   copy demobigtable from 's3://rs-vs-rds/test_date/2006.csv' 
   credentials 'aws_iam_role=<iam-role-arn>'
   delimiter ',' 
   IGNOREHEADER 1
   ACCEPTINVCHARS;
   
   copy demobigtable from 's3://rs-vs-rds/test_date/2007.csv' 
   credentials 'aws_iam_role=<iam-role-arn>'
   delimiter ',' 
   IGNOREHEADER 1
   ACCEPTINVCHARS;
   
   copy demobigtable from 's3://rs-vs-rds/test_date/2008.csv' 
   credentials 'aws_iam_role=<iam-role-arn>'
   delimiter ',' 
   IGNOREHEADER 1
   ACCEPTINVCHARS;
   ```
   - 中国区
   ```
   copy demobigtable from 's3://rs-vs-rds/2006.csv' 
   credentials 'aws_iam_role=<iam-role-arn>'
   delimiter ',' 
   IGNOREHEADER 1
   ACCEPTINVCHARS;
   
   copy demobigtable from 's3://rs-vs-rds/2007.csv' 
   credentials 'aws_iam_role=<iam-role-arn>'
   delimiter ',' 
   IGNOREHEADER 1
   ACCEPTINVCHARS;
   
   copy demobigtable from 's3://rs-vs-rds/2008.csv' 
   credentials 'aws_iam_role=<iam-role-arn>'
   delimiter ',' 
   IGNOREHEADER 1
   ACCEPTINVCHARS;
   ```

### 测试 RedShift

1. 开启 sql 时间记录功能

   ```
   \timing on
   ```

2. 执行 SQL 语句

   ```
   SELECT a.Year,a.Month,a.DayofMonth,a.FlightNum,a.TailNum
   FROM
         (SELECT Year,Month,DayofMonth,FlightNum,TailNum 
         FROM demobigtable 
         GROUP BY Year,Month,DayofMonth,FlightNum,TailNum) 
         AS a
   LIMIT 10;
   ```

## 实验结果

### RDS 实验结果

![](assets/RedShift_MySQL/result-rds-3.jpg)

### RedShift 实验结果

![](assets/RedShift_MySQL/result-rs-3.jpg)
