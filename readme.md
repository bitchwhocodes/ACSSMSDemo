# Using SMS from Azure Communication Services with Raspberry Pi 

## **Introduction**
Learn how to add SMS functionality available in [Azure Communication Services](https://azure.microsoft.com/en-us/services/communication-services/)   with the Raspberry Pi. Take this knowledge and apply it to other devices or platforms using the python SDK. Learn more about Aure Communication Services and the possibilities at https://azure.microsoft.com/en-us/services/communication-services/. 

**At the time of delivering this tutorial, the SMS functionality isn't widely avaiable in all Azure subscriptions. To get access during the month of November, 2020 - please submit a request at https://aka.ms/acs-garage-hack and join the Azure Communication Services Hackathon at https://aka.ms/garage/acs/hack**

### **What you will learn**
1. How to connect to your Raspberry Pi using SSH
2. How to set up and configure Azure Communication Services to leverage SMS including getting a phone number
3. How to install the Azure Communication Services python sdk on the Raspberry Pi
4. How to set up and configure Azure Event Grid to enable receiving of messages to the phone number from Azure Communication Services
5. How to use the Azure Communications Services python SDK to send an SMS and receive SMS

### **What you will need**
This tutorial will require both hardware and access to your Azure subscription. 

<em>Hardware and Configuration</em>
- Raspberry Pi 
- SD card imaged with the latest version of Raspberry Pi OS. Please see the additional Notes & Resources for instructions. 
- Ability to SSH into your Raspberry Pi. Please see the additional Notes & Resources for instructions. 
- Ensure your Raspberry Pi is connected to the WiFi and that your host computer are on the same network. Please see the additional Notes & Resources for instructions.  
<em>Azure Subscription</em>
- Microsoft Employees - Activate your subsription credits if you haven't already at my.visualstudio.com
- Login to the Azure portal at portal.azure.com

### **Time Required**
Approximately 30 minutes with a Raspberry Pi that has Rasbian configured. 
### **Additional Resources & Notes** 

**Installing Raspbian Pi OS** - 
Please follow these directions to format an SD card with the latest version of Raspbian Pi OS https://www.raspberrypi.org/downloads/raspberry-pi-os/

**Enabling SSH on your Raspberry Pi** -
Please follow these directions to enable SSH on your Raspberry Pi 
https://www.raspberrypi.org/documentation/remote-access/ssh

**Getting your Pi on the WiFi** -
There are a few ways to configure your Pi to get on the WiFi. Ensure it is connected to the WiFi by opening a browser on the device or pinging a url. 
https://raspberrytips.com/raspberry-pi-wifi-setup/ 


***

## **Let's Get Started**
At the end of this section, you should have a working demo of sending an SMS and receiving one, on the Raspberry Pi. This lesson can serve as a building block to create more complex applications. 

Before going through these steps, please ensure you are set up to work with your Raspberry Pi. For the purpose of this tutorial, we are SSH'ing into the Raspberry Pi and working with it headless ( No GUI ). You can work directly on the Pi if you have a monitor and peripherals, or RDP into it as well. 

Please note if you are not ssh'ing in and accessing your Pi through an alternative means, you can skip to step 3. If you are not one to read directions and just want the steps in the form of commands, please skip to "aggregated steps"

### 1. SSH into the Raspberry Pi 

We will SSH into the Raspberry Pi from our computer to access its command line remotely. To do so, interfacing with the device via SSH will have to be enabled and the IP of the device will need to be known. Please see the XXXX for how to enable SSH on the device & get its IP. The default user name and password for the device is pi/raspberry - please change at least the password. 

```
ssh pi@<replace with your IP>
```

![logging into the pi](/images/01pilogin.gif)

### 2. Create a folder and navigate to that directory

```mkdir sms-quickstart && cd sms-quickstart```

### 4. Install the Azure Communication Services python SDK 

```pip install azure-communication-sms```

### 5. **Create an empty Python File** 

We will use the default text editor Nano to create and open the file. It will open it within the terminal, and navigating in this window will be a bit different. This will be an empty file that we add code to later. 

```sudo nano send-sms.py```

Nano will open up this file ( if it didn't exist it will create it, then open up - if it did exist previously, it will open it up).
Nothing will be added at this point, so save the file out. 
Save the script by:
- CTRL+O  ( to write out the file)
- CTRL+X ( to exit out of nano )

### 6. **Create an Azure Communication Services Resource**

Go to the portal at https://portal.azure.com to create an Azure Commuincation Services Resource. Please see the [full tutorial](https://docs.microsoft.com/en-us/azure/communication-services/quickstarts/create-communication-resource) for more detailed instructions. 
1. Create a Resource 

![Create a resource](/images/01Azurecreateresource.png)

2. Search in the top left box "communication", Azure Communication Services should show up in the list. Select it. 

![Create a resource](/images/02Commservice.png)

3. Create the Communication Services resource
Typical fields for creating a resource will need to be filled out. 

![Create a resource](/images/03Commservice.png)


### 7. **Get the Credientials for the Service** 

Once the service is created, go to the left hand side and select Keys

![Create a resource](/images/04Commservice.png)

Copy the **connection string** for this service to be used later in the python script on the Rasbperry Pi. 

![Create a resource](/images/06Commservice.png)


### 8. **Get a Phone Number**

Provided below are quick steps, for the complete tutorial please see https://docs.microsoft.com/en-us/azure/communication-services/quickstarts/telephony-sms/get-phone-number.  

On the Azure Communication page for the resource recently created, go to the left hand side and select **# Phone Number**

![Select the Phone Number](/images/05Commservice.png)

On this page select the **+ Get** button to get a new phone number.

![Select the Get button](/images/getphonenumber1.png)

Select the country to be **United States** use case to be **an application will be making calls or sending SMS messages**, the Number type as **Toll-free**, Calling to be **Outbound calling** and SMS to be **Inbound and outbound SMS**. Select Next. 

![Configure the phone number](/images/getphonenumber2.png)

Select area code to be 833 and quantity of 1. Select **Search**

![Configure the phone number](/images/getphonenumber2PNG.png)

A new phone number will be allocated that you can use to send messages from. Note this number for later use in the python script. 

### 9. **Add code to Python with Connection String and Phone Number previously recorded**

Go back to the Raspberry Pi and adjust this script by replacing the phone number allocated to you by the service, and input a number to send the SMS to. Please note the format of the number must includ the **+1**. The file can be edited with nano, or you can copy over and replace the entire script if that is easier. Note this that service is currently only available in the US. 

**You will need the connection string, and the phone number from the service**

```
import os
from azure.communication.sms import PhoneNumber
from azure.communication.sms import SendSmsOptions
from azure.communication.sms import SmsClient
connection_string =  '<PUT YOUR CONNECTION STRING HERE>'
sms_client = SmsClient.from_connection_string(connection_string)


try:
    # Quickstart code goes here
# calling send() with sms values
        sms_response = sms_client.send(
                from_phone_number=PhoneNumber("+18330001122"),
                to_phone_numbers=[PhoneNumber("+17201112233")],
                message="Hello World via SMS",
                send_sms_options=SendSmsOptions(enable_delivery_report=True)) # optional property
except Exception as ex:
    print('Exception:')
    print(ex)

```
Save the script by:
- CTRL+O  ( to write out the file)
- CTRL+X ( to exit out of nano )

### 10. Run the script 

It's time to run the script. 

```
python send-sms.py
```
Check the number you sent it to, a text should be there. Hopefully :) 



----



## **Tips & Troubleshooting**

### **Issues with Python**
Please check what version of python you have installed. This tutorial is following the default version that is associated on Raspbian OS being 2.7+. Both Python 2 and 3 can be on the device. 
```
python --version 
```

### **Can't Send Messages Internationally**
Please not that at the time of writing this tutorial, the service currently only supports US based numbers. 

### **Can't get a Phone Number**
SMS functionality currently isn't available in the public preview in all subscription types. Please submit a request to get access to this service at aka.ms/acs-garage-hack. 


### **How to Enable SSH**

If starting from a fresh install of Raspbian OS, SSH will need to be enabled before attempting to connect to the device remotely. Setting the Pi to work as a desktop is the easiest way to do this. 

**Desktop**

1. Launch Raspberry Pi Configuration from the Preferences menu
2. Select the Interfaces tab
3. Select Enabled next to SSH
4. Click OK 


![gif to show how to do this](/images/00enablessh.gif)

**Terminal**
1. Open a terminal window on the Pi
2. Enter <code> sudo raspi-config</code> in the terminal window
3. Select <code> Interfacing Options </code>
4. Select <code>SSH</code>
5. Choose <code>Yes</code>
6. Select <code>OK</code>
7. Choose <code>Finish</code>


![gif to show how to do this](/images/00enablesshterminal00.gif)






