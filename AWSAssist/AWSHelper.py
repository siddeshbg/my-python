import boto3
import os

class AWSHelper:
    def __init__(self, profile=None):
        self.profile = profile

        if self.profile:
            boto3.setup_default_session(profile_name=self.profile)

    def get_s3_bucket_names(self):
        s3 = boto3.resource('s3')
        return [bucket.name for bucket in s3.buckets.all()]

    def upload_file_to_s3(self, bucket_name, file_path):
        data = open(file_path, 'rb')
        s3 = boto3.resource('s3')
        s3.Bucket(bucket_name).put_object(Key=os.path.basename(file_path),
                                          Body=data)


def main():
    helper = AWSHelper(profile='datos')
    print(helper.get_s3_bucket_names())

    helper.upload_file_to_s3(
        'siddeshbg',
        '/Users/siddeshbg/work/github-siddesh/my-python/log.txt'
    )


if __name__ == '__main__':
    main()
