# Part 1: 使用SMS导入您的VM

本指导将逐步描述如何使用AWS Server Migration Service (SMS)服务，将您 VMware vSphere 的虚拟机自动迁移到 AWS 云。

### 步骤一  添加IAM用户

您可以选择在控制台添加IAM，步骤如下：

 - IAM 控制台中选择 Roles 和 Create new role。 
 - 在 Search role type 页面上，找到 SMS并选择 Select。 
 - 在 Attach Policy 页面上，选择 ServerMigrationServiceRole，然后选择 Next Step。 
 - 在 Set role name and review 页面上，键入 Role name。  
 - 选择 Create role。您现在应该能够在可用角色列表中看到该角色。 

### 步骤二 在 VMware 上安装服务器迁移连接器

本主题介绍设置 AWS SMS 以将 VM 从 VMware 迁移到 Amazon EC2 的步骤。此信息仅适用于本地 VMware 环境中的 VM。从 LAN 上的客户端计算机系统中完成以下步骤，以在 VMware 环境中设置 AWS 服务器迁移连接器。

##### 第一步：为 VMware 环境设置连接器

1.	设置您的 vCenter 服务账户。在vSphere Client点击Home->Role->Add Role创建一个 vCenter 用户。
2.	右击创建的用户，点击Edit Role，在 vCenter 中创建具有以下权限的角色：

     -	Datastore -> Browse datastore and Low level file operations (Datastore.Browse 和 Datastore.FileManagement) 
     -	Host -> Configuration -> System Management (Host.Config.SystemManagement) 
     -	vApp -> Export (VApp.Export) 
     -	Virtual Machine -> Snapshot management -> Create snapshot and Remove Snapshot (VirtualMachine.State.CreateSnapshot 和 VirtualMachine.State.RemoveSnapshot) 
     
     [![image 01](assets/SMS_vm-import/SMS01.png)]

3.	将此 vCenter 角色分配给连接器的服务账户以用于登录 vCenter，向此角色分配针对包含要迁移的 VM 的数据中心的传播权限。

##### 第二步：配置连接器

1.	在控制台中打开 AWS Server Migration，选择 Connectors->SMS Connector setup guide。
    [![image 01](assets/SMS_vm-import/SMS02.png)]
2.	在 AWS Server Migration Connector setup 页面上，选择 Download OVA 以下载适用于 VMware 环境的连接器。 
3.	在 vSphere 客户端点击File->Deploy OVF Template，将下载的连接器 OVA 部署到您的 VMware 环境中。
4.	打开连接器的虚拟机控制台并使用密码 ec2pass 以 ec2-user 身份进行登录。在系统提示时提供新密码。 
5.	获取连接器的 IP 地址，如下所示：
    ```sh
    Current network configuration: DHCP
    IP: 192.0.2.100
    Netmask: 255.255.254.0
    Gateway: 192.0.2.1
    DNS server 1: 192.0.2.200
    DNS server 2: 192.0.2.201
    DNS suffix search list: subdomain.example.com
    Web proxy: not configured
    Reconfigure your network:
      1. Renew or acquire a DHCP lease
      2. Set up a static IP
      3. Set up a web proxy for AWS communication
      4. Set up a DNS suffix search list
      5. Exit
    Please enter your option [1-5]:
    ```

6.	在连接器的网络配置菜单中，配置 DNS 后缀搜索列表中的域后缀值。
7.	在 Web 浏览器中，通过 IP 地址 (https://ip-address-of-connector/) 访问连接器 VM，然后选择 Get started now。 
    [![image 03](assets/SMS_vm-import/SMS03.png)]
8.	阅读许可协议，选中复选框，然后选择 Next。 
9.	为连接器创建密码。
    [![image 04](assets/SMS_vm-import/SMS04.png)]
10.	选择 Upload logs automatically 和 服务器迁移连接器 auto-upgrade。 
    [![image 05](assets\SMS_vm-import/SMS05.png)]
11.	对于 AWS Region，从列表中选择您的区域。对于 AWS Credentials，输入您在配置您的 AWS 账户权限中创建的 IAM 凭证。选择 Next。 
12.	对于 vCenter Service Account，输入步骤 3 中的 vCenter 主机名、用户名和密码。选择 Next。 
13.	接受 vCenter 证书后，完成注册，然后查看连接器配置控制面板。
    [![image 06](assets\SMS_vm-import/SMS06.png)]
14.	验证 Connectors 页面中是否显示您已注册的连接器。 


##### 第三步：使用 AWS SMS 控制台复制 VM

1. 如果您尚未导入目录，请选择 Servers -> Import server catalog。如需在 VMware 环境中添加的新服务器，请选择 Re-import server catalog。
2. 选择要复制的服务器，然后选择 Create replication job。
    [![image 07](assets\SMS_vm-import/SMS07.png)]
3. 在 Configure server -> specific settings 页面上的 License type 列中，选择要从复制作业创建的 AMI 的许可类型。Linux 服务器只能使用自带许可 (BYOL)。Windows 服务器可以使用 AWS 提供的许可或 BYOL。您还可以选择 Auto 以让 AWS SMS 选择适当的许可。选择 Next。
4. 在 Configure replication job settings 页面上，有以下设置可用：

    •	 Replication job type - replicate server every interval 选项创建一个重复的复制过程，该过程按您从菜单提供的间隔创建新的 AMI。One-time migration 选项会触发服务器的单个复制，而不安排重复复制。
    •	Start replication run - 您可将复制运行配置为立即开始或计划在未来 30 天内的某一日期和时间开始。日期和时间设置会参考浏览器的本地时间。
•	IAM service role - 提供 (如有必要) 您之前创建的 IAM 服务角色。
•	Description - 提供复制运行的描述。(可选) 
•	Enable automatic AMI deletion - 将 AWS SMS 配置为当复制 AMI 数量超出您在字段中提供的数字时删除较早的复制 AMI。
•	启用通知 - 选择是，则可以配置 Amazon Simple Notification Service (Amazon SNS) 在复制作业完成、失败或被删除时通知列表中的收件人。

5. 选择 Next。
6. 在“Review”页面上，检查您的设置。如果所有设置均正确，请选择 Create。要更改设置，请选择 Previous。在设置完复制作业后，将在指定的时间、以指定的间隔自动开始复制。

##### 第四步： 监控和修改服务器复制作业

 - 在 AWS SMS 控制台中，选择 Replication jobs。可通过滚动表来查看所有复制作业。在搜索栏中，可按特定值筛选表内容。
    选择一个复制作业，以便在下方的窗格中查看有关该作业的详细信息。Job details 选项卡显示有关当前复制运行的信息，包括该复制作业创建的最新 AMI 的 ID。Run history 选项卡显示有关选定复制作业的所有复制运行的详细信息。

 - 如更改作业参数，请在 Replication jobs 页面上选择一个作业，点击 Actions -> Edit replication job。在 Edit configuration job 表单中输入新信息后，选择 Save 以提交您的更改。

    
##### 第五步： 关闭复制

 - 如在复制完服务器后，需要删除复制作业。在 Replication jobs中选择对应作业，点击 Actions -> Delete replication jobs。在确认窗口中，选择 Delete。这会停止复制作业并清除该服务创建的任何项目 (例如，作业的 S3 存储桶)，不会删除由已停止的作业运行创建的任何 AMI。
 - 如需清除服务器目录，请选择 Servers -> Clear server catalog。将从 AWS SMS 和您的显示中删除服务器列表。
 - 如需取消连接器关联，请选择 Connectors，然后选择要取消关联的连接器。在其信息部分的右上角选择 Disassociate，然后在确认窗口中再次选择 Disassociate。此操作将从 AWS SMS 中取消注册连接器。

# Part 2: 使用vm-import导入您的VM

本指导将逐步描述如何从VM中导出您的虚拟系统，使用 AWS Command Line Interface(AWS CLI) 或 API 工具将其导入 Amazon EC2。在开始操作前，请确保您的电脑中已经安装有 AWS CLI （请参考AWS CML用户指南）。

### 步骤一  配置AWS CLI

安装客户端后，请在 AWS 控制台中选择您的 IAM User，创建安全证书并下载访问安全密钥，根据 AWS Access Key 和 AWS Secret Access Key 配置您的帐户。

[![image 01](assets/SMS_vm-import/VMImport01.png)]

### 步骤二 配置并导出VM

在导出前，需确保您的VM具有以下几种配置：

Windows系统：

  - 启用 Remote Desktop (RDP) 以进行远程访问。
  -如果配置了主机防火墙 (Windows 防火墙或类似防火墙)，请确保该防火墙允许访问 RDP。否则在导入完成后，您将无法访问您的实例。
  - 确保管理员账户和所有其他用户账户使用安全密码。所有账户均须有密码，否则导入可能失败。
  - 在 VM 上安装适当的 .NET Framework 版本。请注意，如果需要，系统会自动在您的 VM 上安装 .NET Framework 4.5 或更高版本。
  - 在您的 Windows VM 上禁用 Autologon。
  - 设置 RealTimeIsUniversal 注册表项。有关更多信息，请参阅 Amazon EC2 用户指南（适用于 Windows 实例） 中的设置时间。

Linux系统：

  - 在VM中启用SSH远程访问，并保证VM防火墙允许外部访问VM。虽然允许基于密码的SSH，但为安全起见，建议使用公共密钥登录。
  - 在VM中配置一个非root用户。（可选）
  - 确保您的 Linux VM 将 GRUB（传统 GRUB）或 GRUB 2 作为其启动加载程序。
  - 确保您的 Linux VM 使用下列根文件系统之一：EXT2、EXT3、EXT4、Btrfs、JFS 或 XFS。
  - 关闭所有反病毒软件，从您的 VMware 虚拟机上卸载 VMware 工具。
  - 保持您的网络设置为 DHCP 而不是静态 IP 地址。
  - 导入的 Linux VM使用 64 位映像

完成导入准备工作后，您可以从虚拟环境中将VM导出。

AWS支持四种格式的磁盘：开放虚拟化存档 (OVA)、虚拟机磁盘 (VMDK)、虚拟硬盘 (VHD/VHDX) 和原始格式。您也可以选择将开放虚拟化格式 (OVF)作为导出格式，OVF通常包含一个或多个 VMDK、VHD 或 VHDX 文件。

有关更多信息，请参阅您的虚拟化环境的文档。例如：
  - VMware - VMware 网站上的导出 OVF 模板
  - Citrix - Citrix 网站上的将 VM 导出为 OVF/OVA
  - Microsoft Hyper-V - Microsoft 网站上的导出和导入虚拟机概览

本示例中我们使用VirualBox，该应用软件是一款小巧精悍、功能齐全的免费应用软件，且支持导出OVF/OVA格式的VM。

导出VM时，在VirualBox主界面打开File->Export Appliance，选择需要导出的虚拟机，点击Next。
选择导出配置，这里可以选择OVF/OVA两种格式，并选择保存地址。

[![image 02](assets/SMS_vm-import/VMImport02.png)]

接下来对导出的VM添加说明信息后，就可以导出了，这里大约需要等待3分钟。
[![image 03](assets/SMS_vm-import/VMImport03.png)]

### 步骤三 将VM作为映像导入

您可以使用 VM Import/Export 将虚拟机 (VM) 映像作为 Amazon 系统映像 (AMI) 从虚拟化环境导入到 Amazon EC2 中，并用于启动实例。随后，您也可以将 VM 映像从实例导回到虚拟化环境中。

##### 1.	创建VM import服务角色

VM Import 需要一个角色在您的账户中执行特定的操作，例如：从 Amazon S3 存储桶下载磁盘映像

###### 创建服务角色

 - 利用以下策略创建名为 trust-policy.json 的文件，这里需注意，如果您位于中国区，请在Service后增加.cn。

    ```sh
    {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": { "Service": "vmie.amazonaws.com" },
            "Action": "sts:AssumeRole",
            "Condition": {
                "StringEquals":{
                    "sts:ExternalId": "vmimport"
                }
            }
        }]
    }
    ```
    
 - 使用 create-role 命令创建名为 vmimport 的角色，并向 VM Import/Export 提供对该角色的访问权。请确保指定 trust-policy.json 文件的完整路径，并且为路径添加 file:// 前缀。

    ```sh
    aws iam create-role --role-name vmimport --assume-role-policy-document  file://trust-policy.json
    ```

 - 创建名为 role-policy.json 的文件并编写下面的策略，其中，disk-image-file-bucket 为存储磁盘映像的存储桶，这里需注意，如果您在中国区，请将Resource中arn:aws:s3更改为arn:aws-cn:s3。

    ```sh
    {
        "Version":"2012-10-17",
        "Statement":[{
            "Effect":"Allow",
            "Action":[
                "s3:GetBucketLocation",
                "s3:GetObject",
                "s3:ListBucket" 
            ],
            "Resource":[
                "arn:aws:s3:::disk-image-file-bucket",
                "arn:aws:s3:::disk-image-file-bucket/*"
            ]
        },
        {
            "Effect":"Allow",
            "Action":[
                "ec2:ModifySnapshotAttribute",
                "ec2:CopySnapshot",
                "ec2:RegisterImage",
                "ec2:Describe*"
            ],
            "Resource":"*"
        }]
    }
    ```
    
 - 使用下面的 put-role-policy 命令将策略挂载到之前创建的角色。请务必指定 role-policy.json 文件位置的完整路径。    
    ```sh
    aws iam put-role-policy --role-name vmimport --policy-name vmimport             --policy-document file://role-policy.json
    ```
    
##### 2.	导入映像任务

- 创建名为containers.json的文件。
    ```sh
    [{
        "Description": "Windows 2008 OVA",
        "Format": "ova",
        "UserBucket": {
            "S3Bucket": "my-import-bucket",
            "S3Key": "vms/my-windows-2008-vm.ova"
        }
    }]
    ```
    
 - 导入OVA。

    ```sh
    aws ec2 import-image --description " Centos 7.0 " --disk-containers file://containers.json
    ```

##### 3.	检查您的导入映像任务的状态

用户根据上一步保留的 ImportTaskId 值自行替换该值，即可查询该任务的情况。

    ```sh
    aws ec2 describe-import-image-tasks --cli-input-json "{ \"ImportTaskIds\":         [\"import-ami-fggrs8es\"], \"NextToken\": \"abc\", \"MaxResults\": 10 } "
    ```

当使用上述命令查询任务状态时，根据AWS的处理进度，返回任务响应中的Status依次为“Pending”、“Converting”、“Updating”、“Updated”、“Preparing AMI”等。整个的处理过程持续10+分钟，请用户耐心等待。

[![image 04](assets/SMS_vm-import/VMImport04.png)]