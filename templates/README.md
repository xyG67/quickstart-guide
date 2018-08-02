# Templates
所有 **CloudFormation Templates** 存放在如下文件夹，所有templates必须存放于子文件夹中


## 文件命令规则
如果比较简单的任务，尽量写成一个template, 如果任务比较复杂，可以分成两个template.

* `xxxx.template` 是china region 和global region通用的模板
* `xxx_cn.template` 表示仅仅支持china region
* `xxx_global.template` 表示仅仅支持global region

