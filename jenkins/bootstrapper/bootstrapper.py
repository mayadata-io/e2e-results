import argparse
import datetime
import os
import requests
import yaml
import testrail
import json
import shutil

ACCESS_RIGHT = 0o755


def create_directory(path):
    try:
        os.makedirs(path, ACCESS_RIGHT)
    except OSError as e:
        print("Directory %s creation failed\nError: %s" % (path, e))
        return path, -1
    print("Successfully Created directory %s" % path)
    return path, 0


def remove_directory(path):
    try:
        shutil.rmtree(path, ignore_errors=True)
    except OSError as e:
        print("Directory %s creation failed\nError: %s" % (path, e))
        return -1
    return 1


def create_init_directory(args):
    build_number = args['build_number']
    path = '/tmp/%s/%s' % (str(datetime.datetime.now())[:10], build_number) + '/testrail'
    return create_directory(path)


def get_yml(args, path, filename):
    url = args['yml_url']
    return save_file(url, path + "/" + filename)


def parse_plans(filename):
    try:
        file = open(filename, 'r')
        plans = yaml.load(file.read())
        file.close()
    except EnvironmentError as e:
        print("File operation failed\nError: %s" % e)
        return None, -1
    except yaml.YAMLError as e:
        print("YAML operation failed\nError: %s" % e)
        return None, -1
    if 'TestRailProjectID' not in plans.keys() or 'Platform' not in plans.keys():
        print("Error parsing yml file")
        return {}, -1
    return plans, 0


def add_suites(args, add_suites_args):
    suite_id, description, plan_id = add_suites_args['suite_id'], add_suites_args['description'], add_suites_args[
        'plan_id']
    return args['client'].send_post('add_plan_entry/' + plan_id, {'suite_id': suite_id, 'description': description})


def get_cases(suite_id, args):
    return args['client'].send_get('get_cases/' + args['project_id'] + '&suite_id=' + suite_id)


def write_file(path, content):
    try:
        file = open(path, "w+")
        file.write(content)
        file.close()
    except EnvironmentError as e:
        print("File operation failed\nError: %s" % e)
        return "", -1
    return path, 0


def save_file(url, path):
    try:
        r = requests.get(url)
    except requests.exceptions.RequestException as e:
        print("Request for url: %s failed\nError: %s" % (url, e))
        return "", -1
    return write_file(path, r.text)


def create_case_resources(cases, path):
    case_result, master_playbook_result = {}, []

    # Iterating over cases
    for case in cases:
        if len(case['refs'].split(',')) != 3:
            print("Case Id: %s's refs not in correct format" % str(case['id']))
            return {}, [], -1
        #  Splitting url,reponame and issue_number from case reference
        case_result['url'], case_result['reponame'], case_result['issue_number'] = case['refs'].split(',')

        case_result['case_id'] = case['id']

        # Creating directory for test
        tmp_path, err = create_directory(path + "/" + str(case['id']))
        if err == -1: return {}, [], err

        # Downloading playbook and saving to file
        _, err = save_file(case_result['url'], tmp_path + "/playbook.yml")
        if err == -1: return {}, [], err

        # Linking local yml to master yml
        master_playbook_result.append({'include': str(case['id']) + '/playbook.yml'})

    return case_result, master_playbook_result, 0


def create_suite_resources(args, create_suite_resources_args):
    suites, path, plan_id = create_suite_resources_args['suites'], create_suite_resources_args['path'], \
                            create_suite_resources_args['plan_id']
    map_src_id = {}

    # Iterating over suites
    for suite in suites:
        for suite_name, suite_info in suite.items():

            # Checking if any description available for suite
            description = suite_info if suite_info is not None else ""

            # Adding suite into plan
            add_suites_args = {'suite_id': int(suite_name), 'plan_id': plan_id, 'description': description}
            tmp_suite = add_suites(args, add_suites_args)
            if tmp_suite['suite_id'] is None:
                print("Adding suite %s failed\nError: %s" % (suite_name, suite))
                return {}, [], -1

            # Mapping suite id with run id
            map_src_id[tmp_suite['suite_id']] = {'run_id': tmp_suite['runs'][0]['id'], 'cases': []}

            # Fetching cases of suites
            cases = get_cases(str(suite_name), args)

            # Creating case resources
            cases_result, master_playbook_map, err = create_case_resources(cases, path)
            if err == -1: return {}, [], err

            # Adding information to maps
            map_src_id[tmp_suite['suite_id']]['cases'].append(
                {'case_id': cases_result['case_id'], 'url': cases_result['url'], 'reponame': cases_result['reponame'],
                 'issue_number': cases_result['issue_number']})

    return map_src_id, master_playbook_map, 0


def create_testrail_plan(args, create_testrail_plan_args):
    plan_name, description = create_testrail_plan_args['plan_name'], create_testrail_plan_args['description']
    return args['client'].send_post('add_plan/' + args['project_id'], {'name': plan_name, 'description': description})


def plan_util(args, plan_util_args):
    platform_name, platform_info, path = plan_util_args['platform_name'], plan_util_args['platform_info'], \
                                         plan_util_args['path']
    date, build_number = str(datetime.datetime.now())[:16], args['build_number']

    # Creating plan name
    plan_name = date + ' build-' + platform_name + '-' + build_number

    # Registering a plan in testrail for current platform
    create_testrail_plan_args = {'plan_name': plan_name, 'description': platform_info['Description']}
    plan = create_testrail_plan(args, create_testrail_plan_args)

    # Checking if plan created
    if plan['id'] is None:
        print("Plan creation failed")
        return path, plan, -1

    # Creating directory for platform
    temp_path, err = create_directory(path + "/" + platform_name)
    if err == -1:
        return path, plan, err

    return temp_path, plan, err


def write_maps(path, maps):
    for filename, value in maps.items():
        _, err = write_file(path + "/" + filename, value)
        if err == -1:
            return err
    return 0


def create_plan_resources(args, create_plan_resources_args):
    plans_info, path = create_plan_resources_args['plans_info'], create_plan_resources_args['path']
    # Adding testrail client and path to args for reuse
    client, client.user, client.password = testrail.APIClient(args['test_rail_api']), args['testrail_username'], args[
        'testrail_password']
    args['client'] = client

    # Iterating over platforms
    for platform in plans_info['Platform']:

        # Iterating over platform dictionary
        for platform_name, platform_info in platform.items():
            print("Setting up " + platform_name + ":")
            plan_util_args = {'platform_name': platform_name, 'platform_info': platform_info, 'path': path}
            temp_path, plan, err = plan_util(args, plan_util_args)
            if err == -1:
                return err
            # creating a map of suite id run id and cases
            create_suite_resources_args = {'suites': platform_info['Test Suite'], 'path': temp_path,
                                           'plan_id': str(plan['id'])}
            map_src_id, master_playbook_map, err = create_suite_resources(args, create_suite_resources_args)

            if err == -1:
                return err

            # writing maps to file
            maps = {'mapping.json': json.dumps(map_src_id),
                    'master.yml': yaml.dump(master_playbook_map, default_flow_style=False)}
            err = write_maps(temp_path, maps)
            if err == -1:
                return err
    return 0


def clean_up(path, err):
    if remove_directory(path) == -1:
        print("Cleaning up failed")
    else:
        print("Cleaning up successful")
    print("Bootstrapping unsuccessful")
    exit(err)


def driver(args):
    path, err = create_init_directory(args)
    if err == -1:
        clean_up(path, err)
    plans_info, err = get_yml(args, path, "plan-info.yml")
    if err == -1:
        clean_up(path, err)
    plans_info, err = parse_plans(plans_info)
    if err == -1:
        clean_up(path, err)
    args['project_id'] = str(plans_info['TestRailProjectID'])
    create_plan_resources_args = {'plans_info': plans_info, 'path': path}
    err = create_plan_resources(args, create_plan_resources_args)
    if err == -1:
        print("Plan Resource Failed\nCleaning up")
        clean_up(path, err)
    print("Bootstrapping completed successfully")


def main():
    parser = argparse.ArgumentParser(description='cli to get the required data')
    parser.add_argument('-bn', '--build-number', help='It is the build number from jenkins', required=True)
    parser.add_argument('-yl', '--yml-url', help="url of the raw yml file", required=True)
    parser.add_argument('-tuser', '--testrail-username', help='Username of TestRail', required=True)
    parser.add_argument('-tpass', '--testrail-password', help='Password of Testrail', required=True)
    parser.add_argument('-turl', '--test-rail-api', help='API url of testrail', required=True)
    args = vars(parser.parse_args())
    driver(args)


if __name__ == '__main__':
    main()
