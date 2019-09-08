#!/usr/bin/env python
# coding: utf-8

# Object: folder/cat.jpg (key/version ID)<br>
# Bucket: jennie

# Link: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-examples.html

# https://docs.aws.amazon.com/code-samples/latest/catalog/code-catalog-python-example_code-s3.html

# https://realpython.com/python-boto3-aws-s3/

# # Create bucket

# In[1]:


import boto3
import uuid

import logging
import sys


# low-level interface
# s3_client = boto3.client('s3')
# or hig-level interrface
s3_resource = boto3.resource('s3')


# In[2]:



def create_bucket_name(bucket_prefix):
    return ''.join([bucket_prefix, str(uuid.uuid4())])


# In[3]:


# manually
# bucket_name = create_bucket_name("jennie.first")
# s3_resource.create_bucket(Bucket= bucket_name, CreateBucketConfiguration={'LocationConstraint': 'ap-southeast-1'})


# In[4]:


# region is set automatically with session

def create_bucket(bucket_prefix, s3_connection):
    session = boto3.session.Session()
    current_region = session.region_name
    bucket_name = create_bucket_name(bucket_prefix)
    bucket_response = s3_connection.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': current_region})
    
    return bucket_name, bucket_response


# In[5]:


first_bucket_name, first_bucket_response = create_bucket("jennie-first-", s3_resource)


# In[6]:


print(first_bucket_name)


# # File Name

# In[7]:


def create_tmp_file(size, file_name, file_content):
    random_file_name = ''.join([str(uuid.uuid4().hex[:6]), file_name])
    with open(random_file_name, 'w') as f:
        f.write(str(file_content) * size)
    return random_file_name


# In[8]:


first_file_name = create_tmp_file(300, 'firstfile.txt', 'f')


# In[9]:


with open(first_file_name, 'r') as file:
    for line in file:
        print(line)


# # Bucket and Object Instances

# In[10]:


first_bucket = s3_resource.Bucket(name=first_bucket_name)
first_object = s3_resource.Object(bucket_name= first_bucket_name, key="s3-file-dummy.txt")
# first_object_again = first_bucket.Object(first_file_name)


# # Upload a file

# 3 ways:<br>
# 1. Object instance<br>
# 2. Bucket<br>
# 3. client<br>

# In[11]:


# first_object - obj on S3
# Filename - object on my computer
first_object.upload_file(Filename= "C:\\Users\\Trang\\Desktop\\picapicachu.txt")
# client
# s3_resource.meta.client.upload_file(Filename=first_file, Bucket=bucket_name, Key=first_file)


# # Download a file

# In[12]:


first_file_name


# In[13]:


first_object.download_file('./tmpFolder/firstfile.txt')


# # Copy an object between buckets

# In[14]:


# second bucket
second_bucket_name, second_response = create_bucket('jennie-second-', s3_resource)


# In[15]:


print(second_bucket_name)


# In[16]:


# second_bucket = s3_resource.Bucket(name=second_bucket_name)
# second_object = second_bucket.Object("UAUAUAhello.txt")
# # no object created at this point


# In[17]:



def copy_to_bucket(src_bucket_name, src_file_name, dest_bucket_name, dest_file_name):
    copy_source = {'Bucket': src_bucket_name, 'Key': src_file_name}
    if dest_file_name is None:
        dest_file_name = src_file_name
        
    try:
        s3_resource.meta.client.copy_object(CopySource=copy_source, Bucket=dest_bucket_name, Key=dest_file_name)
    except:
        logging.error(sys.exc_info()[0])
        return False
    return True

second_file_name = 'lalallalalhello.txt'
copy_to_bucket(first_bucket_name, first_file_name, second_bucket_name, second_file_name)
# if the file does not exist, it will be created


# In[24]:


bucket = 'arn:aws:s3:::jennie-second-33412163-d7e9-4012-9b3e-d04c130b90dc'
bucket = str(bucket[13:])
# print(bucket)

def delete_all_objects(bucket_name):
    res = []
    bucket=s3_resource.Bucket(bucket_name)
    for obj_version in bucket.object_versions.all():
        res.append({'Key': obj_version.object_key,
                    'VersionId': obj_version.id})
#     print(res)
    bucket.delete_objects(Delete={'Objects': res})
    
# # delete_all_objects(bucket)
s3_resource.Bucket(bucket).delete()


# In[23]:


for bucket in s3_resource.buckets.all():
    print(bucket.name)
    if 'jennie' in bucket.name:
        print(bucket.name)
        for obj_version in bucket.object_versions.all():
            if obj_version is not None:
                delete_all_objects(bucket.name)
                break
        bucket.delete()


# In[ ]:




