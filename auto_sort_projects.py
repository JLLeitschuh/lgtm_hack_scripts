from typing import Dict, List

from lgtm import LGTMSite, LGTMDataFilters, SimpleProject

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
    'Netflix_Projects': [
        'Netflix',
        'nebula-plugins'
    ],
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
        'eclipse-theia',
    ],
    'Microsoft_Projects': ['microsoft', 'Azure'],
    'PayPal_Projects': ['paypal'],
    'Spinnaker_Projects': ['spinnaker'],
    'Elastic_Projects': ['elastic'],
    'Facebook_Projects': ['facebook'],
    'DataDog_Projects': ['DataDog'],
    'Micronaut_Projects': ['micronaut-projects'],
    'Apple_Projects': ['apple'],
    'Gradle_Plugin_Projects': ['nebula-plugins'],
    'Open_Rewrite_Projects': ['openrewrite'],
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
    ],
    'Gradle_Plugin_Projects': [
        '47degrees/hood',
        'autonomousapps/dependency-analysis-android-gradle-plugin',
        'applandinc/appmap-gradle-plugin',
        'anatawa12/auto-visitor',
        'aim42/htmlSanityCheck',
        'android-async-http/android-async-http',
        'diffplug/spotless',
        'diffplug/blowdryer',
        'diffplug/spotless-changelog',
        'spring-cloud/spring-cloud-contract',
        'JetBrains/gradle-intellij-plugin',
        'JetBrains/gradle-jps-compiler-plugin',
        'JetBrains/gradle-grammar-kit-plugin',
        'JetBrains/gradle-changelog-plugin',
        'JetBrains/gradle-idea-ext-plugin',
        'JetBrains/gradle-node-envs',
        'JetBrains/gradle-python-envs',
        'JetBrains/gradle-ruby-envs',
        'JetBrains/gradle-intellij-plugin',
        'openrewrite/rewrite-gradle-plugin',
    ],
    'Top_Java_Projects': [
        'apereo/cas',
        'spring-projects/spring-boot',
        'iluwatar/java-design-patterns',
        'square/retrofit',
        'square/okhttp',
        'zxing/zxing',
        'libgdx/libgdx',
        'google/guava',
        'alibaba/dubbo',
        'jfeinstein10/SlidingMenu',
        'netty/netty',
        'JakeWharton/ActionBarSherlock',
        'chrisbanes/Android-PullToRefresh',
        'alibaba/fastjson',
        'deeplearning4j/deeplearning4j',
        'JakeWharton/ViewPagerIndicator',
        'alibaba/druid',
        'liaohuqiu/android-Ultra-Pull-To-Refresh',
        'mybatis/mybatis-3',
        'springside/springside4',
        'apache/storm',
        'xetorthio/jedis',
        'apache/hadoop',
        'dropwizard/dropwizard',
        'swagger-api/swagger-codegen',
        'code4craft/webmagic',
        'junit-team/junit',
        'Trinea/android-common',
        'clojure/clojure',
        'nhaarman/ListViewAnimations',
        'perwendel/spark',
        'spring-projects/spring-mvc-showcase',
        'square/dagger',
        'swagger-api/swagger-core',
        'jhy/jsoup',
        'mcxiaoke/android-volley',
        'Activiti/Activiti',
        'spring-projects/spring-petclinic',
        'openhab/openhab',
        'JakeWharton/NineOldAndroids',
        'wildfly/wildfly',
        'Bukkit/Bukkit',
        'jersey/jersey',
        'NLPchina/ansj_seg',
        'spring-projects/spring-security-oauth',
        'eclipse/vert.x',
        'apache/flink',
        'neo4j/neo4j',
        'google/guice',
        'MyCATApache/Mycat-Server',
        'apache/camel',
        'druid-io/druid',
        'naver/pinpoint',
        'AsyncHttpClient/async-http-client',
        'thinkaurelius/titan',
        'stanfordnlp/CoreNLP',
        'dropwizard/metrics',
        'bauerca/drag-sort-listview',
        'EnterpriseQualityCoding/FizzBuzzEnterpriseEdition',
        'brettwooldridge/HikariCP',
        'pardom/ActiveAndroid',
        'google/auto',
        'square/otto',
        'openmrs/openmrs-core',
        'alibaba/jstorm',
        'b3log/solo',
        'hankcs/HanLP',
        'knightliao/disconf',
        'facebook/presto',
        'aws/aws-sdk-java',
        'cucumber/cucumber-jvm',
        'Atmosphere/atmosphere',
        'yusuke/twitter4j',
        'yasserg/crawler4j',
        'alibaba/canal',
        'gephi/gephi',
        'NanoHttpd/nanohttpd',
        'google/closure-compiler',
        'JakeWharton/DiskLruCache',
        'apache/hive',
        'square/okio',
        'scribejava/scribejava',
        'checkstyle/checkstyle',
        'roboguice/roboguice',
        'hazelcast/hazelcast',
        'antlr/antlr4',
        'databricks/learning-spark',
        'Alluxio/alluxio',
        'jfinal/jfinal',
        'apache/hbase',
        'javaee-samples/javaee7-samples',
        'joelittlejohn/jsonschema2pojo',
        'dangdangdotcom/elastic-job',
        'pxb1988/dex2jar',
        'alibaba/DataX',
        'shuzheng/zheng',
        'Graylog2/graylog2-server',
        'brianfrankcooper/YCSB',
        'essentials/Essentials',
        'kbastani/spring-cloud-microservice-example',
        'square/javapoet',
    ],
}

# Flip the list
gh_org_to_project_list_name: Dict[str, str] = {}
for list_name in project_list_name_to_gh_org:
    for gh_org in project_list_name_to_gh_org[list_name]:
        gh_org_to_project_list_name[gh_org] = list_name

gh_repo_to_project_list_name: Dict[str, str] = {}
for list_name in project_list_to_repo:
    for gh_repo in project_list_to_repo[list_name]:
        gh_repo_to_project_list_name[gh_repo] = list_name

site = LGTMSite.create_from_file()
my_projects = site.get_my_projects()
org_to_projects: Dict[str, List[SimpleProject]] = LGTMDataFilters.org_to_ids(my_projects)
for org in org_to_projects:
    project_lists_to_use: List[Dict] = []

    if org in gh_org_to_project_list_name:
        project_list_name = gh_org_to_project_list_name[org]
        project_list_id = site.get_or_create_project_list(project_list_name)
        project_lists_to_use.append({'id': project_list_id, 'name': project_list_name})

    for project in org_to_projects[org]:
        if project.is_protoproject:
            print('Unable to add project to project list since it is a protoproject. %s' % project)
            continue

        # Create a list of project lists to add this project to
        project_lists_to_use_local = project_lists_to_use.copy()
        if project.display_name in gh_repo_to_project_list_name:
            project_list_name = gh_repo_to_project_list_name[project.display_name]
            project_list_id = site.get_or_create_project_list(project_list_name)
            project_lists_to_use_local.append({'id': project_list_id, 'name': project_list_name})

        project_list_str = [project_list["name"] for project_list in project_lists_to_use_local]
        print(f'Adding repository {project.display_name} to project lists: {project_list_str}')
        # Add the project to the project lists
        for project_list in project_lists_to_use_local:
            site.load_into_project_list(project_list['id'], [project.key])

        if project_lists_to_use_local:
            site.unfollow_repository(project)
