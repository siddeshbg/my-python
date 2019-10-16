#!/usr/bin/env python3
import os
import jenkins
import requests
from requests.auth import HTTPBasicAuth


class JenkinsHelper:
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password
        self.server = jenkins.Jenkins(url, username=self.username, password=self.password)

    def download_build_log(self, build_url, download_dir='logs'):
        job_path = build_url.split('job')[1]
        job_name = job_path.split('/')[1]
        build_number = job_path.split('/')[2]
        log_file_name = job_name + "_" + str(build_number) + "_log.txt"
        log_path = download_dir + "/" + log_file_name

        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        if not os.path.exists(log_path):
            print("Start: Downloading %s ... " % build_url)
            response = self.get_console_output(build_url)

            with open(log_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)
            print("Done: Downloaded %s at %s... " % (build_url, log_file_name))
        else:
            print("Info: %s already downloaded at %s, ignoring ..." % (build_url, log_file_name))

    def get_server_info(self):
        user = self.server.get_whoami()
        version = self.server.get_version()
        print('Hello %s from Jenkins %s' % (user['fullName'], version))

    def get_jobs(self):
        return self.server.get_jobs()

    def get_last_build_number(self, job_name):
        return self.server.get_job_info(job_name)['lastCompletedBuild']['number']

    def get_job_config(self, job_name):
        return self.server.get_job_config(job_name)

    def get_build_info(self, job_name, build_number):
        return self.server.get_build_info(job_name, build_number)

    def get_job_info(self, job_name):
        return self.server.get_job_info(job_name, fetch_all_builds=True)

    def get_available_builds(self, job_name):
        builds = {}
        job_info = self.get_job_info(job_name)
        for build in job_info['builds']:
            builds[build['number']] = build['url']

        return builds

    def get_console_output(self, build_url):
        return requests.get(build_url, auth=HTTPBasicAuth(self.username, self.password), verify=False, stream=True)

    def get_build_console_output(self, job_name, build_number):
        return self.server.get_build_console_output(job_name, build_number)


def main():
    url = os.environ['JENKINS_URL']
    user = os.environ['JENKINS_USER']
    passwd = os.environ['JENKINS_PASSWORD']
    helper = JenkinsHelper(url, user, passwd)
    helper.get_server_info()
    #jobs = helper.get_jobs()
    job_name = 'Build_CDM_Unit_Tests'
    #job_info = helper.get_job_config(job_name)
    #last_build_number = helper.get_last_build_number(job_name)
    #build_info = helper.get_build_info(job_name, last_build_number)
    #job_info = helper.get_job_info(job_name)

    build_number = 435
    build_path = url + "/job/" + job_name + "/" + str(build_number) + "/consoleText"
    ''' usage of reading console output
    response = helper.get_console_output(build_path)
    console_out = response.text.splitlines()
    print(console_out[0], "\n", console_out[-1])
    '''
    helper.download_build_log(build_path)
    builds = helper.get_available_builds(job_name)
    for buildnum in builds.keys():
        print(buildnum, builds[buildnum])


if __name__ == '__main__':
    main()
