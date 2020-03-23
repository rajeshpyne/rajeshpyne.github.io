import requests
import json
from pandas import json_normalize

url = "https://coronavirus-monitor.p.rapidapi.com/coronavirus/latest_stat_by_country.php"

querystring = {"country":"India"}

headers = {
    'x-rapidapi-host': "coronavirus-monitor.p.rapidapi.com",
    'x-rapidapi-key': "p3sNWKR33HmshSGWi2vxzPFX9LSKp1RGAtZjsn7rCR821QnNHR"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

results = json.loads(response.text)
india_stat = (results["latest_stat_by_country"][0])

#print(india_stat["country_name"])
#print(india_stat["total_cases"])

df = (json_normalize(india_stat))
#print(df.info())
#df.to_csv('india_covid19.csv',index=False)
df = df.drop(columns=["id"])
df = df.rename(columns={"country_name": "Country", "total_cases": "Total Cases","new_cases":"New Cases","active_cases":"Active Cases","total_deaths":"Total Deaths","new_deaths":"New Deaths","total_recovered":"Total Recovered","serious_critical":"Serious Critical","region":"Region","total_cases_per1m":"Total Cases/Million","record_date":"Last Updated(UTC)"})
covid19_html = df.to_html(index=False)

#write html to file
text_file = open("covid19.html", "w")
text_file.write(covid19_html)
text_file.write("\n\n\n")
text_file.write("Disclaimer: The data presented is a representation of the data pulled from the api present at https://rapidapi.com/astsiatsko/api/coronavirus-monitor/endpoints")
text_file.close()
