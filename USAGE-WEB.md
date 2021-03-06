### Web UI Usage

In Web UI, you can start with building a configuration consisting of all the parameters which will be needed to run the application successfully. The configuration has two flavors, one with global configuration by which, you can connect to all the devices using one set of credential (i.e., username and password) or entering them separately for every device.

##### Step 0 : If you are running this application on your local system, starting the server will be the first step.
```
# First make sure that you are in the ptolemy directory
cd app
python httpserver.py
```

#### Building a new Configuration for first time users
##### Step 1: Start building a new configuration
![Click on Build configuaration to start building a new configuration](https://github.com/JNPRAutomate/ptolemy/blob/master/demo/screenshots/web-ui/Build_Step1.png)

##### Step 2: Here you have two options :-
###### 1. Building Configuration With Global Credentials
Check Global Configuration and Choose required output formats and Log Types
![For using global credentials for all devices, Check the Use Global Credentials check box and then choose required output formats and desired log types.](https://github.com/JNPRAutomate/ptolemy/blob/master/demo/screenshots/web-ui/Build_Step2_1.png)

###### 2. Building Configuration Without Global Credentials
Uncheck Global Configuration and Choose output formats and Log Types
![Uncheck Use Global Credentials check box and then choose required output formats and desired log types.](https://github.com/JNPRAutomate/ptolemy/blob/master/demo/screenshots/web-ui/Build_Step2_2.png)

##### Step 3: Enter the device details by Uploading a CSV and/or editing the Device Credential Table


***
Read the details about how a valid [CSV File](VALID-CSV.md) will look like.
***

![Choose a CSV File with Connection details for the devices and/or Click edit to make changes to the existing table by add, removing and editing device credentials.](https://github.com/JNPRAutomate/ptolemy/blob/master/demo/screenshots/web-ui/Build_Step3.png)

#### Step 4 (Optional) : Confirm the changes made in the table if any or cancel to discard them.
![Choose Confirm after adding/editing/removing device details to save the changes or click Cancel to discard them.](https://github.com/JNPRAutomate/ptolemy/blob/master/demo/screenshots/web-ui/Build_Step4_1.png)

![If you choose Global User Credentials then providing Username and Password for each device is not needed as only Global User Credentials will only be picked while running the program.](https://github.com/JNPRAutomate/ptolemy/blob/master/demo/screenshots/web-ui/Build_Step4_2.png)

#### Step 5 : Click on Generate Graph button
![Click on Generate graph to finish graph generation](https://github.com/JNPRAutomate/ptolemy/blob/master/demo/screenshots/web-ui/Build_Step5.png)



#### Generating graph from an existing template
##### Step 1: Switch on Develop Using Existing Template
![Click on Build configuaration to start building a new configuration](https://github.com/JNPRAutomate/ptolemy/blob/master/demo/screenshots/web-ui/Template_Step1.png)

##### Step 2: Choose an existing template built from configurations used earlier or made using Sample Template.

##### Step 3: Click on Generate Graph button
![Click on Choose File for Browse Template to select the template file consiting of an already existing configuration and then Click on Generate graph to finish graph generation](https://github.com/JNPRAutomate/ptolemy/blob/master/demo/screenshots/web-ui/Template_Step2and3.png)



### Output and Logs
![Output](https://github.com/JNPRAutomate/ptolemy/blob/master/demo/screenshots/web-ui/Output_1.png)

#### Sample Outputs

##### Download Sample Outputs
[DOT](https://github.com/JNPRAutomate/ptolemy/blob/master/demo/output/SampleOutput.dot), [SVG](https://github.com/JNPRAutomate/ptolemy/blob/master/demo/output/SampleOutput.svg), [JSON](https://github.com/JNPRAutomate/ptolemy/blob/master/demo/output/SampleOutput.json)

A Sample output in SVG Format
![Sample Output](https://github.com/JNPRAutomate/ptolemy/blob/master/demo/output/SampleOutput.png)

##### Sample Template

[Dowload Sample Template](https://github.com/JNPRAutomate/ptolemy/blob/master/demo/output/SampleTemplate.ptpl)

```
{
	"Global Credentials": "None",
	"Output Formats": [
		"DOT",
		"JSON",
		"SVG"
	],
	"Logs": "Global",
	"Connection Details": [
		{
			"hostname": "cdbu-sol-vcf-5100-24q-01.dcbg.juniper.net",
			"username": "root",
			"password": "admin",
			"path": "",
			"port": ""
		},
		{
			"hostname": "cdbu-sol-vcf-5100-48s-05.dcbg.juniper.net",
			"username": "root",
			"password": "admin",
			"path": "",
			"port": ""
		},
		{
			"hostname": "cdbu-sol-vcf-5100-48s-06.dcbg.juniper.net",
			"username": "root",
			"password": "admin",
			"path": "",
			"port": ""
		},
		{
			"hostname": "cdbu-sol-vcf-5100-24q-02.dcbg.juniper.net",
			"username": "root",
			"password": "admin",
			"path": "",
			"port": ""
		}
	],
	"Filename": "lldp_graph"
}
```


##### Global Logs
![Logs](https://github.com/JNPRAutomate/ptolemy/blob/master/demo/screenshots/web-ui/Output_2.png)

