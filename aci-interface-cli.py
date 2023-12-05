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

    def login(self, user, pw, url):
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
        self.headers["Cookie"] = f'APIC-cookie={response.json()["imdata"][0]["aaaLogin"]["attributes"]["token"]}'

    def list(self) -> list:
        response = requests.request(
            "GET",
            url=f'{self.base_url}/api/node/class/l1PhysIf.json?query-target-filter=ne(l1PhysIf.descr, "")',
            headers=self.headers,
            verify=self.ssl_verify
        )
        if response.status_code == 200:
            return response.json()
        raise Exception('Failed to Execute.')


@click.group()
@click.pass_context
def aci_interface_cli(ctx):
    '''ACI Interface CLI'''
    if "ACI_USERNAME" not in os.environ or "ACI_PASSWORD" not in os.environ or "ACI_URL" not in os.environ:
        click.secho(
            "ERROR: You must specify ACI_USERNAME and ACI_PASSWORD and ACI_URL as environment variables.",
            fg="red"
        )
        exit(1)
    obj = ACI()
    obj.login(
        url=os.environ['ACI_URL'],
        user=os.environ['ACI_USERNAME'],
        pw=os.environ['ACI_PASSWORD']
    )
    ctx.obj = obj

@click.command()
@click.pass_obj
@click.option(
    "--table/--json", 
    default=True, 
    required=False,
    help='Show a list as table or json'
)
@click.option(
    "--csv", 
    default=False,
    is_flag=True,
    required=False,
    help='Show a list as table or json'
)
def list(obj, table, csv):
    '''Show a list of Physical Interfaces from ACI'''
    output = None
    queried = obj.list()
    if csv:
        template_raw = '''
sep=^
pod^node^interface^adminSt^mtu^mode^descr
{% for item in interfaces['imdata'] %}
{%- set l1PhysIf = item["l1PhysIf"]["attributes"] -%}
{{l1PhysIf["dn"].split('/')[1].split('-')[1]}}^{{l1PhysIf["dn"].split('/')[2].split('-')[1]}}^{{l1PhysIf["dn"].split('-')[3][1:-1]}}^{{l1PhysIf.adminSt}}^{{l1PhysIf.mtu}}^{{l1PhysIf.mode}}^{{l1PhysIf.descr}}
{% endfor %}'''
        template = Template(source=template_raw)
        rendered = template.render(interfaces=queried)
        with open('interfaces.csv', 'w') as f:
            f.write(rendered)
            print('interface.csv file was created.')
    elif table:
        output = PrettyTable()
        output.field_names = [
            "pod",
            "node",
            "interface",
            "adminSt",
            "mtu",
            "mode",
            "descr"
        ]
        output.align = "l"
        for item in queried['imdata']:

            l1PhysIf = item["l1PhysIf"]["attributes"]
            row = [
                l1PhysIf["dn"].split('/')[1].split('-')[1],
                l1PhysIf["dn"].split('/')[2].split('-')[1],
                l1PhysIf["dn"].split('-')[3][1:-1],
                l1PhysIf["adminSt"],
                l1PhysIf["mtu"],
                l1PhysIf["mode"],
                l1PhysIf["descr"]
            ]
            output.add_row(row)
        click.echo(output)
    else:
        output = json.dumps(queried)
        click.echo(output)

aci_interface_cli.add_command(list)

if __name__ == "__main__":
    aci_interface_cli()