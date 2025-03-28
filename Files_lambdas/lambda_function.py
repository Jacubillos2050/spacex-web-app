import json
import requests
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('SpaceXLaunches')

def get_rockets():
    """Obtiene un diccionario de rocket_id a rocket_name desde la API de SpaceX."""
    try:
        response = requests.get('https://api.spacexdata.com/v4/rockets')
        response.raise_for_status()
        rockets = response.json()
        return {rocket['id']: rocket['name'] for rocket in rockets}
    except requests.RequestException as e:
        print(f"Error al obtener cohetes: {str(e)}")
        return {}

def get_launches():
    """Obtiene la lista de lanzamientos desde la API de SpaceX."""
    try:
        response = requests.get('https://api.spacexdata.com/v4/launches')
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error al obtener lanzamientos: {str(e)}")
        return []

def determine_status(launch_date_utc, success):
    """Determina el estado del lanzamiento basado en la fecha y éxito."""
    if not launch_date_utc:
        return 'upcoming'
    launch_date = datetime.strptime(launch_date_utc, '%Y-%m-%dT%H:%M:%S.%fZ')
    current_date = datetime.utcnow()
    if launch_date > current_date:
        return 'upcoming'
    return 'success' if success else 'failed'

def lambda_handler(event, context):
    """Manejador principal de la función Lambda."""
    is_manual = not event  # Si event está vacío, es una invocación manual
    rocket_names = get_rockets()
    launches = get_launches()
    new_count = 0
    updated_count = 0
    processed_launches = []

    for launch in launches:
        launch_id = launch.get('id', '')
        if not launch_id:
            continue  # Saltar si no hay ID

        mission_name = launch.get('name', 'Unknown')
        rocket_id = launch.get('rocket', '')
        rocket_name = rocket_names.get(rocket_id, 'Unknown')
        launch_date_utc = launch.get('date_utc')
        success = launch.get('success') if launch_date_utc else None
        status = determine_status(launch_date_utc, success)

        item = {
            'launch_id': launch_id,
            'mission_name': mission_name,
            'rocket_name': rocket_name,
            'launch_date': launch_date_utc if launch_date_utc else 'N/A',
            'status': status
        }

        try:
            # Verificar si el item ya existe para contar nuevos vs actualizados
            existing_item = table.get_item(Key={'launch_id': launch_id}).get('Item')
            table.put_item(Item=item)  # PutItem sobrescribe si existe (upsert)
            
            if is_manual:
                processed_launches.append({
                    'launch_id': launch_id,
                    'mission_name': mission_name,
                    'status': status
                })
            if not existing_item:
                new_count += 1
            else:
                updated_count += 1
        except Exception as e:
            print(f"Error al procesar lanzamiento {launch_id}: {str(e)}")

    if is_manual:
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Procesamiento completado',
                'new_launches': new_count,
                'updated_launches': updated_count,
                'processed': processed_launches
            })
        }

    return {
        'statusCode': 200,
        'body': json.dumps('Procesamiento exitoso')
    }