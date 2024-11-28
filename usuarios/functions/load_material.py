### se va a generar la comunicación con Bonita y hacer la carga de materiales
from django.shortcuts import get_object_or_404, redirect
import requests

from usuarios.forms import Material, Materiales

USERNAME = 'walter.bates'
PASSWORD = 'bpm'
USER_ID=4
PUERTO = '8080'
def login():
    login_url = f"http://localhost:{PUERTO}/bonita/loginservice"
    login_data = {
        'username': USERNAME,
        'password': PASSWORD
    }

    # Realizar la petición POST para login
    login_response = requests.post(login_url, data=login_data)

    # Comprobar el estado de la respuesta de login
    if login_response.status_code == 200 or login_response.status_code == 204:
        # Obtener las cookies de la respuesta
        cookies = login_response.cookies
        x_bonita_api_cookie = cookies.get('X-Bonita-API-Token')
        return x_bonita_api_cookie, cookies.get('JSESSIONID')
    else:
        print(
            f"Error en el login: {login_response.status_code}, {login_response.text}")
        return None, None



def get_processes(x_bonita_api_cookie, jsessionid):
    process_url = f"http://localhost:{PUERTO}/bonita/API/bpm/process?p=0&c=10"
    
    headers = {
        'X-Bonita-API-Token': x_bonita_api_cookie,
        'Host': f'localhost:{PUERTO}',
        'Cookie': f'BOS_Locale=es; JSESSIONID={jsessionid}; X-Bonita-API-Token={x_bonita_api_cookie}'
    }

    process_response = requests.get(process_url, headers=headers)
    if process_response.status_code == 200 or process_response.status_code == 204:
        return process_response.json()
    return None


def find_process_by_name(processes, process_name):
    # Filtrar procesos que contengan el nombre especificado
    matching_processes = [p for p in processes if process_name in p['name']]
    if matching_processes:
        return matching_processes[0]['id']
    return None

def instantiate_process(x_bonita_api_cookie, jsessionid, process_id):
    # URL para instanciar el proceso
    instantiate_url = f"http://localhost:{PUERTO}/bonita/API/bpm/process/{process_id}/instantiation"

    # Configurar el header con el token X-Bonita-API-Token
    headers = {
        'X-Bonita-API-Token': x_bonita_api_cookie,
        'Host': f'localhost:{PUERTO}',
        'Cookie': f'BOS_Locale=es; JSESSIONID={jsessionid}; X-Bonita-API-Token={x_bonita_api_cookie}'
    }

    # Realizar la solicitud POST para instanciar el proceso
    instantiate_response = requests.post(instantiate_url, headers=headers)

    if instantiate_response.status_code == 200:
        return instantiate_response.json()
    return None

def update_case_variable(x_bonita_api_cookie, jsessionid, case_id, nombre_variable, valor_variable, tipo_variable):
    """
    Actualiza una variable de caso en Bonita Soft.
    
    :param x_bonita_api_cookie: Token de la API de Bonita.
    :param jsessionid: ID de sesión JSESSIONID.
    :param case_id: ID del caso en Bonita.
    :param nombre_variable: Nombre de la variable a actualizar.
    :param valor_variable: Valor que se asignará a la variable.
    :param tipo_variable: Tipo Java de la variable (ej: 'java.lang.String', 'java.lang.Boolean', etc.).
    :return: True si la actualización fue exitosa, False en caso contrario.
    """
    # URL para actualizar la variable del caso
    update_url = f"http://localhost:{PUERTO}/bonita/API/bpm/caseVariable/{case_id}/{nombre_variable}"
    headers = {
        'X-Bonita-API-Token': x_bonita_api_cookie,
        'Host': f'localhost:{PUERTO}',
        'Cookie': f'BOS_Locale=es; JSESSIONID={jsessionid}; X-Bonita-API-Token={x_bonita_api_cookie}',
        'Content-Type': 'application/json'
    }

    body = {
        "type": tipo_variable,
        "value": valor_variable
    }

    # Hacemos la solicitud PUT
    response = requests.put(update_url, headers=headers, json=body)
    
    return response.status_code == 200

def get_task_id_by_case_id(x_bonita_api_cookie, jsessionid, case_id):
    get_url = f"http://localhost:{PUERTO}/bonita/API/bpm/task?f=caseId={case_id}"

    headers = {
        'X-Bonita-API-Token': x_bonita_api_cookie,
        'Host': f'localhost:{PUERTO}',
        'Cookie': f'BOS_Locale=es; JSESSIONID={jsessionid}; X-Bonita-API-Token={x_bonita_api_cookie}'
    }

    response = requests.get(get_url, headers=headers)

    if response.status_code == 200:
        tasks = response.json()
        if tasks:
            return tasks[0]['id']
        return None
    return None

def assign_user_to_task_id(x_bonita_api_cookie, jsessionid, task_id, assigned_id):
    update_url = f"http://localhost:{PUERTO}/bonita/API/bpm/humanTask/{task_id}"

    headers = {
        'X-Bonita-API-Token': x_bonita_api_cookie,
        'Host': f'localhost:{PUERTO}',
        'Cookie': f'BOS_Locale=es; JSESSIONID={jsessionid}; X-Bonita-API-Token={x_bonita_api_cookie}',
        'Content-Type': 'application/json'
    }

    body = { "assigned_id": assigned_id }

    response = requests.put(update_url, headers=headers, json=body)

    return response.status_code == 200
    

def execute_user_task(x_bonita_api_cookie, jsessionid, task_id):
    # URL para ejecutar la tarea de usuario con el taskId
    execute_url = f"http://localhost:{PUERTO}/bonita/API/bpm/userTask/{task_id}/execution"

    # Configurar el header con el token X-Bonita-API-Token
    headers = {
        'X-Bonita-API-Token': x_bonita_api_cookie,
        'Host': f'localhost:{PUERTO}',
        'Cookie': f'BOS_Locale=es; JSESSIONID={jsessionid}; X-Bonita-API-Token={x_bonita_api_cookie}',
        'Content-Type': 'application/json'
    }

    # Realizar la solicitud POST para ejecutar la tarea de usuario
    response = requests.post(execute_url, headers=headers)

    # Comprobar el estado de la respuesta
    if response.status_code == 204:
        print("Tarea ejecutada con éxito, pero no hay contenido para devolver.")
        return True  # Retornar True o None según lo que necesites
    elif response.status_code == 200:
        # Mostrar el contenido de la respuesta (JSON)
        return response.json()
    else:
        print(
            f"Error al ejecutar la tarea de usuario: {response.status_code}, {response.text}")
        return None

def recoleccion_materiales(mail_recolector, material):
    [x_bonita_api_cookie, jsessionid] = login()

    processes = get_processes(x_bonita_api_cookie, jsessionid)
    process_name = processes[0]['name']

    process_id = find_process_by_name(processes, process_name)

    instantiated_process = instantiate_process(x_bonita_api_cookie, jsessionid, process_id)

    case_id = instantiated_process["caseId"]

    # updateamos las variables de bonita
#    update_case_variable(x_bonita_api_cookie, jsessionid, case_id, 'validacion', 'true', 'java.lang.Boolean')
    update_case_variable(x_bonita_api_cookie, jsessionid, case_id, 'mail_recolector', mail_recolector, 'java.lang.String')
    update_case_variable(x_bonita_api_cookie, jsessionid, case_id, 'material', material, 'java.lang.String')

    
    task_id = get_task_id_by_case_id(x_bonita_api_cookie, jsessionid, case_id)

    assign_user_to_task_id(x_bonita_api_cookie, jsessionid, task_id, USER_ID)

    execute_user_task(x_bonita_api_cookie, jsessionid, task_id)
    return case_id
    
def validar_materiales(case_id, es_cantidad_real):
    print(case_id, es_cantidad_real)
    [x_bonita_api_cookie, jsessionid] = login()
    update_case_variable(x_bonita_api_cookie, jsessionid, case_id, 'validacion', es_cantidad_real, 'java.lang.Boolean')
    task_id = get_task_id_by_case_id(x_bonita_api_cookie, jsessionid, case_id)

    assign_user_to_task_id(x_bonita_api_cookie, jsessionid, task_id, USER_ID)

    execute_user_task(x_bonita_api_cookie, jsessionid, task_id)
