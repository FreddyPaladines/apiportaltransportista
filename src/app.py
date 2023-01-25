from flask import Flask

app = Flask(__name__)
@app.route('/')

#python 
#python .\src\app.py

def RespuestaPost():
    import pyodbc
    import pandas as pd
    import json
    server = "Jorgeserver.database.windows.net"
    database = 'DPL' 
    username = 'Jmmc' 
    password = 'ChaosSoldier01'  
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
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


if __name__ == "__main__":
    
    app.run(host='0.0.0.0',
            debug=True,
            port=8080)



