import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
import joblib

# 1. Cargar los datos históricos
print("Cargando datos...")
df = pd.read_csv('tramites_historicos.csv')

# 2. Preprocesamiento de datos
# Convertimos las variables de texto a números para que el modelo pueda entenderlas
le_tramite = LabelEncoder()
le_area = LabelEncoder()

df['tipo_tramite_num'] = le_tramite.fit_transform(df['tipo_tramite'])
df['area_asignada_num'] = le_area.fit_transform(df['area_asignada'])

# Definimos nuestras características (X) y lo que queremos predecir (y)
X = df[['tipo_tramite_num', 'dias_espera_promedio', 'documentos_completos', 'area_asignada_num']]
y = df['prioridad_asignada']

# Dividimos los datos: 80% para entrenar el modelo, 20% para probarlo
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Entrenar el Modelo
print("Entrenando el modelo Random Forest...")
modelo = RandomForestClassifier(n_estimators=100, random_state=42)
modelo.fit(X_train, y_train)

# 4. Evaluar el Modelo
predicciones = modelo.predict(X_test)
precision = accuracy_score(y_test, predicciones)
print(f"\nPrecisión del modelo: {precision * 100:.2f}%")
print("\nReporte de Clasificación:")
print(classification_report(y_test, predicciones))

# 5. Exportar el Modelo Entrenado
print("\nGuardando el modelo y los codificadores...")
joblib.dump(modelo, 'modelo_prioridad_tramites.pkl')
joblib.dump(le_tramite, 'encoder_tramite.pkl')
joblib.dump(le_area, 'encoder_area.pkl')

print("¡Modelo exportado con éxito! Listo para integrarse al sistema de la municipalidad.")