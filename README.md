# quickstart-guide

**Guide: 将MongoDB部署到现有VPC**

**步骤一：加载Quick Start**

1. 在您的 AWS 控制台中选择 AWS CloudFormation ，开始部署 MangoDB 集群。

![Image one](https://github.com/xyG67/quickstart-guide/blob/xy/IMG/01.png)


2. 在配置前，请确保您的VPC在不同可用区中有两个公有子网和三个私有子网（可选），以及 DHCP 选项中配置的域名选项，如 [Amazon VPC](http://docs.aws.amazon.com/AmazonVPC/latest/UserGuide/VPC_DHCP_Options.html) [文档](http://docs.aws.amazon.com/AmazonVPC/latest/UserGuide/VPC_DHCP_Options.html)中所述。
3. 私有子网需配置 NAT 网关或 NAT 实例以用于出站 Internet 连接，并需创建堡垒主机及其关联的安全组以实现入站 SSH 访问。(请参阅 [Amazon VPC](https://aws.amazon.com/quickstart/architecture/vpc/) [快速入门](https://aws.amazon.com/quickstart/architecture/vpc/)设置VPC， [Linux](https://aws.amazon.com/quickstart/architecture/linux-bastion/) [堡垒主机快速入门](https://aws.amazon.com/quickstart/architecture/linux-bastion/)设置堡垒主机。)
4. 检查导航栏右上角显示的所在区域，根据需要进行更改。
5. 在 **Select Template** 页面上，保留模板 URL 的默认设置，然后选择 **Next** 。

![Image two](https://github.com/xyG67/quickstart-guide/blob/xy/IMG/02.png)


6. 在 **Specify Details** 页面上，更改堆栈名称（可选）。填写模板的参数，并仔细检查默认设置中的其他参数，根据需要进行更改（见下表）。完成后选择 **Next** 进入下一步。

**选项**** 1：用于将 **** MongoDB **** 部署到现有 **** VPC **** 的参数**

_网络配置__:_

| 参数标签 | 参数名称 | 默认值 | 说明 |
| --- | --- | --- | --- |
| VPC | VPC | _需要输入_ | 用于部署MongoDB 群集的 VPC的ID (例如，vpc-0343606e)。 |
| 主节点子网 | PrimaryNodeSubnet | _需要输入_ | 要部署主MongoDB到节点的 VPC 中现有子网的 ID (例如，subnet-a0246dcd)。 |
| Secondary0 节点子网 | Secondary0NodeSubnet | _需要输入_ | 要部署副本集中第一个辅助 MongoDB 节点的 VPC 中现有子网的 ID。有关预期置放的更多信息，请参阅 [架构](https://docs.aws.amazon.com/zh_cn/quickstart/latest/mongodb/architecture.html)部分。 |
| Secondary1 节点子网 | Secondary1NodeSubnet | _需要输入_ | 要部署副本集中第二个辅助 MongoDB 节点的 VPC 中现有子网的 ID。有关预期置放的更多信息，请参阅 [架构](https://docs.aws.amazon.com/zh_cn/quickstart/latest/mongodb/architecture.html)部分。 |
| 堡垒安全组 ID | BastionSecurityGroupID | _需要输入_ | 现有 VPC 中防御安全组的 ID (例如 sg-7f16e910)。 |

_安全配置：_

| 参数标签 | 参数名称 | 默认值 | 说明 |
| --- | --- | --- | --- |
| 密钥名称 | KeyPairName | _需要输入_ | 公有/私有密钥对，使您能够在实例启动后安全地与它连接。|

_MongoDB 数据库配置：_

| 参数标签 | 参数名称 | 默认值 | 说明 |
| --- | --- | --- | --- |
| 群集副本集计数 | ClusterReplicaSetCount | 1 | 副本集成员的数量。选择 1 或 3。 |
| Iops | Iops | 100 | 如果选择io1卷类型，需设置为 EBS 卷的 IOPS，否则将忽略此设置。 |
| MongoDB 版本 | MongoDBVersion | 3.4 | 将部署的 MongoDB 的版本。|
| MongoDB 管理员用户名 | MongoDBAdminUsername | 管理员 | MongoDB 管理账户的用户名。 |
| MongoDB 管理员密码 | MongoDBAdminPassword | _需要输入_ | 您的 MongoDB 数据库密码。您可以输入由以下字符组成的 8-32 个字符的字符串：[A-Za-z0-9\_@-]。 |
| 节点实例类型 | NodeInstanceType | m4.large | MongoDB 节点的 EC2 实例类型。 |
| 副本分区索引 | ReplicaShardIndex | 0 | 此副本集的分区索引。有关分区索引的信息，请参阅 [MongoDB](https://docs.mongodb.com/v3.0/core/sharding-shard-key-indexes/) [文档](https://docs.mongodb.com/v3.0/core/sharding-shard-key-indexes/) |
| 卷大小 | VolumeSize | 400 | 挂载到 MongoDB 节点的 Amazon EBS (数据) 卷的大小 (以 GiB 为单位)。 |
| 卷类型 | VolumeType | gp2 | 挂载到 MongoDB 节点 (gp2或io1) 的 Amazon EBS (数据) 卷的卷类型。 |

_AWS 快速入门配置：_

| 参数标签 | 参数名称 | 默认值 | 说明 |
| --- | --- | --- | --- |
| 快速入门 S3 存储桶名称 | QSS3BucketName | quickstart-reference | 安装快速入门模板和脚本的 S3 存储桶。如果您希望自定义或扩展快速入门，请使用该参数来指定为该副本创建的 S3 存储桶名称。存储桶名称可包含数字、小写字母、大写字母和连字符，但不得包括连字符开头或结尾。 |
| 快速入门 S3 键前缀 | QSS3KeyPrefix | mongodb/latest/ | [S3](http://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html) [键名称前缀](http://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html)，用于模拟快速入门资产的副本的文件夹 (如果您决定自定义或扩展快速入门)。此前缀可以包含数字、小写字母、大写字母、连字符和正斜杠。它不赢以连字符 (-) 开头或结尾。 |

7. 在 **Options** 页面上，您可以为堆栈中的资源 [指定标签](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html) (键/值对) 并 [设置高级选项](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-console-add-tags.html)。在完成此操作后，选择 **Next** 。
8. 在 **Review** 页面上，查看并确认模板设置。选择 **Capabilities** 下的复选框，以确认模板将创建 IAM 资源。


![Image](https://github.com/xyG67/quickstart-guide/blob/xy/IMG/03.png)


9. 选择 **Create** 以部署堆栈。
10. 监控堆栈的状态。当状态为 **CREATE\_COMPLETE** 时 (如图4所示)，表示 MongoDB 群集已淮备就绪。


![Image](https://github.com/xyG67/quickstart-guide/blob/xy/IMG/04.png)


**步骤二 连接到 MongoDB 节点**

当 AWS CloudFormation 模板成功创建堆栈后，您需要通过AWS账户中已安装的软件运行MongoDB 节点。请使用 SSH 连接到堡垒主机实例，以连接到任一 MongoDB 节点，即在 Amazon EC2 控制台中，选择该堡垒实例，然后选择 **Connect** 。


![Image](https://github.com/xyG67/quickstart-guide/blob/xy/IMG/05.png)


使用 SSH 连接到堡垒主机实例后，您可以通过类似的方式连接到任何 MongoDB 节点 (选择节点，然后选择 **Connect** 以查找 SSH 命令)。

**重要提示**

您需要私有密钥 (.pem) 文件才能连接到 MongoDB 节点。请将私有密钥 (.pem) 文件复制到堡垒主机实例中，例如：

        scp –i mykey.pem mykey.pem ec2-user@Bastion-public-ip:/home/ec2-user/mykey.pem

请注意，所有 MongoDB 节点均通过 IAM 角色来启动，该角色需要权限包括：创建和删除 Amazon DynamoDB 表、访问 Amazon Simple Storage Service (Amazon S3)、创建和删除 Amazon EC2 实例等。您可以使用 IAM 控制台修改该策略。有关 IAM 角色的详细信息请参阅 AWS 文档中的 [使用](http://docs.aws.amazon.com/IAM/latest/UserGuide/role-usecase-ec2app.html) [IAM](http://docs.aws.amazon.com/IAM/latest/UserGuide/role-usecase-ec2app.html) [角色向](http://docs.aws.amazon.com/IAM/latest/UserGuide/role-usecase-ec2app.html) [Amazon EC2](http://docs.aws.amazon.com/IAM/latest/UserGuide/role-usecase-ec2app.html) [上运行的应用程序委托权限](http://docs.aws.amazon.com/IAM/latest/UserGuide/role-usecase-ec2app.html)。
