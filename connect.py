import requests,json as jsony

class WatsonConnect:

	def __init__(self,wml):
		wml_credentials = wml

		# Paste your Watson Machine Learning service apikey here
		# Use the rest of the code sample as written
		apikey = wml_credentials['apikey']

		# Get an IAM token from IBM Cloud
		url = "https://iam.bluemix.net/oidc/token"
		headers = {"Content-Type": "application/x-www-form-urlencoded"}
		data = "apikey=" + apikey + "&grant_type=urn:ibm:params:oauth:grant-type:apikey"
		IBM_cloud_IAM_uid = "bx"
		IBM_cloud_IAM_pwd = "bx"
		response = requests.post(url, headers=headers, data=data, auth=(IBM_cloud_IAM_uid, IBM_cloud_IAM_pwd))
		self.iam_token = response.json()["access_token"]

	def sendImage(self,json,url):
		headers = {
			"Authorization": "Bearer "+self.iam_token,
			"Content-Type" : "application/json"
			}
		resp = requests.post(url=url,json=json, headers=headers)
		return jsony.loads(resp.content.decode('utf-8'))
