import streamlit as st 
import PIL as pl
import os
import io


ruta = os.getcwd()
ruta = ruta.replace("\\", "/")
st.set_page_config(layout = "wide")
st.title("\"Análisis de variables climatológicas en Cuba en el período 1990-2022\"")
st.markdown("<hr style='height:10px;border:none;color:#333;background-color:#333;' />", unsafe_allow_html=True)


opciones = ['Introducción', 'Humedad Relativa', 'Precipitaciones', 'Temperatura', "Huracanes y Tormentas Tropicales", "Análisis Multivariado", "Podcast", "Fuentes e Información"]
selección = st.sidebar.radio('Selecciona una opción:', opciones)

#################################################################################################################################
#Introducción
#################################################################################################################################

if selección == 'Introducción':
    col1,col2 = st.columns(2)
    with open(f'{ruta}' + '/images/cubaAI.jpg', 'rb') as f:
        datos_imagen = f.read()
    imagen = pl.Image.open(io.BytesIO(datos_imagen)).resize((900,700))
    col2.image(imagen, use_column_width=True)
    col1.write("""
    El clima de un país tiene un impacto profundo y multifacético en casi todos los aspectos de la vida y la sociedad. En el caso de Cuba, su clima tropical no es una excepción. Desde la economía hasta la cultura, la vida cotidiana hasta la biodiversidad, el impacto del clima es significativo.

En términos económicos, el clima afecta a sectores como la agricultura, la pesca y el turismo. La agricultura, por ejemplo, depende en gran medida de las condiciónes climáticas para el crecimiento de los cultivos. El turismo, una parte vital de la economía cubana, también está estrechamente ligado al clima, ya que los turistas suelen preferir el clima cálido y soleado para sus visitas. Culturalmente, el clima también juega un papel importante. Ha influido en la música, la danza, la literatura y las tradiciónes de la isla. Por ejemplo, muchas canciónes y poemas cubanos hacen referencia al clima y a la belleza natural de la isla. En cuanto a la biodiversidad, el clima tropical de Cuba ha permitido el florecimiento de una rica y diversa vida de plantas y animales. Muchas especies se han adaptado a las condiciónes específicas del clima cubano, lo que ha resultado en una biodiversidad única.""")

    st.write("""En resumen, el clima de Cuba tiene un impacto significativo en la vida en la isla. Conocer y entender las variables climáticas es esencial para apreciar plenamente cómo el clima moldea la vida en Cuba. Este Data Product te permitirá explorar estas variables en profundidad. En este Data Product, nos centraremos en tres variables climatológicas clave: la humedad relativa, las temperaturas y las lluvias.

La **humedad relativa** es una medida de cuánta humedad hay en el aire en comparación con la cantidad máxima de humedad que el aire podría contener a esa temperatura. Esta variable es crucial para entender el confort térmico y puede influir en fenómenos como la formación de nubes y la precipitación.

Las **temperaturas** son una parte integral de cualquier estudio climático. Las temperaturas pueden influir en una variedad de fenómenos, desde los patrones de vida de las plantas y los animales hasta los patrones de asentamiento humano. En un país tropical como Cuba, las temperaturas pueden variar significativamente entre las estaciones secas y húmedas.

Las **precipitaciones** son otra variable climática crucial. La cantidad, la frecuencia y la intensidad de las lluvias pueden tener un impacto significativo en todo, desde el suministro de agua hasta la salud del suelo y la vida vegetal.
             
Además, ofreceremos miradas a relaciones entre estas variables y otras caracteristicas interesantes del clima cubano.

Este Data Product te permitirá explorar estas variables en profundidad. Al entender estas variables y cómo interactúan entre sí, puedes llegar a tus propias conclusiones sobre el clima de Cuba. Ya sea que estés interesado en la meteorología, la geografía, la ecología, o simplemente tengas curiosidad, este Data Product te proporcionará las herramientas para explorar y entender el clima de Cuba a tu propio ritmo. ¡Disfruta explorando!
    """)
    
    st.markdown('')
    st.markdown('')
    st.markdown('### ¿Cómo navegar el Data Product?')
    st.markdown("<hr style='height:5px;border:none;color:#333;background-color:#333;' />", unsafe_allow_html=True)
    st.markdown('''
Arriba a la izquierda, encontrarás un menú desplegable en donde podras elegir que variable quieres explorar. Dentro de cada una de las secciones encontrarás distintos medios de interacción y visualización para hacer mas clara la comprensión de las variables y sus relaciones. Nuestro objetivo es que el usurario reciba claramente los datos que busca, para que pueda utilizarlos por sí mismo para realizar los análisis que necesite.
''')

####################################################################################################################################
#Secciones del DataFrame
####################################################################################################################################


elif selección == 'Humedad Relativa':
    with open(f'{ruta}' + '/Humedad/humedad.py', encoding="UTF-8") as f:
        exec(f.read())

elif selección == 'Precipitaciones':
    with open(f'{ruta}' + '/Precipitaciones/precipitación.py', encoding="UTF-8") as f:
        exec(f.read())

elif selección == 'Temperatura':
    with open(f'{ruta}' + '/temperature/main.py', encoding="UTF-8") as f:
        exec(f.read())

elif selección == "Análisis Multivariado":
    with open(f'{ruta}' + '/Análisis Multivariado/mvanalysis.py', encoding="UTF-8") as f:
        exec(f.read())

elif selección == "Huracanes y Tormentas Tropicales":
    with open(f'{ruta}' + '/Huracanes y Tormentas Tropicales/hurtrops.py', encoding="UTF-8") as f:
        exec(f.read())

elif selección == "Fuentes e Información":
    with open(f'{ruta}' + '/Fuentes e Información/biblio.py', encoding="UTF-8") as f:
        exec(f.read())
        
elif selección == "Podcast":
    with open(f'{ruta}' + '/podcast_web/main.py', encoding="UTF-8") as f:
        exec(f.read())




