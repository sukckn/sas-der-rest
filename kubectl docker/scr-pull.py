from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/pull-scr', methods=['POST'])
def pull_scr():
    # Get JSON data from the request
    inputData= request.get_json()

    # set http status code
    status= 200

    # get input parameters
    SCR_NAME= inputData.get('SCR_NAME')
    if not SCR_NAME:
        status= 400
        return jsonify({'error': 'SCR_NAME is required'}), status

    SCR_TAG= inputData.get('SCR_TAG')
    if not SCR_TAG:
        status= 400
        return jsonify({'error': 'SCR_TAG is required'}), status

    APP_OWNER= inputData.get('APP_OWNER')
    if not APP_OWNER:
        status= 400
        return jsonify({'error': 'APP_OWNER is required'}), status

    # Prepare the environment variables for the yaml file
    env= ''
    ENV_VARS= inputData.get('ENV_VARS')
    if ENV_VARS:
        for v in ENV_VARS:
            na= list(v.keys())[0]
            val= v[list(v.keys())[0]]
            env+= f'        - name: "{na}"\n          value: "{val}"\n'

    # Open yaml template and replace placeholders
    with open('./scr-template.yaml', 'r') as file:
        yaml_template= file.read()

    yaml_content= yaml_template.replace('<SCR-NAME>', SCR_NAME)
    yaml_content= yaml_content.replace('<APP-OWNER>', APP_OWNER)
    yaml_content= yaml_content.replace('<SCR-TAG>', SCR_TAG)
    yaml_content= yaml_content.replace('<ENV-VARS>', env)

    yaml_file= f'scr-{SCR_NAME}.yaml'
    with open(yaml_file, "w", encoding="utf-8") as file:
        file.write(yaml_content)

    # Apply the yaml file using kubectl
    try:
        result= subprocess.run(['kubectl', 'apply', '-f', yaml_file], capture_output=True, text=True)
    except Exception as e:
        status= 424 # Failed Dependency
        # Return an error response        
        return jsonify({'error': f'{e}'}), status

    # read some parameters from the yamle file so that we can return them in the response
    bNamespace= False
    bServerURL= False
    with open(yaml_file, 'r') as file:
        for line in file:
            if line.strip()[0:10] == 'namespace:':
                if not bNamespace:
                    NAMESPACE= line.strip()[10:].strip()
                    bNamespace= True
            if line.strip()[0:7] == '- host:':
                if not bServerURL:
                    SERVER_URL= line.strip()[7:].strip()
                    bServerURL= True
            if line.strip()[0:11] == 'targetPort:':
                if not bServerURL:
                    PORT= line.strip()[11:].strip()

    # Return a response
    return jsonify({
        'message': f'{SCR_NAME} successfully applied in namespace {NAMESPACE}',
        'url': f'https://{SERVER_URL}/{SCR_NAME}:{PORT}',
        'result': f'{result.stdout}',
        'error': f'{result.stderr}'
                 }), 200

###########################################################################################
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8089)


