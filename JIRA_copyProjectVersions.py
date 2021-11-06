# Script for copying project version from project A to project B
# Requirements:
#   'jira' package
# Usage:
#   Just change the Jira URL, username and password and define your project keys

from jira.client import JIRA
import re
import urllib3

jiraHost = 'https://jira.domain.com'
jiraUser = 'username'
jiraPass = 'password'

projectA = 'PROJECTKEYOLD'
projectB = 'PROJECTKEYNEW'

options = JIRA.DEFAULT_OPTIONS
options['server'] = jiraHost

# disable SSL verification
options['verify'] = False
urllib3.disable_warnings()

# initiate
jira = JIRA(options=options, basic_auth=(jiraUser, jiraPass))
print(f"Moving all versions from project '{projectA}' to project '{projectB}'...")

for version in jira.project_versions(projectA):
    print(version, '... ', end='')

    # some condition added - e.g. when we don't want archived version or specific
    if version.archived or not re.search(r'^1.[0-9]', version.name):
        print("skipped")
        continue

    try:
        jira.create_version(version.name, projectB)
        print("created")
    except:
        print("error - already exists?")
