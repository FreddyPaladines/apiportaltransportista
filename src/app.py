from flask import Flask,request,jsonify
import pyodbc

import json
app = Flask(__name__)

server = "Jorgeserver.database.windows.net"
database = 'DPL' 
username = 'Jmmc' 
password = 'ChaosSoldier01'  
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)




@app.route('/')
#python .\src\app.py
def RespuestaPost():
    import pandas as pd

    cursor = cnxn.cursor()
    queryIEES = "SELECT * FROM [citas].[PRTAL_Transportistas]"
    queryRegistroPenal = "SELECT * FROM [citas].[RegistroPenal]"
    df_IESS = pd.read_sql(queryIEES, cnxn)
    df_RegistroPenal=pd.read_sql(queryRegistroPenal, cnxn)
    df=pd.merge(df_IESS,df_RegistroPenal, how="left")
    df= df.fillna("")



    
    result=df.to_json(orient="records",date_format="iso")
    parsed = json.loads(result)
    pd=json.dumps(parsed, indent=4) 

    

    return pd

#--------Prueba post--------------------
@app.route('/seguridad', methods=['POST'])
def registrar_curso():
    try:
        cursor = cnxn.cursor()
        sql="""insert into citas.FormularioSeguridad_Resultados (Cedula,Fecha,Estado,Puntuacion)
                values ('{0}','{1}','{2}',{3})""".format(request.json['cedula'],request.json['Fecha'],request.json['Estado'],request.json['Puntuacion'])
        cursor.execute()
        cnxn.commit()
        return jsonify({'mensaje':"Curso registrado"})
    except Exception as ex:
        return jsonify({'mensaje':"Error"})



if __name__ == "__main__":
    
    app.run(host='0.0.0.0',
            debug=True,
            port=8080)



