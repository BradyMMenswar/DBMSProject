    
# Download the Instant client and place it in the root directory of the repo

Either from: 

```
https://download.oracle.com/otn_software/nt/instantclient/213000/instantclient-basic-windows.x64-21.3.0.0.0.zip 
```

or:

```
https://drive.google.com/file/d/1C6qmyL_RlQifqJGV3bUd31v88EyEBN8R/view?usp=sharing
```


# Unzip the Instant client 

Please note that this is an example with using powershell. 

```powershell
Expand-Archive .\instantclient-basic-windows.x64-21.3.0.0.0.zip
```

The location of the client libraries will be found in .\instantclient-basic-windows.x64-21.3.0.0.0\instantclient_21_3\

```powershell
PS C:\Users\kkerekovski\db_group_project\DBMSProject> ls -l .\instantclient-basic-windows.x64-21.3.0.0.0\instantclient_21_3\


    Directory: C:\Users\kkerekovski\db_group_project\DBMSProject\instantclient-basic-windows.x64-21.3.0.0.0\instantclient_21_3


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----          4/6/2022   8:48 AM                network
-a----         9/28/2021   7:08 AM          32256 adrci.exe
-a----         9/28/2021   7:08 AM          40424 adrci.sym
-a----         7/20/2020   8:01 AM           5903 BASIC_LICENSE
-a----         9/28/2021   7:09 AM           1738 BASIC_README
-a----         9/28/2021   7:08 AM          76288 genezi.exe
-a----         9/28/2021   7:08 AM          72768 genezi.sym
-a----         9/28/2021   7:00 AM         817152 oci.dll
-a----         9/28/2021   7:00 AM         792816 oci.sym
-a----         7/21/2021   4:56 PM         192000 ocijdbc21.dll
-a----         7/21/2021   4:56 PM          71424 ocijdbc21.sym
-a----         9/28/2021   6:11 AM         634368 ociw32.dll
-a----         9/28/2021   6:10 AM         127840 ociw32.sym
-a----         7/21/2021  10:06 AM        5053909 ojdbc8.jar
-a----         9/28/2021   5:52 AM          99840 oramysql.dll
-a----         9/28/2021   5:52 AM          71456 oramysql.sym
-a----          7/8/2021   5:02 PM        5123072 orannzsbb.dll
-a----          7/8/2021   5:02 PM        2109376 orannzsbb.sym
-a----         9/28/2021   5:03 AM        1095680 oraocci21.dll
-a----         9/28/2021   7:08 AM        1181096 oraocci21.sym
-a----         9/28/2021   5:43 AM        1076736 oraocci21d.dll
-a----         9/28/2021   7:08 AM        1048224 oraocci21d.sym
-a----         9/28/2021   7:06 AM      220298752 oraociei.dll
-a----         9/28/2021   7:06 AM       15387680 oraociei.sym
-a----         9/28/2021   6:52 AM         237568 orasql.dll
-a----         9/28/2021   6:52 AM          63624 orasql.sym
-a----         7/21/2021  10:31 AM        1790634 ucp.jar
-a----         9/28/2021   7:08 AM          32256 uidrvci.exe
-a----         9/28/2021   7:08 AM          40424 uidrvci.sym
-a----         9/27/2021   7:44 AM          74603 xstreams.jar


```




# Create a virtual environment 

```powershell
python -m venv venv
```


# Create an .env file in the root directory of the project 

This .env file will be used by the module python-decouple to extract the necessary info to connect to oracle 

Here's an example of what the file contents looks like. Ensure that your username and password reflect your own account. 
<p>

**the mydsn variable shouldn't be changed!!!**
</p>

```
myuser = "kerekovskik"
mypw = "MYSUPER_SECRET_PASSWORD"
mydsn = "oracle.cise.ufl.edu:1521/orcl"
```

# Activate the virtual environment 

Depending on what environment you're working on, you will need to activate the environment differently. Furthermore, Pycharm and VSCODE have their own way of specifying a virtual environment.

* For Powershell 
```powershell
.\venv\Scripts\Activate.ps1
```

* For CMD

```powershell
venv\Scripts\activate
```


# Install flask, cx_oracle and python-decouple nto the virtual environment

```powershell
python -m pip install -r .\requirements.txt
```


# Test your oracle connection

You can easily test whether you can connect to oracle by running the oracleFuncs.py script as a standalone script. 

**Ensure that you're actually connected to the GatorLink VPN otherwise this will fail.** 

```powershell
(venv) PS C:\Users\kkerekovski\db_group_project\DBMSProject> python .\oracleFuncs.py
Instant client NOT found in PATH variable... Attempting to set it manually
('it works',)
```