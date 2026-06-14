import streamlit as st
import requests

# 1. Configuración de la página web
st.set_page_config(page_title="Portal Yau - Trámites", page_icon="🏛️", layout="centered")

# 2. Diseño de la cabecera
st.title("🏛️ Municipalidad Provincial de Yau")
st.subheader("Ventanilla Virtual de Trámites con IA")
st.markdown("Ingrese los datos de su solicitud. Nuestro sistema inteligente evaluará y priorizará su trámite en tiempo real para brindarle un servicio más ágil.")
st.divider()

# 3. Formulario interactivo para el ciudadano
with st.form("formulario_tramite"):
    st.write("### 👤 Datos del Solicitante")
    nombres = st.text_input("Nombres y Apellidos Completos")
    correo = st.text_input("Correo Electrónico (Para recibir notificaciones del estado)")
    
    st.write("### 📄 Detalles del Trámite")
    # Colocamos opciones que sabemos que tu modelo de IA ya conoce
    tipo_tramite = st.selectbox("Seleccione el Trámite", [
        "Permiso de Urbanización", 
        "Licencia para Farmacia", 
        "Certificado de Soltería",
        "Registro de Nacionalización",
        "Certificado de Planeamiento Urbano"
    ])
    
    area_asignada = st.selectbox("Área de Destino", [
        "Obras Públicas", 
        "Desarrollo Económico", 
        "Registro Civil", 
        "Cultura", 
        "Desarrollo Urbano"
    ])
    
    col1, col2 = st.columns(2)
    with col1:
        dias_espera = st.number_input("Días de espera promedio histórico (Referencia)", min_value=1, max_value=100, value=15)
    with col2:
        docs_completos = st.radio("¿Cuenta con todos los requisitos adjuntos?", ["Sí", "No"])
        doc_num = 1 if docs_completos == "Sí" else 0

    # Botón principal
    enviado = st.form_submit_button("Enviar Trámite y Evaluar", type="primary", use_container_width=True)

# 4. Lógica de comunicación con tu API
if enviado:
    if not nombres or not correo:
        st.error("Por favor, complete su nombre y correo.")
    else:
        with st.spinner("La Inteligencia Artificial está procesando su solicitud..."):
            # Armamos el JSON que tu API está esperando
            payload = {
                "nombres": nombres,
                "correo_ciudadano": correo,
                "tipo_tramite": tipo_tramite,
                "dias_espera_promedio": dias_espera,
                "documentos_completos": doc_num,
                "area_asignada": area_asignada
            }
            
            # Hacemos la petición a tu API local (FastAPI)
            try:
                respuesta = requests.post("https://portalyau.onrender.com/procesar_y_notificar/", json=payload)
                
                if respuesta.status_code == 200:
                    datos_api = respuesta.json()
                    prioridad = datos_api["prioridad_asignada"]
                    
                    st.success("✅ ¡Trámite ingresado con éxito al sistema municipal!")
                    
                    # Mostrar resultados visuales atractivos
                    st.divider()
                    st.write("### Resultados del Análisis IA")
                    if prioridad == "Alta":
                        st.error(f"🚀 **Prioridad Asignada:** {prioridad} (Atención Urgente)")
                    elif prioridad == "Media":
                        st.warning(f"⚡ **Prioridad Asignada:** {prioridad} (Atención Regular)")
                    else:
                        st.info(f"⏳ **Prioridad Asignada:** {prioridad} (Atención Estándar)")
                        
                    st.info(f"📧 Se ha enviado una notificación automática a: **{correo}**")
                else:
                    st.error(f"Error en los datos: {respuesta.json().get('detail', 'Revise los campos')}")
            except Exception as e:
                st.error("Error de conexión. Asegúrese de que el servidor FastAPI esté encendido en la otra terminal.")