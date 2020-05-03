from retrying import retry
import random


class FileNotYetUploaded(Exception):
    pass


def retry_if_file_empty(result):
    print("Check if file empty: {}".format(result))
    return result <= 5


@retry(retry_on_result=retry_if_file_empty, wait_fixed=2000,
       stop_max_attempt_number=3)
def read_file():
    status = random.randint(0, 10)
    return status


def retry_on_exception(exc):
    return isinstance(exc, FileNotYetUploaded)


@retry(retry_on_exception=retry_on_exception, wait_fixed=2000,
       stop_max_attempt_number=10)
def _check_if_file_uploaded():
    status = random.randint(0, 10)
    print("Status:{}".format(status))
    if status != 7:
        if status == 1:
            raise Exception("Error while uploading file")
        print(
            "File not yet uploaded, retry after 2 seconds: {}".format(status))
        raise FileNotYetUploaded
    else:
        print("File uploaded successfully")


def __upload_file():
    print("Uploading file ....")
    _check_if_file_uploaded()


if __name__ == '__main__':
    print("Hello")
    __upload_file()
    read_file()
