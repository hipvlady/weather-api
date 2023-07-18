from flask import Flask, render_template
import pandas as pd
app = Flask(__name__)

stations_list = "data_small/stations.txt"
stations = pd.read_csv(stations_list, skiprows=17, on_bad_lines='skip')
stations = stations[["STAID","STANAME                                 "]]


@app.route('/')
def home():
    # Use a breakpoint in the code line below to debug your script.
    return render_template("index.html", data=stations.to_html())


@app.route('/api/v1/<station>/<date>')
def get_station_date_data(station, date):
    # Use a breakpoint in the code line below to debug your script.
    filename = "data_small/TG_STAID"+str(station).zfill(6)+".txt"
    df = pd.read_csv(filename, skiprows=20, on_bad_lines='skip', parse_dates=["    DATE"])
    temperature = df.loc[df["    DATE"] == date, "   TG"].squeeze() / 10
    return {"station":station, "date":date, "temperature": temperature}


@app.route('/api/v1/<station>')
def get_station_all_data(station):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, on_bad_lines='skip', parse_dates=["    DATE"])
    result = df.to_dict(orient="records")
    return result


@app.route("/api/v1/annual/<station>/<year>")
def get_station_annual_data(station, year):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, on_bad_lines='skip', parse_dates=["    DATE"])
    df["    DATE"] = df["    DATE"].astype(str)
    result = df[df["    DATE"].str.startswith(str(year))].to_dict(orient="records")
    return result


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)
