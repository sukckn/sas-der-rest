import subprocess

SCR_NAME= 'churn-agent'
NAMESPACE= 'agentic-ai'
APP_OWNER= 'viyademo01'
SERVER_URL= 'ck06-sukckn.net.sas.com'

# Open yaml template and replace placeholders
with open('./scr-template.yaml', 'r') as file:
    yaml_template= file.read()

yaml_content= yaml_template.replace('<SCR-NAME>', SCR_NAME)
yaml_content= yaml_content.replace('<NAMESPACE>', NAMESPACE)
yaml_content= yaml_content.replace('<APP-OWNER>', APP_OWNER)
yaml_content= yaml_content.replace('<SERVER-URL>', SERVER_URL)

yaml_file= f'scr-{SCR_NAME}.yaml'
with open(yaml_file, "w", encoding="utf-8") as file:
    file.write(yaml_content)
    
try:
    result= subprocess.run(['kubectl', 'apply', '-f', yaml_file], capture_output=True, text=True)
except Exception as e:
    print (e)

print(result)