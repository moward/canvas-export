#!/usr/bin/env python3
"""
Allows the user to export files from courses via the Canvas API.

TODO: Support for epub export
"""

__author__ = "Matt Howard <http://matt.how/>"
__version__ = "0.1"
__status__ = "Prototype"

import requests
import argparse
import os
import time

class CanvasClient(object):
    # dleay 1 second between polling the API
    POLL_DELAY = 1

    def __init__(self, access_token, api_base):
        self._access_token = access_token
        self._api_base = api_base

    # credit to Christian Barcenas (@cbarcenas) for this method, with modification
    def _request(self, method, path, **kwargs):
        # Construct full URL
        url = requests.compat.urljoin(self._api_base, path)

        # Set headers, overriding as necessary
        headers_override = kwargs.get('headers', {})
        kwargs['headers'] = {}
        kwargs['headers'].update(headers_override)
        kwargs['headers'].setdefault('Authorization', 'Bearer %s' % self._access_token)

        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        return response

    # credit to Christian Barcenas (@cbarcenas) for this method
    def _consume_pagination(self, path, **kwargs):
        while path:
            response = self._request('GET', path, **kwargs)
            items = response.json()
            yield from items
            path = response.links.get('next', {}).get('url')

    def get_courses(self):
        return list(self._consume_pagination('/api/v1/courses'))
    
    def export_course(self, course_id):
        '''Creates an export, waits on it to be ready, and returns a stream of the export'''

        export_post = self._request('POST', '/api/v1/courses/%d/content_exports' % course_id, data={'export_type': 'zip'})

        export_post_obj = export_post.json()

        progress_url = export_post_obj['progress_url']

        export_id = export_post_obj['id']

        completion = 0

        while completion < 100:
            time.sleep(self.POLL_DELAY)

            progress_response = self._request('GET', progress_url)
            completion = progress_response.json()['completion']
            print('Export %d%% complete' % completion)

        export_get_obj = {'workflow_state': 'exporting'}

        while export_get_obj['workflow_state'] == 'exporting':
            time.sleep(self.POLL_DELAY)

            export_get_obj = self._request('GET', '/api/v1/courses/%d/content_exports/%d' % (course_id, export_id)).json()

        if export_get_obj['workflow_state'] != 'exported':
            raise RuntimeError('Illegal export workflow_state %s' % export_get_obj['workflow_state'])

        return self._request('GET', export_get_obj['attachment']['url'])


def get_access_token():
    if 'CANVAS_ACCESS_TOKEN' not in os.environ:
        raise ValueError('CANVAS_ACCESS_TOKEN environmental variable not set')
    else:
        return os.environ['CANVAS_ACCESS_TOKEN']

def get_api_base():
    if 'CANVAS_API_BASE' not in os.environ:
        raise ValueError('CANVAS_API_BASE environmental variable not set')
    else:
        return os.environ['CANVAS_API_BASE']

def download_response(response, filename):
    with open(filename, 'wb') as fd:
        for chunk in response.iter_content(chunk_size=128):
            fd.write(chunk)

def generate_parser():
    parser = argparse.ArgumentParser(description='Export and download course files from Canvas LMS')

    parser.add_argument('-l', '--list', action='store_true',
        help='list all available courses by code and name then exits')

    parser.add_argument('-a', '--all', dest='export_all', action='store_true',
        help='export all courses')

    parser.add_argument('-f', '--force', action='store_true',
        help='overwrite existing files rather than skipping them')

    parser.add_argument('courses', metavar='COURSE', nargs='*',
        help='either the code or id of a course you want to export')

    return parser

def make_course_map(course_idens, ids_to_code):
    '''Generates a dict of id => course_code based off a list of identifiers

    Arguments:
    course_idens - A list of strings either representing ids or course codes
    ids_to_code - A dict of id => course code for all available courses
    '''

    codes_to_id = {v: k for k, v in ids_to_code.items()}

    courses_to_export = {}

    for course_iden in course_idens:
        if course_iden in codes_to_id:
            # define by code
            course_id = codes_to_id[course_iden]
            courses_to_export[course_id] = course_iden
        elif course_iden.isdigit():
            # define by id
            course_id = int(course_iden)
            if course_id in ids_to_code:
                courses_to_export[course_id] = ids_to_code[course_id]
            else:
                print('Skipping course id %d, course not found' % course_id)
        else:
            print('Skipping %s, course not found' % course_iden)

    return courses_to_export

def main():
    parser = generate_parser()
    args = parser.parse_args()

    # config client class
    access_token = get_access_token()
    api_base = get_api_base()
    client = CanvasClient(access_token, api_base)

    all_courses = client.get_courses()

    if args.list:
        for course in all_courses:
            if('course_code' in course):
                print('%s\t%s' % (course['course_code'], course['name']))
        return

    ids_to_code = {}
    for course in all_courses:
        if 'name' in course:
            ids_to_code[course['id']] = course['course_code']

    courses_to_export = None

    if args.export_all:
        courses_to_export = ids_to_code
    else:
        courses_to_export = make_course_map(args.courses, ids_to_code)

    if not len(courses_to_export):
        print("No courses to export. Exiting.")
        return

    for course_id, course_code in courses_to_export.items():
        download_filename = '%s.zip' % course_code

        if os.path.isfile(download_filename) and not args.force:
            print('Skipping \'%s\' because it already exists' % download_filename)
        else:
            print('Requesting %s' % course_code)

            content_export_response = client.export_course(course_id)

            print('Downloading %s' % course_code)

            download_response(content_export_response, download_filename)
            print('Download complete')

if __name__ == "__main__":
    main()
