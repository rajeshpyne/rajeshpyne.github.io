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
covid19_html = df.to_html(index=False)

#write html to file
text_file = open("index.html", "w")
text_file.write(covid19_html)
text_file.write("\n")
text_file.write("Disclaimer: I do not take any responsibility for the correctness of the data in this dashboards. The data presented is a representation of the data pulled from the api present at https://rapidapi.com/astsiatsko/api/coronavirus-monitor/endpoints")
text_file.close()
