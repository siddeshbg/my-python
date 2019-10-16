#!/usr/bin/env python3
from jira import JIRA
import os


class JiraHelper:
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password
        self.jira = JIRA(self.url, basic_auth=(self.username, self.password))

    def get_all_fields(self):
        all_fields = self.jira.fields()
        return {field['name']: field['id'] for field in all_fields}

    def get_custom_field_value(self, issue, field):
        issue = self.jira.issue(issue, fields=field)
        return getattr(issue.fields, field)

    def get_component_manager(self, issue, fields='components,customfield_12713'):
        result = {}
        issue = self.jira.issue(issue, fields=fields)
        result['component'] = [comp.name for comp in issue.fields.components]
        result['component_manager'] = getattr(issue.fields, 'customfield_12713').displayName
        return result

    def get_issues(self, query, max_results=1000):
        return self.jira.search_issues(query, maxResults=max_results)

    def get_issue_description(self, issues):
        description = {}
        for issue in issues:
            description[issue.key] = issue.fields.description
        return description


def main():
    url = os.environ['JIRA_URL']
    user = os.environ['JIRA_USER']
    passwd = os.environ['JIRA_PASSWORD']
    helper = JiraHelper(url, user, passwd)
    print(helper.get_all_fields())
    # query = os.environ['JQL_QUERY']
    # result = helper.get_issues(query)
    # print("Following tickets in query: %s" % query)
    # for issue in result:
    #     print(issue.key)
    #     # print(issue.fields.summary)
    #     # print(issue.fields.description)
    # descriptions = helper.get_issue_description(result)
    #helper.get_field_values('CDM-169571', fields='customfield_12713')
    #comp_manager = helper.get_custom_field_value('CDM-169571', 'customfield_12713')
    #print(helper.get_component_manager('CDM-169571'))


if __name__ == '__main__':
    main()
