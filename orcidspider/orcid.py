import json
import logging
from urllib.parse import urlencode
from urllib.parse import unquote
import requests


class OrcidSpider(object):

    def __init__(self, **kwargs):
        self.params = kwargs.get('params')
        print(self.params)
        self.list_url = 'https://pub.orcid.org/v2.0/search/?{}'
        self.detail_url = 'https://pub.orcid.org/v2.0/{}'
        self.headers = {
            "Accept": "application/json",
        }

    def send_requests(self, url):
        for _ in range(5):
            try:
                resp = requests.get(url, headers=self.headers)
            except Exception as err:
                logging.error(err.args[0])
            else:
                if resp.status_code == 200:
                    return resp

    def parse_list(self, q_params):
        resp = self.send_requests(self.list_url.format(q_params))
        print(self.detail_url.format(q_params))
        if resp is None:
            return
        return json.loads(resp.text)

    def parse_detail(self, orcid):
        resp = self.send_requests(self.detail_url.format(orcid))
        if resp is None:
            return
        return json.loads(resp.text)

    def run(self):
        q_params = urlencode(self.params)   # url编码
        q_params = unquote(q_params)        # url解码
        list_resp_text = self.parse_list(q_params)
        if list_resp_text is None:
            return
        result = list_resp_text['result']
        if result is None:
            return
        with open("orcid8.txt", 'a+', encoding='utf-8-sig') as f:
            for item in result:
                try:
                    orcid = item['orcid-identifier']['path']
                except:
                    print('出错了！')
                    return
                detail_resp_text = self.parse_detail(orcid)
                # 两种情况退出
                if detail_resp_text is None:
                    return
                education = parse_info(detail_resp_text['activities-summary']['educations']['education-summary'])
                employment = parse_info(detail_resp_text['activities-summary']['employments']['employment-summary'])
                if education == [] and employment == []:
                    return
                # 数据处理
                if detail_resp_text['person']['name']['family-name'] is None:
                    familyname = None
                else:
                    familyname = detail_resp_text['person']['name']['family-name']['value']
                if detail_resp_text['person']['biography'] is not None:
                    bio = detail_resp_text['person']['biography']['content']
                else:
                    bio = None
                json_record = dict(
                    orcid=orcid,
                    biography=bio,
                    familyname=familyname,
                    givennames=detail_resp_text['person']['name']['given-names']['value'],
                    education=education,
                    employment=employment
                )
                f.write(json.dumps(json_record, ensure_ascii=False))
                f.write('\n')                       # 输出这个人的详细信息
                return orcid
def parse_arg(*args):
    if args[0] != '':
        if args[2] == '':
            if args[3] == '':
                return 'family-name:"{}"+AND+given-names:"{}"'.format(args[0], args[1])
            return 'family-name:"{}"+AND+given-names:"{}"+AND+"{}"'.format(args[0], args[1], args[3])
        else:
            if args[3] == '':
                return 'family-name:"{}"+AND+given-names:"{}"+AND+affiliation-org-name:"{}"'.format(args[0], args[1], args[2])
            return 'family-name:"{}"+AND+given-names:"{}"+AND+affiliation-org-name:"{}"+AND+"{}"'.format(args[0], args[1], args[2], args[3])
    else:
        if args[2] == '':
            if args[3] == '':
                return 'given-names:"{}"'.format(args[1])
            return 'given-names:"{}"+AND+"{}"'.format(args[1], args[3])
        else:
            if args[3] == '':
                return 'given-names:"{}"+AND+affiliation-org-name:"{}"'.format(args[1], args[2])
            return 'given-names:"{}"+AND+affiliation-org-name:"{}"+AND+"{}"'.format(args[1], args[2], args[3])


def parse_info(list):
    l = []
    for item in list:
        department = item['department-name']
        role = item['role-title']
        if item['start-date'] is not None:
            if item['start-date']['year'] is not None:
                if item['start-date']['month'] is not None:
                    if item['start-date']['day'] is not None:
                        start_date = item['start-date']['year']['value'] + '-' + item['start-date']['month']['value'] +\
                                     '-' + item['start-date']['day']['value']
                    else:
                        start_date = item['start-date']['year']['value'] + '-' + item['start-date']['month']['value']
                else:
                    start_date = item['start-date']['year']['value']
            else:
                start_date = item['start-date']
            # start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        else:
            start_date = None
        if item['end-date'] is not None:
            if item['end-date']['year'] is not None:
                if item['end-date']['month'] is not None:
                    if item['end-date']['day'] is not None:
                        end_date = item['end-date']['year']['value'] + '-' + item['end-date']['month']['value'] + '-' +\
                                   item['end-date']['day']['value']
                    else:
                        end_date = item['end-date']['year']['value'] + '-' + item['end-date']['month']['value']
                else:
                    end_date = item['end-date']['year']['value']
            else:
                end_date = item['end-date']
            # end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        else:
            end_date = None
        organization = item['organization']['name']
        it = dict(department=department, role=role, start_date=start_date, end_date=end_date, organization=organization)
        l.append(it)
    return l