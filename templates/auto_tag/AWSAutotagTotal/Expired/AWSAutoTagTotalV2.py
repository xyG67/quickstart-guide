#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/4 上午12:56
# @Author  : Dicey
# @File    : AWSAutoTagTotal2.0.py
# @Software: PyCharm


from __future__ import print_function
import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def tag_ec2(detail, user, principal):
    '''
    给 EC2 打 tag
    :return:
    '''
    ids = []
    ec2 = boto3.resource('ec2')

    items = detail['responseElements']['instancesSet']['items']
    for item in items:
        ids.append(item['instanceId'])
    logger.info(ids)
    logger.info('number of instances: ' + str(len(ids)))

    base = ec2.instances.filter(InstanceIds=ids)

    # loop through the instances
    for instance in base:
        for vol in instance.volumes.all():
            ids.append(vol.id)
        for eni in instance.network_interfaces:
            ids.append(eni.id)
    if ids:
        for resourceid in ids:
            print('Tagging resource ' + resourceid)
        ec2.create_tags(Resources=ids,
                        Tags=[{'Key': 'Owner', 'Value': user}, {'Key': 'PrincipalId', 'Value': principal}])


def tag_dynamodb(detail, user, principal):
    client = boto3.client('dynamodb')
    resource_arn = detail['responseElements']['tableDescription']['tableArn']
    tags = [{'Key': 'Owner', 'Value': user}, {'Key': 'PrincipalId', 'Value': principal}]
    client.tag_resource(ResourceArn=resource_arn, Tags=tags)


def tag_lambda(detail, user, principal):
    # Lambda 的实际 API 与文档中并不一致, 其组成为 AIP 名字+版本
    client = boto3.client('lambda')

    # Lambda 函数的 arn
    function_arn = detail['responseElements']['functionArn']
    logger.info('function_arn: ' + function_arn)

    tag = {'Owner': user, 'PrincipalId': principal}
    client.tag_resource(Resource=function_arn, Tags=tag)


def tag_rds(detail, user, principal):
    client = boto3.client('rds')
    resource_arn = detail['responseElements']['dBInstanceArn']

    tags = [{'Key': 'Owner', 'Value': user}, {'Key': 'PrincipalId', 'Value': principal}]
    client.add_tags_to_resource(ResourceName=resource_arn, Tags=tags)


def tag_redshift(detail, event, user, principal):
    cluster_name = detail['requestParameters']['clusterIdentifier']
    client = boto3.client('redshift')

    # 在 API 中并没有提供获取 RedShift ARN 的方法, 需要自己手动拼接
    # 特别的, 中国区的 ARN 形如
    # arn:aws-cn:redshift:region:account-id:cluster:cluster-name
    # 拼接 arn
    account_id = event['account']
    region = event['region']
    resource_arn = "arn:aws-cn:redshift:" + str(region) + ":" + str(account_id) + ":cluster:" + cluster_name
    logger.info("RedShift arn: " + resource_arn)

    tags = [{'Key': 'Owner', 'Value': user}, {'Key': 'PrincipalId', 'Value': principal}]
    client.create_tags(ResourceName=resource_arn, Tags=tags)


def tag_s3_object(detail, user, principal):
    s3 = boto3.client("s3")
    bucket_name = detail['requestParameters']['bucketName']
    object_name = detail['requestParameters']['key']

    tags = [{'Key': 'Owner', 'Value': user}, {'Key': 'PrincipalId', 'Value': principal}]
    s3.put_object_tagging(Bucket=bucket_name, Key=object_name, Tagging={'TagSet': tags})


def tag_s3_bucket(detail, user, principal):
    s3 = boto3.client("s3")
    bucket_name = detail['requestParameters']['bucketName']

    tags = [{'Key': 'Owner', 'Value': user}, {'Key': 'PrincipalId', 'Value': principal}]
    s3.put_bucket_tagging(Bucket=bucket_name, Tagging={'TagSet': tags})


def tag_sqs(detail, user, principal):
    client = boto3.client('sqs')
    queue_url = detail['responseElements']['queueUrl']

    tags = {'Owner': user, 'PrincipalId': principal}
    client.tag_queue(QueueUrl=queue_url, Tags=tags)


def tag_vpc(detail, user, principal):
    vpc_id = detail['responseElements']['vpc']['vpcId']

    ec2 = boto3.resource('ec2')
    vpc = ec2.Vpc(vpc_id)

    tags = [{'Key': 'Owner', 'Value': user}, {'Key': 'PrincipalId', 'Value': principal}]
    vpc.create_tags(DryRun=False, Tags=tags)


def lambda_handler(event, context):
    region = event['region']
    detail = event['detail']
    eventname = detail['eventName']
    arn = detail['userIdentity']['arn']
    principal = detail['userIdentity']['principalId']
    userType = detail['userIdentity']['type']

    # 判断事件是来自 User 实体还是来自 Rule
    if userType == 'IAMUser':
        user = detail['userIdentity']['userName']
    else:
        user = principal.split(':')[1]

    logger.info('principalId: ' + str(principal))
    logger.info('region: ' + str(region))
    logger.info('eventName: ' + str(eventname))
    logger.info('detail: ' + str(detail))

    if eventname == 'RunInstances':
        # 启动 EC2
        tag_ec2(detail, user, principal)

    elif eventname == 'CreateTable':
        # Dynamodb
        tag_dynamodb(detail, user, principal)

    elif eventname == 'CreateFunction20150331':
        # Lambda
        tag_lambda(detail, user, principal)

    elif eventname == 'CreateDBInstance':
        # RDS
        tag_rds(detail, user, principal)

    elif eventname == 'CreateCluster':
        # RedShift
        tag_redshift(detail, event, user, principal)

    elif eventname == 'CreateBucket':
        # 给 S3 桶打标签
        tag_s3_bucket(detail, user, principal)

    elif eventname == 'PutObject':
        # 给 S3 中 Object 打标签
        tag_s3_object(detail, user, principal)

    elif eventname == 'CreateQueue':
        # SQS
        tag_sqs(detail, user, principal)

    elif eventname == 'CreateVpc':
        # VPC
        tag_vpc(detail, user, principal)
    else:
        logger.warning('Not supported action')
        return False

    logger.info("Success!")
    return True