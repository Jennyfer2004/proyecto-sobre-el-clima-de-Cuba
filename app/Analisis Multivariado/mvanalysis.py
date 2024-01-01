import streamlit as st 
import pandas as pd
import sys
import os
ruta = os.getcwd()
ruta = ruta.replace("\\", "/")
sys.path.append(f'{ruta}' + '/Analisis Multivariado')
import mvLogic

st.title("Análisis Multivariado")

df = pd.read_csv("./data/base_datos.csv")
df = df.loc[:, ["Estacion", "Año", "Mes", "Temperatura max med", "Temperatura min med", "Temperatura med", "Humedad Relat", "Precipitaciones",
        "Nombres Estaciones", "Latitud", "Longitud", "Región", "Provincias"]]

df = df.rename(columns={"Temperatura max med": "Temperatura Maxima Media", "Temperatura min med": "Temperatura Minima Media", "Temperatura med": "Temperatura Media", "Humedad Relat": "Humedad Relativa",
        "Nombres Estaciones": "Nombre de Estacion"})

df_Occidente = df.loc[df['Región'] == 'Occidente']
df_Centro = df.loc[df['Región'] == 'Centro']
df_Oriente = df.loc[df['Región'] == 'Oriente']

df_Pdr = df.loc[df['Provincias'] == 'Pinar del Río'] 
df_Art = df.loc[df['Provincias'] == 'Artemisa']
df_Hab = df.loc[df['Provincias'] == 'La Habana']
df_May = df.loc[df['Provincias'] == 'Mayabeque']
df_Mat = df.loc[df['Provincias'] == 'Matanzas']
df_Vcl = df.loc[df['Provincias'] == 'Villa Clara']
df_Cfg = df.loc[df['Provincias'] == 'Cienfuegos']
df_Ssp = df.loc[df['Provincias'] == 'Sancti Spirítus'] 
df_Cav = df.loc[df['Provincias'] == 'Ciego de Ávila']
df_Cam = df.loc[df['Provincias'] == 'Camagüey']
df_Ltu = df.loc[df['Provincias'] == 'Las Tunas']
df_Hol = df.loc[df['Provincias'] == 'Holguín']
df_Gra = df.loc[df['Provincias'] == 'Granma']
df_Sdc = df.loc[df['Provincias'] == 'Santiago de Cuba']
df_Gua = df.loc[df['Provincias'] == 'Guantánamo']

a = st.markdown("## Seleccione la region en la que quiere explorar datos")

opciones = ['General', 'Occidente', 'Centro', 'Oriente']
seleccion = st.selectbox('Selecciona una Región:', opciones)

######################################################################################################################################################################################
#Analisis Multivariado General
######################################################################################################################################################################################

if seleccion == "General":
    
        st.markdown("### Coeficiente de Correlación entre las variables")
        df_corr = df[["Temperatura Media", "Temperatura Maxima Media", "Temperatura Minima Media", "Humedad Relativa", "Precipitaciones"]]
        st.write(df_corr.corr()) 

        st.markdown("### Graficos de Dispersión")
        mvLogic.ScatLogic(df)

        st.markdown("### Graficos de Regresión Lineal")
        mvLogic.RegLogic(df)


###########################################################################################################################################################################
#Analisis Multivariado Occidente
############################################################################################################################################################################
    
if seleccion == "Occidente":

        opciones = ['General', 'Pinar del Río', 'Artemisa', 'La Habana', 'Mayabeque', 'Matanzas']
        seleccion = st.selectbox('Selecciona una Provincia:', opciones)

        

################################################
#GENERAL
################################################
        if seleccion == 'General':      

                st.markdown("### Coeficiente de Correlación entre las variables")
                df_corr = df_Occidente[["Temperatura Media", "Temperatura Maxima Media", "Temperatura Minima Media", "Humedad Relativa", "Precipitaciones"]]
                st.write(df_corr.corr()) 

                st.markdown("### Graficos de Dispersión")
                mvLogic.ScatLogic(df_Occidente)

                st.markdown("### Graficos de Regresión Lineal")
                mvLogic.RegLogic(df_Occidente)


###############################################
#PINAR DEL Río
###############################################

        elif seleccion == 'Pinar del Río':    

                st.markdown("### Coeficiente de Correlación entre las variables")
                df_corr = df_Pdr[["Temperatura Media", "Temperatura Maxima Media", "Temperatura Minima Media", "Humedad Relativa", "Precipitaciones"]]
                st.write(df_corr.corr()) 

                st.markdown("### Graficos de Dispersión")
                mvLogic.ScatLogic(df_Pdr)

                st.markdown("### Graficos de Regresión Lineal")
                mvLogic.RegLogic(df_Pdr)

###############################################
#ARTEMISA
###############################################

        elif seleccion == 'Artemisa':

                st.markdown("### Coeficiente de Correlación entre las variables")
                df_corr = df_Art[["Temperatura Media", "Temperatura Maxima Media", "Temperatura Minima Media", "Humedad Relativa", "Precipitaciones"]]
                st.write(df_corr.corr()) 

                st.markdown("### Graficos de Dispersión")
                mvLogic.ScatLogic(df_Art)

                st.markdown("### Graficos de Regresión Lineal")
                mvLogic.RegLogic(df_Art)

###############################################
#La HABANA
###############################################

        elif seleccion == 'La Habana':

                st.markdown("### Coeficiente de Correlación entre las variables")
                df_corr = df_Hab[["Temperatura Media", "Temperatura Maxima Media", "Temperatura Minima Media", "Humedad Relativa", "Precipitaciones"]]
                st.write(df_corr.corr()) 

                st.markdown("### Graficos de Dispersión")
                mvLogic.ScatLogic(df_Hab)

                st.markdown("### Graficos de Regresión Lineal")
                mvLogic.RegLogic(df_Hab)

###############################################
#MAYABEQUE
###############################################

        elif seleccion == 'Mayabeque':

                st.markdown("### Coeficiente de Correlación entre las variables")
                df_corr = df_May[["Temperatura Media", "Temperatura Maxima Media", "Temperatura Minima Media", "Humedad Relativa", "Precipitaciones"]]
                st.write(df_corr.corr()) 

                st.markdown("### Graficos de Dispersión")
                mvLogic.ScatLogic(df_May)

                st.markdown("### Graficos de Regresión Lineal")
                mvLogic.RegLogic(df_May)

###############################################
#MATANZAS
###############################################

        elif seleccion == 'Matanzas':

                st.markdown("### Coeficiente de Correlación entre las variables")
                df_corr = df_Mat[["Temperatura Media", "Temperatura Maxima Media", "Temperatura Minima Media", "Humedad Relativa", "Precipitaciones"]]
                st.write(df_corr.corr()) 

                st.markdown("### Graficos de Dispersión")
                mvLogic.ScatLogic(df_Mat)

                st.markdown("### Graficos de Regresión Lineal")
                mvLogic.RegLogic(df_Mat)


##################################################################################################################################
#Analisis Multivariado Centro
##################################################################################################################################
    
if seleccion == "Centro":

        opciones = ['General', 'Villa Clara', 'Cienfuegos', 'Sancti Spíritus', 'Ciego de Ávila', 'Camagüey']
        seleccion = st.selectbox('Selecciona una Provincia:', opciones)

        
################################################
#GENERAL
################################################
        if seleccion == 'General':      

                st.markdown("### Coeficiente de Correlación entre las variables")
                df_corr = df_Centro[["Temperatura Media", "Temperatura Maxima Media", "Temperatura Minima Media", "Humedad Relativa", "Precipitaciones"]]
                st.write(df_corr.corr()) 

                st.markdown("### Graficos de Dispersión")
                mvLogic.ScatLogic(df_Centro)

                st.markdown("### Graficos de Regresión Lineal")
                mvLogic.RegLogic(df_Centro)

################################################
#Villa Clara
################################################
        if seleccion == 'General':      

                st.markdown("### Coeficiente de Correlación entre las variables")
                df_corr = df_Vcl[["Temperatura Media", "Temperatura Maxima Media", "Temperatura Minima Media", "Humedad Relativa", "Precipitaciones"]]
                st.write(df_corr.corr()) 

                st.markdown("### Graficos de Dispersión")
                mvLogic.ScatLogic(df_Vcl)

                st.markdown("### Graficos de Regresión Lineal")
                mvLogic.RegLogic(df_Vcl)

################################################
#CIENFUEGOS
################################################
        if seleccion == 'Cienfuegos':      

                st.markdown("### Coeficiente de Correlación entre las variables")
                df_corr = df_Cfg[["Temperatura Media", "Temperatura Maxima Media", "Temperatura Minima Media", "Humedad Relativa", "Precipitaciones"]]
                st.write(df_corr.corr()) 

                st.markdown("### Graficos de Dispersión")
                mvLogic.ScatLogic(df_Cfg)

                st.markdown("### Graficos de Regresión Lineal")
                mvLogic.RegLogic(df_Cfg)


################################################
#SANCTI SPS
################################################
        if seleccion == 'Sancti Spíritus':      

                st.markdown("### Coeficiente de Correlación entre las variables")
                df_corr = df_Ssp[["Temperatura Media", "Temperatura Maxima Media", "Temperatura Minima Media", "Humedad Relativa", "Precipitaciones"]]
                st.write(df_corr.corr()) 

                st.markdown("### Graficos de Dispersión")
                mvLogic.ScatLogic(df_Ssp)

                st.markdown("### Graficos de Regresión Lineal")
                mvLogic.RegLogic(df_Ssp)

################################################
#CIEGO DE ÁviLA
################################################
        if seleccion == 'Ciego de Ávila':      

                st.markdown("### Coeficiente de Correlación entre las variables")
                df_corr = df_Cav[["Temperatura Media", "Temperatura Maxima Media", "Temperatura Minima Media", "Humedad Relativa", "Precipitaciones"]]
                st.write(df_corr.corr()) 

                st.markdown("### Graficos de Dispersión")
                mvLogic.ScatLogic(df_Cav)

                st.markdown("### Graficos de Regresión Lineal")
                mvLogic.RegLogic(df_Cav)

################################################
#Camagüey
################################################
                
        if seleccion == 'Camagüey':      

                st.markdown("### Coeficiente de Correlación entre las variables")
                df_corr = df_Cam[["Temperatura Media", "Temperatura Maxima Media", "Temperatura Minima Media", "Humedad Relativa", "Precipitaciones"]]
                st.write(df_corr.corr()) 

                st.markdown("### Graficos de Dispersión")
                mvLogic.ScatLogic(df_Cam)

                st.markdown("### Graficos de Regresión Lineal")
                mvLogic.RegLogic(df_Cam)



##################################################################################################################################
#Analisis Multivariado Oriente
##################################################################################################################################
    
if seleccion == "Oriente":

        opciones = ['General', 'Las Tunas', 'Granma', 'Holguín', 'Santiago de Cuba', 'Guantánamo']
        seleccion = st.selectbox('Selecciona una Provincia:', opciones)

        

################################################
#GENERAL
################################################
        if seleccion == 'General':      

                st.markdown("### Coeficiente de Correlación entre las variables")
                df_corr = df_Occidente[["Temperatura Media", "Temperatura Maxima Media", "Temperatura Minima Media", "Humedad Relativa", "Precipitaciones"]]
                st.write(df_corr.corr()) 

                st.markdown("### Graficos de Dispersión")
                mvLogic.ScatLogic(df_Occidente)

                st.markdown("### Graficos de Regresión Lineal")
                mvLogic.RegLogic(df_Occidente)

################################################
#LAS TUNAS
################################################
        if seleccion == 'Las Tunas':      

                st.markdown("### Coeficiente de Correlación entre las variables")
                df_corr = df_Ltu[["Temperatura Media", "Temperatura Maxima Media", "Temperatura Minima Media", "Humedad Relativa", "Precipitaciones"]]
                st.write(df_corr.corr()) 

                st.markdown("### Graficos de Dispersión")
                mvLogic.ScatLogic(df_Ltu)

                st.markdown("### Graficos de Regresión Lineal")
                mvLogic.RegLogic(df_Ltu)

################################################
#Holguín
################################################
        if seleccion == 'Holguín':      

                st.markdown("### Coeficiente de Correlación entre las variables")
                df_corr = df_Hol[["Temperatura Media", "Temperatura Maxima Media", "Temperatura Minima Media", "Humedad Relativa", "Precipitaciones"]]
                st.write(df_corr.corr()) 

                st.markdown("### Graficos de Dispersión")
                mvLogic.ScatLogic(df_Hol)

                st.markdown("### Graficos de Regresión Lineal")
                mvLogic.RegLogic(df_Hol)

################################################
#GRANMA
################################################
        if seleccion == 'Granma':      

                st.markdown("### Coeficiente de Correlación entre las variables")
                df_corr = df_Gra[["Temperatura Media", "Temperatura Maxima Media", "Temperatura Minima Media", "Humedad Relativa", "Precipitaciones"]]
                st.write(df_corr.corr()) 

                st.markdown("### Graficos de Dispersión")
                mvLogic.ScatLogic(df_Gra)

                st.markdown("### Graficos de Regresión Lineal")
                mvLogic.RegLogic(df_Gra)

################################################
#SANTIAGO DE CUBA
################################################
        if seleccion == 'Santiago de Cuba':      

                st.markdown("### Coeficiente de Correlación entre las variables")
                df_corr = df_Sdc[["Temperatura Media", "Temperatura Maxima Media", "Temperatura Minima Media", "Humedad Relativa", "Precipitaciones"]]
                st.write(df_corr.corr()) 

                st.markdown("### Graficos de Dispersión")
                mvLogic.ScatLogic(df_Sdc)

                st.markdown("### Graficos de Regresión Lineal")
                mvLogic.RegLogic(df_Sdc)

################################################
#GUANtánamO
################################################
        if seleccion == 'Guantánamo':      

                st.markdown("### Coeficiente de Correlación entre las variables")
                df_corr = df_Gua[["Temperatura Media", "Temperatura Maxima Media", "Temperatura Minima Media", "Humedad Relativa", "Precipitaciones"]]
                st.write(df_corr.corr()) 

                st.markdown("### Graficos de Dispersión")
                mvLogic.ScatLogic(df_Gua)

                st.markdown("### Graficos de Regresión Lineal")
                mvLogic.RegLogic(df_Gua)
