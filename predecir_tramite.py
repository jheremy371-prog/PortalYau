import joblib
import pandas as pd

# Cargar el modelo y los codificadores guardados
modelo = joblib.load('modelo_prioridad_tramites.pkl')
le_tramite = joblib.load('encoder_tramite.pkl')
le_area = joblib.load('encoder_area.pkl')

# Simular un NUEVO trámite ingresado por un ciudadano en el sistema
nuevo_tramite = {
    'tipo_tramite': 'Permiso de Urbanización',
    'dias_espera_promedio': 45, 
    'documentos_completos': 0,  
    'area_asignada': 'Obras Públicas'
}

# Convertir el texto a números usando los mismos codificadores
tramite_num = le_tramite.transform([nuevo_tramite['tipo_tramite']])[0]
area_num = le_area.transform([nuevo_tramite['area_asignada']])[0]

# Preparar los datos para la predicción
datos_prediccion = pd.DataFrame([[
    tramite_num, 
    nuevo_tramite['dias_espera_promedio'], 
    nuevo_tramite['documentos_completos'], 
    area_num
]], columns=['tipo_tramite_num', 'dias_espera_promedio', 'documentos_completos', 'area_asignada_num'])

# Hacer la predicción
prioridad_predicha = modelo.predict(datos_prediccion)

print(f"El sistema automatizado ha clasificado este nuevo trámite con Prioridad: {prioridad_predicha[0]}")