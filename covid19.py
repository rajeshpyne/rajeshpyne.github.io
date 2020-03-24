import requests
import json
from pandas import json_normalize
import pandas as pd

url = "https://coronavirus-monitor.p.rapidapi.com/coronavirus/latest_stat_by_country.php"

#querystring = {"country":"India"}
country_list=["India","China","USA"]

headers = {
    'x-rapidapi-host': "coronavirus-monitor.p.rapidapi.com",
    'x-rapidapi-key': "p3sNWKR33HmshSGWi2vxzPFX9LSKp1RGAtZjsn7rCR821QnNHR"
    }

stat_df = pd.DataFrame()
for country_name in country_list:
	response = requests.request("GET", url, headers=headers, params={"country":country_name})

	results = json.loads(response.text)
	country_stat = (results["latest_stat_by_country"][0])

	#print(india_stat["country_name"])
	#print(india_stat["total_cases"])
	#print(country_stat)

	df = json_normalize(country_stat)
	#print(df)
	stat_df = stat_df.append(df,ignore_index=True)
	
print(stat_df.head())
#df.to_csv('india_covid19.csv',index=False)
stat_df = stat_df.drop(columns=["id"])
stat_df = stat_df.rename(columns={"country_name": "Country", "total_cases": "Total Cases","new_cases":"New Cases","active_cases":"Active Cases","total_deaths":"Total Deaths","new_deaths":"New Deaths","total_recovered":"Total Recovered","serious_critical":"Serious Critical","region":"Region","total_cases_per1m":"Total Cases/Million","record_date":"Last Updated(UTC)"})
covid19_html = stat_df.to_html(index=False)

#write html to file
text_file = open("covid19.html", "w")
text_file.write(covid19_html)
text_file.write("<br><br>")
text_file.write("Disclaimer: The data presented is a representation of the data pulled from the api present at https://rapidapi.com/astsiatsko/api/coronavirus-monitor/endpoints")
text_file.close()
