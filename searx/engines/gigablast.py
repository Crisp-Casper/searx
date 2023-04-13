# SPDX-License-Identifier: AGPL-3.0-or-later
#x#"""
#x#Gigablast (Web)
#x#"""
#x## pylint: disable=missing-function-docstring, invalid-name

#x#import re
#x#from json import loads, JSONDecodeError
#x#from urllib.parse import urlencode
#x#from searx.exceptions import SearxEngineResponseException
#x#from searx.poolrequests import get

# about
#x#about = {
#x# "website": 'https://www.gigablast.com',
#x# "wikidata_id": 'Q3105449',
#x# "official_api_documentation": 'https://gigablast.com/api.html',
#x# "use_official_api": True,
#x# "require_api_key": False,
#x# "results": 'JSON',
}

# engine dependent config
#x#categories = ['general']
#x#collections = 'main'
#x#search_type = ''
#x#fast = 0
# gigablast's pagination is totally damaged, don't use it
#x#paging = False
#x#safesearch = True

# search-url
#x#base_url = 'https://gigablast.com'

# ugly hack: gigablast requires a random extra parameter which can be extracted
# from the source code of the gigablast HTTP client
#x#extra_param = ''
#x#extra_param_path='/search?c=main&qlangcountry=en-us&q=south&s=10'

#x#_wait_for_results_msg = 'Loading results takes too long. Please enable fast option in gigablast engine.'

#x#def parse_extra_param(text):

#x# # example:
#x# #
#x# # var uxrl='/search?c=main&qlangcountry=en-us&q=south&s=10&rand=1590740241635&n';
#x# # uxrl=uxrl+'sab=730863287';
#x# #
#x# # extra_param --> "rand=1590740241635&nsab=730863287"

#x# global extra_param  # pylint: disable=global-statement
#x# re_var= None
#x# for line in text.splitlines():
#x##x#  if re_var is None and extra_param_path in line:
#x##x##x##x#var = line.split("=")[0].split()[1]  # e.g. var --> 'uxrl'
#x##x##x##x#re_var = re.compile(var + "\\s*=\\s*" + var + "\\s*\\+\\s*'" + "(.*)" + "'(.*)")
#x##x##x##x#extra_param = line.split("'")[1][len(extra_param_path):]
#x##x##x##x#continue
#x##x#  if re_var is not None and re_var.search(line):
#x##x##x##x#extra_param += re_var.search(line).group(1)
#x##x##x##x#break

#x#def init(engine_settings=None):  # pylint: disable=unused-argument
#x# parse_extra_param(get(base_url + extra_param_path).text)


# do search-request
#x#def request(query, params):  # pylint: disable=unused-argument

#x# # see API http://www.gigablast.com/api.html#/search
#x# # Take into account, that the API has some quirks ..
#x# query_args = {
#x##x#  'c': collections,
#x##x#  'format': 'json',
#x##x#  'q': query,
#x##x#  'dr': 1 ,
#x##x#  'showgoodimages': 0,
#x##x#  'fast': fast,
#x# }

#x# if search_type != '':
#x##x#  query_args['searchtype'] = search_type

#x# if params['language'] and params['language'] != 'all':
#x##x#  query_args['qlangcountry'] = params['language']
#x##x#  query_args['qlang'] = params['language'].split('-')[0]

#x# if params['safesearch'] >= 1:
#x##x#  query_args['ff'] = 1

#x# search_url = '/search?' + urlencode(query_args)
#x# params['url'] = base_url + search_url + extra_param

#x# return params

# get response from search-request
#x#def response(resp):
#x# results = []

#x# try:
#x##x#  response_json = loads(resp.text)
#x# except JSONDecodeError as e:
#x##x#  if 'Waiting for results' in resp.text:
#x##x##x##x#raise SearxEngineResponseException(message=_wait_for_results_msg)  # pylint: disable=raise-missing-from
#x##x#  raise e


#x# for result in response_json['results']:
#x##x#  # see "Example JSON Output (&format=json)"
#x##x#  # at http://www.gigablast.com/api.html#/search

#x##x#  # sort out meaningless result

#x##x#  title = result.get('title')
#x##x#  if len(title) < 2:
#x##x##x##x#continue

#x##x#  url = result.get('url')
#x##x#  if len(url) < 9:
#x##x##x##x#continue

#x##x#  content = result.get('sum')
#x##x#  if len(content) < 5:
#x##x##x##x#continue

#x##x#  # extend fields

#x##x#  subtitle = result.get('title')
#x##x#  if len(subtitle) > 3 and subtitle != title:
#x##x##x##x#title += " - " + subtitle

#x##x#  results.append(dict(
#x##x##x##x#url = url
#x##x##x##x#, title = title
#x##x##x##x#, content = content
#x##x#  ))

#x# return results
