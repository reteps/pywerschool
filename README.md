# pywerschool
A python wrapper over the powerschool api.

### example

```python3
client = pywerschool.Client(base_url)
student = client.getStudent(username, password, toDict=True)
print("Current GPA:{}".format(student["student"]["currentGPA"])
```

### methods

##### `Client(base_url, api_username="pearson", api_password="m0bApP5")`
  + create a client to powerschool
##### `Client.getStudent(username, password, toDict=False)`
  + return a student given a username and password.
  + toDict returns a dictionary instead of a native Zeep object
  
### dependencies

+ zeep (`python3 -m pip install zeep`)
