import requests
import os
from urllib3.exceptions import InsecureRequestWarning
import click
from prettytable import PrettyTable
import json
from jinja2 import Template

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class ACI(object):
    def __init__(self):
        self.base_url = ""
        self.username = ""
        self.password = ""
        self.ssl_verify = False
        self.headers = {"Content-Type": "application/json"}

    def login(self, user, pw, url) -> bool:
        self.base_url = url
        self.username = user
        self.password = pw
        payload = '''{
            "aaaUser": {
                "attributes": {
                    "name": "''' + self.username + '''",
                    "pwd": "''' + self.password + '''"
                }
            }
        }'''
        response = requests.request(
            'POST',
            f'{self.base_url}/api/aaaLogin.json',
            headers=self.headers,
            data=payload,
            verify=self.ssl_verify
        )
        if response.status_code == 200:
            self.headers["Cookie"] = f'APIC-cookie={response.json()["imdata"][0]["aaaLogin"]["attributes"]["token"]}'
            return True
        else:
            return False

    def get_l1PhysIf(self, page_size=100, filters={}) -> (bool, dict):
        '''call rest api for get physical interfaces'''
        l1PhysIf = []
        page = 0
        while True:
            url = f'{self.base_url}/api/node/class/l1PhysIf.json?page-size={page_size}&page={page}'
            if filters:
                filter_items = []
                if 'descr_exists' in filters:
                    filter_items.append('ne(l1PhysIf.descr,"")')
                if 'state' in filters:
                    filter_items.append(f'eq(l1PhysIf.adminSt,"{filters["state"]}")')
                url += f'&query-target-filter=and({",".join(filter_items)})'
            res = requests.request("GET", url=url, headers=self.headers, verify=self.ssl_verify)
            try:
                res.json()['imdata'][0]
                for item in res.json()['imdata']:
                    l1PhysIf.append(item)
            except:
                break
            page += 1
        return True, {"imdata": l1PhysIf}

    def get_vpcIf(self, filters) -> (bool, str):
        '''call rest api for get VPC interfaces'''
        url = f'{self.base_url}/api/node/class/vpcIf.json?page=0'
        if filters:
            if filters['descr_exists']:
                url += '&query-target-filter=ne(vpcIf.descr,"")'
        response = requests.request("GET", url=url, headers=self.headers, verify=self.ssl_verify)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, 'Failed to Execute.'


@click.group()
@click.pass_context
def aci_interface_cli(ctx):
    '''ACI Interface CLI'''
    if "ACI_USERNAME" not in os.environ or "ACI_PASSWORD" not in os.environ or "ACI_URL" not in os.environ:
        click.secho("ERROR: You must specify ACI_USERNAME and ACI_PASSWORD and ACI_URL as environment variables.", fg="red")
        exit(1)
    obj = ACI()
    login = obj.login(url=os.environ['ACI_URL'], user=os.environ['ACI_USERNAME'], pw=os.environ['ACI_PASSWORD'])
    if not login:
        click.secho("Login failed.", fg="red")
        exit(1)
    ctx.obj = obj


@click.command()
@click.pass_obj
@click.option("--state", type=click.Choice(['up', 'down'], case_sensitive=False), required=False, help='Filter by adminSt of interface')
@click.option("--csv", default=False, is_flag=True, required=False, help='Downloads as csv file')
@click.option("--descr-exists", default=False, is_flag=True, required=False, help='Including only interfaces having description')
@click.option("--raw", default=False, is_flag=True, required=False, help='Shows raw data as json format')
def phys(obj, state, csv, descr_exists, raw):
    '''Shows physical interfaces'''
    output = None
    filters = {}
    if descr_exists:
        filters['descr_exists'] = descr_exists
    if state:
        filters['state'] = state
    success, queried = obj.get_l1PhysIf(filters=filters)

    if not success:
        click.secho("Execute failed.", fg="red")
        exit(1)        

    if csv:
        template = Template(source='''sep=^
pod^node^interface^adminSt^mtu^mode^descr
{% for item in interfaces['imdata'] %}
{%- set l1PhysIf = item["l1PhysIf"]["attributes"] -%}
{{l1PhysIf["dn"].split('/')[1].split('-')[1]}}^{{l1PhysIf["dn"].split('/')[2].split('-')[1]}}^{{l1PhysIf["dn"].split('-')[3][1:-1]}}^{{l1PhysIf.adminSt}}^{{l1PhysIf.mtu}}^{{l1PhysIf.mode}}^{{l1PhysIf.descr}}
{% endfor %}''')
        rendered = template.render(interfaces=queried)
        with open('interfaces_phys.csv', 'w') as f:
            f.write(rendered)
            print('interface_phys.csv file was created.')
    elif raw:
        click.echo(json.dumps(queried))
    else:
        output = PrettyTable()
        output.field_names = ["pod", "node", "interface", "adminSt" ,"mtu", "mode", "descr"]
        output.align = "l"
        for item in queried['imdata']:
            intf = item["l1PhysIf"]["attributes"]
            row = [
                intf["dn"].split('/')[1].split('-')[1],     # pod
                intf["dn"].split('/')[2].split('-')[1],     # node
                intf["dn"].split('-')[3][1:-1],             # interface
                intf["adminSt"],
                intf["mtu"],
                intf["mode"],
                intf["descr"]
            ]
            output.add_row(row)
        click.echo(output)


@click.command()
@click.pass_obj
@click.option("--csv", default=False, is_flag=True, required=False, help='Downloads as csv file')
@click.option("--descr-exists", default=False, is_flag=True, required=False, help='Including only interfaces having description')
@click.option("--raw", default=False, is_flag=True, required=False, help='Shows raw data as json format')
def vpc(obj, csv, descr_exists, raw):
    '''Shows physical interfaces'''
    output = None
    filters = {}
    if descr_exists:
        filters['descr_exists'] = descr_exists

    success, queried = obj.get_vpcIf(filters=filters)

    if not success:
        click.secho("Execute failed.", fg="red")
        exit(1)        

    if csv:
        template = Template(source='''
sep=^
pod^node^domain^interface^localOperSt^remoteOperSt^descr
{% for item in interfaces['imdata'] %}
{%- set intf = item["vpcIf"]["attributes"] -%}
{{intf["dn"].split('/')[1].split('-')[1]}}^{{intf["dn"].split('/')[2].split('-')[1]}}^{{intf["dn"].split('/')[6]}}^{{intf["dn"].split('/')[7]}}^{{intf["localOperSt"]}}^{{intf["remoteOperSt"]}}^{{intf["descr"]}}
{% endfor %}''')
        rendered = template.render(interfaces=queried)
        with open('interfaces_vpc.csv', 'w') as f:
            f.write(rendered)
            print('interface_vpc.csv file was created.')
    elif raw:
        output = json.dumps(queried)
        click.echo(output)
    else:
        output = PrettyTable()
        output.field_names = ["pod", "node", "domain", "interface", "localOperSt", "remoteOperSt", "descr"]
        output.align = "l"
        for item in queried['imdata']:
            intf = item["vpcIf"]["attributes"]
            row = [
                intf["dn"].split('/')[1].split('-')[1],     # pod
                intf["dn"].split('/')[2].split('-')[1],     # node
                intf["dn"].split('/')[6],                   # domain
                intf["dn"].split('/')[7],                   # interface
                intf["localOperSt"],
                intf["remoteOperSt"],
                intf["descr"]
            ]
            output.add_row(row)
        click.echo(output)


aci_interface_cli.add_command(phys)
aci_interface_cli.add_command(vpc)


if __name__ == "__main__":
    aci_interface_cli()