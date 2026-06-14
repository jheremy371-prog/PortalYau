from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
from datetime import datetime

# 1. Inicializar la aplicación FastAPI
app = FastAPI(
    title="API - Gestor Inteligente de Trámites de Yau",
    description="Motor de Machine Learning con Sistema de Alertas Automáticas."
)

# 2. Cargar el motor de IA
print("Cargando el motor de IA...")
try:
    modelo = joblib.load('modelo_prioridad_tramites.pkl')
    le_tramite = joblib.load('encoder_tramite.pkl')
    le_area = joblib.load('encoder_area.pkl')
except Exception as e:
    print(f"Error al cargar los archivos .pkl: {e}")

# 3. Nueva estructura de datos (¡Ahora pedimos el correo del ciudadano!)
class TramiteCiudadano(BaseModel):
    nombres: str
    correo_ciudadano: str
    tipo_tramite: str
    dias_espera_promedio: int
    documentos_completos: int
    area_asignada: str

# 4. Módulo de Alertas Automatizadas
def enviar_alerta_ciudadano(nombre: str, correo: str, tramite: str, prioridad: str):
    """
    Simula la conexión a un servidor SMTP (como SendGrid o Gmail) 
    para enviar una notificación en tiempo real.
    """
    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
    mensaje_correo = f"""
    ===================================================
    📧 NUEVA ALERTA ENVIADA
    Para: {correo}
    Fecha: {fecha_actual}
    
    Hola, {nombre}.
    Tu solicitud para el trámite '{tramite}' ha sido ingresada al sistema.
    Debido a nuestra nueva gestión impulsada por IA, tu trámite 
    ha sido clasificado con prioridad: {prioridad.upper()}.
    
    Te notificaremos por este medio ante cualquier cambio de estado.
    ===================================================
    """
    # En un entorno real, aquí va el código de envío (ej. smtplib).
    # Por ahora, lo imprimimos en la consola del servidor para dejar evidencia.
    print(mensaje_correo)
    return True

# 5. Endpoint Principal
@app.post("/procesar_y_notificar/")
def procesar_y_notificar(tramite: TramiteCiudadano):
    try:
        # Convertir texto a números
        tramite_num = le_tramite.transform([tramite.tipo_tramite])[0]
        area_num = le_area.transform([tramite.area_asignada])[0]
        
        # Preparar datos para la predicción
        datos_entrada = pd.DataFrame([[
            tramite_num, 
            tramite.dias_espera_promedio, 
            tramite.documentos_completos, 
            area_num
        ]], columns=['tipo_tramite_num', 'dias_espera_promedio', 'documentos_completos', 'area_asignada_num'])
        
        # Generar la predicción con Machine Learning
        prioridad = modelo.predict(datos_entrada)[0]
        
        # Disparar el sistema de alertas
        enviar_alerta_ciudadano(
            nombre=tramite.nombres,
            correo=tramite.correo_ciudadano,
            tramite=tramite.tipo_tramite,
            prioridad=prioridad
        )
        
        # Retornar respuesta al Frontend
        return {
            "estado": "éxito",
            "mensaje": "Trámite procesado y ciudadano notificado correctamente.",
            "prioridad_asignada": prioridad,
            "alerta_enviada_a": tramite.correo_ciudadano
        }
        
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=f"Error en los datos: El tipo de trámite o área no existe en el sistema.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")