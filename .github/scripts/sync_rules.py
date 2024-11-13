def convert_to_clash(loon_file, clash_file):
    with open(loon_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    yaml_content = ['payload:']
    current_comment = ''
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if line.startswith('#'):
            current_comment = line
            yaml_content.append(f'{current_comment}')
        elif line.startswith('DOMAIN-SUFFIX,'):
            domain = line.split(',')[1]
            yaml_content.append(f'  - DOMAIN-SUFFIX,{domain}')
    
    with open(clash_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(yaml_content) + '\n')

def convert_to_quanx(loon_file, quanx_file, policy):
    with open(loon_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    quanx_content = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if line.startswith('#'):
            quanx_content.append(line)
        elif line.startswith('DOMAIN-SUFFIX,'):
            domain = line.split(',')[1]
            quanx_content.append(f'HOST-SUFFIX,{domain},{policy}')
    
    with open(quanx_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(quanx_content) + '\n')

def main():
    # 同步 Direct 规则
    convert_to_clash('rules/Loon/Self-Direct.list', 'rules/Clash/Self-Direct.yaml')
    convert_to_quanx('rules/Loon/Self-Direct.list', 'rules/QuanX/Self-Direct.list', 'Self-Direct')
    
    # 同步 Proxy 规则
    convert_to_clash('rules/Loon/Self-Proxy.list', 'rules/Clash/Self-Proxy.yaml')
    convert_to_quanx('rules/Loon/Self-Proxy.list', 'rules/QuanX/Self-Proxy.list', 'Self-Proxy')

if __name__ == '__main__':
    main()
