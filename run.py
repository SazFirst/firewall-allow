import math
import subprocess
import configparser
import pandas
import datetime


# 입력한 이름이 기존과 중복되는지 확인
def check_displayname(rule):
    cmd = f'powershell if (Get-NetFirewallRule -DisplayName {rule}) {{ \'True\' }} else {{ \'False\' }}'
    out = subprocess.run(cmd, shell=True, capture_output=True, encoding='cp949').stdout

    # powershell 출력은 \n이 붙어나오므로 \n을 붙여야함
    if (out == 'True\n'):
        return True
    else:
        return False


# 데이터를 받아서 korean_ip.txt 파일에 저장
def crawling():
    print('https://xn--3e0bx5euxnjje69i70af08bea817g.xn--3e0b707e/jsp/statboard/IPAS/inter/sec/currentV4Addr.jsp에서 정보를 받아옵니다...')
    table = pandas.read_html(
        'https://xn--3e0bx5euxnjje69i70af08bea817g.xn--3e0b707e/jsp/statboard/IPAS/inter/sec/currentV4Addr.jsp', flavor='bs4')
    table = table[0]

    print('korean_ip.txt 파일을 작성 중입니다...\n')
    with open('korean_ip.txt', 'w') as f:
        for index, row in table.iterrows():
            network_address = row[0]
            cidr = 24 - int(math.log2(row[2]))
            f.write(network_address + '/' + str(cidr) + '\n')


def update_rule(rule_name):
    print(f'{rule_name}에 규칙을 업데이트 중입니다...\n')
    cmd = ['powershell',
           f'$address=Get-Content -Path .\korean_ip.txt;',
           f'$rule = Get-NetFirewallRule -DisplayName \"{rule_name}\";',
           f'$filter = Get-NetFirewallAddressFilter -AssociatedNetFirewallRule $rule;',
           f'Set-NetFirewallAddressFilter -InputObject $filter -RemoteAddress $address']
    subprocess.run(cmd, shell=True, encoding='cp949')


def create_rule(rule_name):
    print(f'규칙을 새로 생성하는 중입니다...\n')
    cmd = ['powershell',
           f'$address=Get-Content -Path .\korean_ip.txt;',
           f'New-NetFirewallRule -DisplayName {rule_name} -Direction Inbound -Action Allow -Protocol TCP -LocalPort 8839 -RemoteAddress $address']
    subprocess.run(cmd, shell=True, encoding='cp949')


config = configparser.ConfigParser(allow_no_value=True)
if not config.read('config.ini'):
    # 기존 config 파일이 없을 경우
    config['Inbound Rule List'] = {}
    config['global'] = {}
    rules = config['Inbound Rule List']

    # 인바운드 규칙 추가
    print('설정된 인바운드 규칙이 없습니다.')
    rule_name = input('새로 추가할 인바운드 규칙 이름을 지정하세요: ')
    print()
    while check_displayname(rule_name):
        print('중복된 이름입니다.')
        rule_name = input('새로 추가할 인바운드 규칙 이름을 지정하세요: ')
        print()
    rules[rule_name] = None

    # 입력한 이름으로 인바운드 규칙 생성
    crawling()
    create_rule(rule_name)
    print('방화벽 인바운드 규칙 추가가 완료되었습니다.')
else:
    rules = list(config['Inbound Rule List'].keys())
    select_all = len(rules)
    select_insert = len(rules) + 1

    # 설정된 목록을 띄운다
    print('한국 IP만 허용하는 인바운드 규칙 목록입니다')
    for index, key in enumerate(rules):
        print(f'[{index+1}] {key}')
    print(f'[{select_all + 1}] 전부 업데이트')
    print(f'[{select_insert + 1}] 새로운 규칙 생성')

    # 목록에서 선택
    select = int(input('업데이트할 인바운드 규칙을 선택하세요: ')) - 1
    print()

    crawling()

    if select < select_all:
        update_rule(rules[select])
    elif select == select_all:
        for rule in rules:
            update_rule(rule)
    elif select == select_insert:
        # 인바운드 규칙 추가
        rule_name = input('새로 추가할 인바운드 규칙 이름을 지정하세요: ')
        print()
        while check_displayname(rule_name):
            print('중복된 이름입니다.')
            rule_name = input('새로 추가할 인바운드 규칙 이름을 지정하세요: ')
            print()
        config['Inbound Rule List'][rule_name] = None

        create_rule(rule_name)

# 설정 저장
config['global']['date'] = str(datetime.date.today())
with open('config.ini', 'w') as configfile:
    config.write(configfile)

input()
