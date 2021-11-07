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
print(f"Copying all versions from project '{projectA}' to project '{projectB}'...")

for ver in jira.project_versions(projectA):
    verDesc  = ver.raw['description'] if 'description' in ver.raw else ""
    verStart = ver.raw['startDate'] if 'startDate' in ver.raw else None
    verEnd   = ver.raw['releaseDate'] if 'releaseDate' in ver.raw else None
    print(ver, '... ', end='')

    # some condition added - e.g. when we don't want archived ver or specific
    if ver.archived:
        print("skipped - archived")
        continue

    if not re.search(r'^1.[0-9]', ver.name):
        print("skipped - doesn't matach")
        continue

    verB = jira.get_project_version_by_name(projectB, ver.name)

    if verB: # if target version exists, just update it
        verB.update(description=verDesc,
                    startDate=verStart,
                    releaseDate=verEnd,
                    archived=ver.archived,
                    released=ver.released)
        print("updated")
    else: # create a new one                
        verB = jira.create_version(ver.name,
                            projectB,
                            description=verDesc,
                            startDate=verStart,
                            releaseDate=verEnd,
                            released=ver.released)
        
        # set archived flag in the second call (because of bug https://jira.atlassian.com/browse/JRASERVER-61990)
        if ver.archived:
            verB.update(archived=True)
        print("created")

# optional -- deleting all versions in the target project
##for ver in jira.project_versions(projectB):
##    print(ver, '... ', end='')
##
##    verCount = jira.version_count_related_issues(ver.id)
##    if verCount['issuesFixedCount'] or \
##       verCount['issuesAffectedCount'] or \
##       verCount['issueCountWithCustomFieldsShowingVersion']:
##        print('existing issues - skipping...')
##    else:
##        print('deleting...', ver.delete())
