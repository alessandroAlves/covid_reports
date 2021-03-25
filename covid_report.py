from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import requests
import sys

def pull_covid_data(init_date):
    """
    Get data from covid 19 public api. 
    https://documenter.getpostman.com/view/10808728/SzS8rjbc
    """
    url =\
        "https://api.covid19api.com/live/country/brazil/status/confirmed/date/"\
        + init_date.strftime("%Y-%m-%d")\
        + "T00:00:00Z"
    respponse = requests.get(url)
    return respponse


def load_raw_data(init_date, limit_date):
    """ 
    Transform json response to df, filter month and rename columns
    """
    response = pull_covid_data(init_date)
    if response.status_code == 200:
        df = pd.read_json(response.content)
        mask = df["Date"] < limit_date.strftime("%Y-%m-%dT00:00:00Z")
        df = df.loc[mask]
        return df
    else:
        raise(NameError(f"Nao foi poss[vel obter os dados. ERRO: {response}"))


def create_dayly_report(raw):
    """
    Make dataframe with data grouped by day
    """
    df = raw
    df["Date"] = df["Date"].dt.date
    df = df \
        .groupby(["Country", "CountryCode", "Province", "Date"]) \
        .agg({
            "Confirmed" : "max",
            "Deaths" : "max",
            "Recovered" : "max",
            "Active" : "max"  
        })
    return df 


def create_weekly_report(raw):
    """
    Make dataframe with data grouped by week
    """
    df = raw
    df["Week"] = df["Date"].dt.strftime("%V")
    df = df \
        .groupby(["Country", "CountryCode", "Province", "Week"]) \
        .agg(
            Confirmed_AVG = ("Confirmed", "mean"),
            Deaths_AVG = ("Deaths",  "mean"),
            Recoverd_AVG = ("Recovered", "mean"),
            Active_AVG = ("Active", "mean"),
            Confirmed_MIN = ("Confirmed", "min"),
            Deaths_MIN = ("Deaths",  "min"),
            Recoverd_MIN = ("Recovered", "min"),
            Active_MIN = ("Active", "min"), 
            Confirmed_MAX = ("Confirmed", "max"),
            Deaths_MAX = ("Deaths",  "max"),
            Recoverd_MAX = ("Recovered", "max"),
            Active_MAX = ("Active", "max") 
        )
    df["Confirmed"] = df["Confirmed_MAX"] - df["Confirmed_MIN"]
    df["Deaths"] = df["Deaths_MAX"] - df["Deaths_MIN"]
    df["Recoverd"] = df["Recoverd_MAX"] - df["Recoverd_MIN"]
    df["Active"] = df["Active_MAX"] - df["Active_MIN"]
    # Reorder cols
    df = df[[
        "Confirmed",
        "Deaths",
        "Recoverd",
        "Active",
        "Confirmed_AVG",
        "Deaths_AVG",
        "Recoverd_AVG",
        "Active_AVG",
        "Confirmed_MIN",
        "Deaths_MIN",
        "Recoverd_MIN",
        "Active_MIN",
        "Confirmed_MAX",
        "Deaths_MAX",
        "Recoverd_MAX",
        "Active_MAX"
    ]]
    return df 


def write_report(df, path, ref_date, format):
    """
    Create csv report
    """
    if format == "d":
        file_path = path + "/" + ref_date.strftime("%Y-%m") + "_diario.csv"
    else:
        file_path = path + "/" + ref_date.strftime("%Y-%m") + "_semanal.csv"
    
    try:
        df.to_csv(
            path_or_buf=file_path,
            sep="|",
            index=True,
            header=True,
            float_format='%.1f')
        print("""
            + -------------------------------------------- +
            | Relatório disponível no diretório informado. |
            + -------------------------------------------- +
            """)
    except Exception as e:
        print("""
            + ----------------------------------- +
            | Não foi possível salvar o relatório |
            + ----------------------------------- +
            """)
        print(e)
        exit() 


def main():
    # Validate user input path arg
    try: 
        destination_path = str(sys.argv[1])
    except:
        print("""
            Diretório de destino não informado.

            + -------------------------------------------------- +
            | Informe o path de destino do report                |
            |                                                    |
            | python3 covid_report.py [diretorio] [formato[D,S]] |
            + -------------------------------------------------- +
            """)
        exit()
    
    # Validate user input report_format arg
    try:
        report_format = str(sys.argv[2]).lower()
    except:
        print("""
            Formato de relatório não informado

            + -------------------------------------------------- +
            | Informe D para Diário e S para semanal             |
            |                                                    |
            | python3 covid_report.py [diretorio] [formato[D,S]] |
            + -------------------------------------------------- +
            """)
        exit()
    
    if report_format in ["s", "d"]:
        last_month = date.today() + relativedelta(months=-1)
        last_month_start = last_month.replace(day=1)
        month_start = datetime.today().replace(day=1)

        raw = load_raw_data(init_date=last_month_start, limit_date=month_start) 
        
        if report_format == "d":
            df = create_dayly_report(raw)
        else:
            df = create_weekly_report(raw)

        write_report(df, destination_path, last_month, report_format)
        exit()
    else:
        print("""
            Formato de relatório inválido. 
            Opções: 
                - 'D' ou 'd' para diário.
                - 'S' ou 's' para semanal.

            + -------------------------------------------------- +
            | Informe D para Diário e S para semanal             |
            |                                                    |
            | python3 covid_report.py [diretorio] [formato[D,S]] |
            + -------------------------------------------------- +
            """)
        exit()

if __name__ == "__main__":
    main()