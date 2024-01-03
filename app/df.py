
import pandas as pd

df = pd.read_excel("./data/data.xlsx")

nombres_estaciónes = {
    78310:"Cabo de San Antonio.Pinar del Río",
    78315:"Pinar del Río Ciudad",
    78318:"Bahía Honda.Artemisa",
    78320:"Güira de Melena.Artemisa",
    78321:"Santa Fe.Isla de la Juventud",
    78323:"Güines.Mayabeque",
    78328:"Varadero.Matanzas",
    78330:"Jovellanos.Matanzas",
    78333:"Playa Girón.Matanzas",
    78344:"Cienfuegos Ciudad",
    78343:"El Yabú.Santa Clara",
    78349:"Sancti Spíritus Ciudad",
    78346:"Venezuela.Ciego de Ávila",
    78339:"Cayo Coco.Ciego de Ávila",
    78355:"Camagüey Ciudad",
    78351:"Santa Cruz del Sur.Camagüey",
    78357:"Las Tunas Ciudad",
    78372:"Pedagogico.Holguín",
    78365:"Cabo Lucrecia.Holguín",
    78377:"Veguitas.Granma",
    78360:"Cabo Cruz.Granma",
    78371:"Pinares de Mayarí.Holguín",
    78364:"Universidad.Santiago de Cuba",
    78368:"Guantánamo Ciudad",
    78369:"Punta de Maisí.Guantánamo",
    78325:"Casablanca.La Habana"
}

df["Nombres Estaciónes"] = df["Estación"].replace(nombres_estaciónes)





latitudes = {
    78310:21.86307,
    78315:22.41425,
    78318:22.91454,
    78320:22.79683,
    78321:21.74313,
    78323:22.84336,
    78328:23.14319,
    78330:22.80816,
    78333:22.06881,
    78344:22.16039,
    78343:22.45247,
    78349:21.93292,
    78346:21.74284,
    78339:22.50907,
    78355:21.39274,
    78351:20.71562,
    78357:20.95792,
    78372:20.88454,
    78365:21.07219,
    78377:20.30817,
    78360:19.84707,
    78371:20.48392,
    78364:20.03132,
    78368:20.14,
    78369:20.22579,
    78325:23.14673

}




df["Latitud"] = df["Estación"].replace(latitudes)






longitudes = {
    78310:-84.95083,
    78315:-83.69072,
    78318:-83.16144,
    78320:-82.51408,
    78321:-82.75601,
    78323:-82.025231,
    78328:-81.26677,
    78330:-81.19439,
    78333:-81.02466,
    78344:-80.44002,
    78343:-80.01739,
    78349:-80.01739,
    78346:-78.78864,
    78339:-78.40828,
    78355:-77.90616,
    78351:-77.99387,
    78357:-76.95280 ,
    78372:-76.22091,
    78365:-75.62036,
    78377:-76.90400,
    78360:-77.72011,
    78371:-75.80345,
    78364:-75.81282,
    78368:-75.2129,
    78369:-74.15279,
    78325:-82.33209


}




df["Longitud"] = df["Estación"].replace(longitudes)











regiónes  = {
    78310:"Occidente",
    78315:"Occidente",
    78318:"Occidente",
    78320:"Occidente",
    78321:"Isla de la Juventud",
    78323:"Occidente",
    78328:"Occidente",
    78330:"Occidente",
    78333:"Occidente",
    78344:"Centro",
    78343:"Centro",
    78349:"Centro",
    78346:"Centro",
    78339:"Centro",
    78355:"Centro",
    78351:"Centro",
    78357:"Oriente",
    78372:"Oriente",
    78365:"Oriente",
    78377:"Oriente",
    78360:"Oriente",
    78371:"Oriente",
    78364:"Oriente",
    78368:"Oriente",
    78369:"Oriente",
    78325:"Occidente"


}




df["Región"] = df["Estación"].replace(regiónes)







#Convertir a archivo csv 
df.to_csv("./data/base_datos.csv",index=False)

