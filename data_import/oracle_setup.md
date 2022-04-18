    
# Download the Instant client 

Either from: 

```
https://download.oracle.com/otn_software/nt/instantclient/213000/instantclient-basic-windows.x64-21.3.0.0.0.zip 
```

or:

```
https://drive.google.com/file/d/1C6qmyL_RlQifqJGV3bUd31v88EyEBN8R/view?usp=sharing
```


# Unzip the Instant client

```powershell
Expand-Archive .\instantclient-basic-windows.x64-21.3.0.0.0.zip
```




# Create a virtual environment 

```powershell
python -m venv venv
```




# Modify Environment Variables

In this step, we will modify the environment

* Set the Environment path to contain the location of the Oracle Instant Client files
* Set environment variables so that the python code can properly determine username/password and database connection string

```powershell
$Env:PATH += ";$pwd/instantclient-basic-windows.x64-21.3.0.0.0/instantclient_21_3"
$Env:myuser = "kerekovskik"
$Env:mypw = "PASSWORD"
$Env:mydsn = "oracle.cise.ufl.edu:1521/orcl"
```


# Install flask and cx_oracle into the virtual environment

```powershell
python -m pip install -r .\requirements.txt
```