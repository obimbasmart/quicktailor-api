#!/usr/bin/env python3

"""
This module encapsulates functionality for
interacting with AWS S3 (Simple Storage Service).
"""

from typing import List, Dict
from uuid import uuid4
import boto3
from os import getenv
from src.storage.config import get_settings
from fastapi import File

settings = get_settings()


class S3StorageService():
    __allowed_file_types = ['png', 'jpeg', 'pdf', 'svg', 'jpg']
    __presigned_url_exp_time = 3600

    def __init__(self, cache=None):
        self.bucket_name = settings.S3_BUCKET_NAME
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name='eu-north-1'
        )

        self.cache = cache

    def __is_valid_file_extenstion(self, filename):
        file_ext = filename.split('.')[-1]
        return file_ext in S3StorageService.__allowed_file_types

    def upload_file(self, file: File, id: str, folder='') -> str:
        """
        :param file: file object
        :param tailor_id: tailor's id
        :param product_id: product id - :: depreciated (tailor will first upload image b4 creating product)
        :raises: TypeError - invalid file type
        :return: img url
        """
        if not self.__is_valid_file_extenstion(file.filename):
            raise TypeError("Invalid file type")

        key_name = f'{folder}/{id}/{str(uuid4().hex)}'
        self.s3_client.upload_fileobj(file.file, self.bucket_name, key_name,
                                      ExtraArgs={'ContentType': file.content_type})
        return key_name

    def generate_presigned_url(self, action_type: str, key_name: str, width=None, height=None, aspect_ratio = None) -> str:
        """generate aws s3 url for performing actions on an object

        :param action_type: 'get_object' | 'put_object' | 'delete_object'
        :param key_name: object key
        :return: presigned url
        """

        data = self.cache.get(key_name, self.cache.get_json)
        if data:
            return data

        img_url = self.s3_client.generate_presigned_url(
            action_type,
            Params={'Bucket': self.bucket_name, 'Key': key_name},
            ExpiresIn=S3StorageService.__presigned_url_exp_time
        )

        image_data = {
            'url': img_url,
            'width': width,
            'height': height,
            'aspect_ratio': aspect_ratio
        }

        self.cache.store_json(key_name, image_data, self.__presigned_url_exp_time)
        return image_data

    def generate_presigned_urls(self, action_type: str, images: List[Dict]) -> List[Dict]:
        return [
            self.generate_presigned_url('get_object', image['url'])
            for image in images
        ]

    def upload_files(self, files: List[File], id: str, folder: str) -> Dict[str, str]:
        img_urls = [
            self.upload_file(file, id, folder)
            for file in files
        ]
        return img_urls
  

    def delete_file(self, filename):
        return self.s3_client.delete_object(Bucket=self.bucket_name, Key=filename)

    def delete_files(self, filenames: List[str]) -> None:
        [
            self.delete_file(filename)
            for filename in filenames
        ]

from services.cache import cache
s3_client = S3StorageService(cache=cache)
