from typing import Dict

from lgtm import LGTMSite, LGTMDataFilters

project_list_name_to_gh_org = {
    'Google_Projects': [
        'google',
        'GoogleCloudPlatform',
        'GoogleContainerTools',
        'googleapis',
        'googlecolab',
        'googlemaps',
        'google-cloudsearch',
        'flutter'
    ],
    'Apache_Projects': ['apache'],
    'AirBnB_Projects': ['airbnb'],
    'LinkedIn_Projects': ['linkedin'],
    'Netflix_Projects': ['Netflix'],
    'OpenTracing_Projects': ['opentracing', 'opentracing-contrib'],
    'Spring_Projects': ['spring-projects'],
    'Jenkins_Projects': ['jenkinsci'],
    'Cloudfoundry_Projects': ['cloudfoundry'],
    'Square_Projects': ['square'],
    'Gradle_Projects': ['gradle'],
    'PortSwigger_Projects': ['PortSwigger'],
    'Wildlfy_Projects': ['wildfly', 'jbosstools'],
    'Graphite_Projects': ['graphite-project'],
    'Openmrs_Projects': ['openmrs'],
    'JetBrains_Projects': ['JetBrains'],
    'Eclipse_Projects': [
        'eclipse',
        'eclipse-ee4j',
    ],
    'Microsoft_Projects': ['microsoft'],
    'PayPal_Projects': ['paypal'],
    'Spinnaker_Projects': ['spinnaker'],
    'Elastic_Projects': ['elastic'],
    'Facebook_Projects': ['facebook'],
    'DataDog_Projects': ['DataDog'],
    'Micronaut_Projects': ['micronaut-projects'],
    'Apple_Projects': ['apple'],
}

project_list_to_repo = {
    'jOOq-Users': [
        'self-xdsd/self-storage',
        'folio-org/mod-source-record-storage',
        'ICIJ/datashare',
        'hartwigmedical/hmftools',
        'openforis/collect',
        'jklingsporn/vertx-jooq',
        'trib3/leakycauldron',
        'ZupIT/charlescd',
        'waikato-datamining/adams-applications'
    ]
}

# Flip the list
gh_org_to_project_list_name: Dict[str, str] = {}
for list_name in project_list_name_to_gh_org:
    for gh_org in project_list_name_to_gh_org[list_name]:
        gh_org_to_project_list_name[gh_org] = list_name

site = LGTMSite.create_from_file()
org_to_projects = LGTMDataFilters.org_to_ids(site.get_my_projects())
for org in org_to_projects:
    if org not in gh_org_to_project_list_name:
        print('Skipping %s as org location not specified' % org)
        continue
    project_list_name = gh_org_to_project_list_name[org]
    project_list_id = site.get_or_create_project_list(project_list_name)
    for project in org_to_projects[org]:
        if project.is_protoproject():
            print('Unable to add project to project list since it is a protoproject. %s' % project)
            continue
        site.load_into_project_list(project_list_id, [project.key])
        site.unfollow_repository(project)
