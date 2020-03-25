import requests
import json
from pandas import json_normalize
import pandas as pd


def rapidapi_monitor(rapidapi_url):
	url = rapidapi_url
	#querystring = {"country":"India"}
	country_list=["India","China","USA","Iran","Italy","France","Germany"]

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
	#return stat_df
	stat_df = stat_df.drop(columns=["id"])
	stat_df = stat_df.rename(columns={"country_name": "Country", "total_cases": "Total Cases","new_cases":"New Cases","active_cases":"Active Cases","total_deaths":"Total Deaths","new_deaths":"New Deaths","total_recovered":"Total Recovered","serious_critical":"Serious Critical","region":"Region","total_cases_per1m":"Total Cases/Million","record_date":"Last Updated(UTC)"})
	covid19_html = stat_df.to_html(index=False)

	#write html to file
	text_file = open("covid19.html", "w")
	text_file.write(covid19_html)
	text_file.write("<br><br>")
	text_file.write("Disclaimer: The data presented is a representation of the data pulled from the api present at https://rapidapi.com/astsiatsko/api/coronavirus-monitor/endpoints")
	text_file.close()


def agg_stat_api(rootnet_agg_stat_api):
	url = rootnet_agg_stat_api

	response = requests.request("GET", url)
	results = json.loads(response.text)

	summary = results["data"]["summary"]
	summary.update({"last_updated": results["lastRefreshed"]})
	#last_updated = results["lastRefreshed"]
	summary_df = json_normalize(summary)
	summary_df = summary_df.rename(columns={"total":"Total Confirmed Cases",
						"confirmedCasesIndian":"Total Confirmed Cases(Indian)",
						"confirmedCasesForeign":"Total Confirmed Cases(Foreigner)",
						"discharged":"Total Discharged",
						"deaths":"Total Deaths",
						"confirmedButLocationUnidentified":"Confirmed (Missing)",
						"last_updated":"Last Updated(UTC)"})
	print(summary_df)
	indian_covid19_summary_html = summary_df.to_html(index=False)

	states_stat = results["data"]["regional"]
	indian_state_df = pd.DataFrame(columns=["State","Confirmed Cases(Indian)","Confirmed Cases(Foreigner)","Discharged","Deaths"])
	for state_index in range(len(states_stat)):
		state = (states_stat[state_index]["loc"])
		confirmed_indian = (states_stat[state_index]["confirmedCasesIndian"])
		confirmed_foreigner = (states_stat[state_index]["confirmedCasesForeign"])
		discharged = (states_stat[state_index]["discharged"])
		deaths = (states_stat[state_index]["deaths"])
		indian_state_df.loc[state_index] = [state,confirmed_indian,confirmed_foreigner,discharged,deaths]
	print(indian_state_df)
	indian_stat_agg_html = indian_state_df.to_html(index=False)
	text_file = open("indian_state_agg.html", "w")
	text_file.write("<br><br>")
	text_file.write(indian_covid19_summary_html)
	text_file.write("<br><br>")
	text_file.write(indian_stat_agg_html)
	text_file.write("<br><br>")
	text_file.write("Disclaimer: The data presented is a representation of the data pulled from https://www.mohfw.gov.in/")
	text_file.close()


def agg_hospital_stat(rootnet_hospital_bed_stat_api):
	url = rootnet_hospital_bed_stat_api

	response = requests.request("GET", url)
	results = json.loads(response.text)

	summary = results["data"]["summary"]
	summary.update({"last_updated": results["lastRefreshed"]})
	#last_updated = results["lastRefreshed"]
	summary_df = json_normalize(summary)
	summary_df = summary_df.rename(columns={"totalBeds":"Total Beds",
						"totalHospitals":"Total Hospitals",
						"urbanBeds":"Urban Total Beds",
						"urbanHospitals":"Urban Total Hospitals",
						"ruralBeds":"Rural Total Beds",
						"ruralHospitals":"Rural Total Hospitals",
						"last_updated":"Last Updated(UTC)"})
	print(summary_df)
	indian_hospital_summary_html = summary_df.to_html(index=False)

	states_stat = results["data"]["regional"]
	indian_hospitals_df = pd.DataFrame(columns=["State","Rural Hospitals","Rural Beds","Urban Hospitals","Urban Beds","Total Hospitals","Total Beds","Last Updated"])
	for state_index in range(len(states_stat)):
		state = (states_stat[state_index]["state"])
		total_rural_hospitals = (states_stat[state_index]["ruralHospitals"])
		total_rural_beds = (states_stat[state_index]["ruralBeds"])
		total_urban_hospitals = (states_stat[state_index]["urbanHospitals"])
		total_urban_beds = (states_stat[state_index]["urbanBeds"])
		total_hospitals = (states_stat[state_index]["totalHospitals"])
		total_beds = (states_stat[state_index]["totalBeds"])
		last_updated = (states_stat[state_index]["asOn"])
		indian_hospitals_df.loc[state_index] = [state,total_rural_hospitals,total_rural_beds,total_urban_hospitals,total_urban_beds,total_hospitals,total_beds,last_updated]
	print(indian_hospitals_df)
	indian_hospital_agg_html = indian_hospitals_df.to_html(index=False)
	text_file = open("indian_hospitals_agg.html", "w")
	text_file.write("<h2>Indian Hospital Statistics</h2>")
	text_file.write("<br>")
	text_file.write(indian_hospital_agg_html)
	text_file.write("<br><br>")
	text_file.write("<b>Disclaimer: The data presented is a representation of the data pulled from "+results["data"]["sources"][0]["url"]+"</b>")
	text_file.close()


def patient_tracing_stat(patient_tracing_api):
	response = requests.request("GET", patient_tracing_api)
	results = json.loads(response.text)

	patient_data_df = pd.DataFrame(
	columns=["PatientId","Reported On","OnSet Estimate","Age Estimate",
	"Gender","City","District","State","Status","Remarks","Contracted From",
	"News Source","Nationality","Foreign Visit","Place","Family Link","Trace Link"])

	patient_data = results["data"]["rawPatientData"]
	for patient_index in range(len(patient_data)):
		patient_id = "P"+str(patient_data[patient_index]['patientId']).encode('ascii', 'ignore').decode('ascii')
		reported_on = patient_data[patient_index]['reportedOn'].encode('ascii', 'ignore').decode('ascii')
		onset_estimate = patient_data[patient_index]['onsetEstimate'].encode('ascii', 'ignore').decode('ascii')
		age_estimate = patient_data[patient_index]['ageEstimate'].encode('ascii', 'ignore').decode('ascii')
		gender = patient_data[patient_index]['gender'].encode('ascii', 'ignore').decode('ascii')
		city = patient_data[patient_index]['city'].encode('ascii', 'ignore').decode('ascii')
		district = patient_data[patient_index]['district'].encode('ascii', 'ignore').decode('ascii')
		state = patient_data[patient_index]['state'].encode('ascii', 'ignore').decode('ascii')
		status = patient_data[patient_index]['status'].encode('ascii', 'ignore').decode('ascii')
		remarks = patient_data[patient_index]['notes'].encode('ascii', 'ignore').decode('ascii')
		if("contractedFrom" not in patient_data[patient_index]):
			contracted_from = ""
		else:
			contracted_from = patient_data[patient_index]['contractedFrom'].encode('ascii', 'ignore').decode('ascii')
		if("sources" not in patient_data[patient_index]):
			sources = ""
		elif len(patient_data[patient_index]['sources']) > 0 :
			sources = patient_data[patient_index]['sources'][0].encode('ascii', 'ignore').decode('ascii')
		if (len(patient_data[patient_index]['nationality'])>0):
			nationality = patient_data[patient_index]['nationality'][0].encode('ascii', 'ignore').decode('ascii')
		else:
			nationality = "Not Found"
		place_attributes = patient_data[patient_index]['place_attributes']
		foreign_visit = ""
		place = ""
		for visit in range(len(place_attributes)):
			foreign_visit = foreign_visit + str(place_attributes[visit]['is_foreign']) + ", "
			place = place + place_attributes[visit]['place'].encode('ascii', 'ignore').decode('ascii') + ","
		relationship = patient_data[patient_index]['relationship']
		family_link = ""
		trace_link = ""
		for relation in range(len(relationship)):
			family_link = family_link + relationship[relation]['link'].encode('ascii', 'ignore').decode('ascii') + ", "
			if(len(relationship[relation]['with']) > 0):
				trace_link = trace_link + relationship[relation]['with'][0].encode('ascii', 'ignore').decode('ascii') + ", "
		patient_data_df.loc[patient_index] = [patient_id,reported_on,onset_estimate,age_estimate,gender,city,district,state,status,remarks,contracted_from,sources,nationality,foreign_visit,place,family_link,trace_link]
		patient_data_html = patient_data_df.to_html(index=False)
		text_file = open("covid19_patient_tracking.html", "w")
		text_file.write("<h2>Covid19 Patient Tracker</h2>")
		text_file.write("<br>")
		text_file.write(patient_data_html)
		text_file.write("<br><br>")
		text_file.write("Last Refreshed : "+ results["lastRefreshed"])
		text_file.write("<br/><br/><b>Disclaimer: The data shown here is subject to verification from the news.</b>")
		text_file.close()


if __name__=='__main__':
	rapidapi_url = "https://coronavirus-monitor.p.rapidapi.com/coronavirus/latest_stat_by_country.php"
	rapidapi_monitor(rapidapi_url)
	#print(rapidapi_stat.head())

	rootnet_agg_stat_api = "https://api.rootnet.in/covid19-in/stats/latest"
	rootnet_daily_series_stat_api = "https://api.rootnet.in/covid19-in/stats/daily"
	rootnet_hospital_bed_stat_api = "https://api.rootnet.in/covid19-in/stats/hospitals"
	rootnet_contact_and_helpline_api = "https://api.rootnet.in/covid19-in/contacts"
	rootnet_notification_api = "https://api.rootnet.in/covid19-in/notifications"

	patient_tracing_api = "https://api.rootnet.in/covid19-in/unofficial/covid19india.org"
	statewise_tracing_api = "https://api.rootnet.in/covid19-in/unofficial/covid19india.org/statewise"
	statewise_tracing_history = "https://api.rootnet.in/covid19-in/unofficial/covid19india.org/statewise/history"
	patient_travel_history = "https://api.rootnet.in/covid19-in/unofficial/covid19india.org/travelhistory"

	agg_stat_api(rootnet_agg_stat_api)

	agg_hospital_stat(rootnet_hospital_bed_stat_api)

	patient_tracing_stat(patient_tracing_api)
	#print(rapidapi_stat.head())
	#df.to_csv('india_covid19.csv',index=False)
