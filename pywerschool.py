#!/usr/bin/env python3
import zeep, requests, logging
import zeep.helpers

class PywerschoolError(Exception):
    ''' An error within pywerschool '''

class Client:
    ''' The client for connecting to powerschool
    
    Client(base_url, api_username="pearson", api_password="m0bApP5")

    A client for using powerschool methods '''
    def __init__(self, base_url, api_username="pearson", api_password="m0bApP5"):
        logging.basicConfig(level=logging.CRITICAL)
        session = requests.session()
        session.auth = requests.auth.HTTPDigestAuth(api_username, api_password)
        if base_url[:-1] != "/":
            base_url += "/"
        self.url = base_url + "pearson-rest/services/PublicPortalServiceJSON"
        try:
            self.client = zeep.Client(wsdl=self.url + "?wsdl",transport=zeep.transports.Transport(session=session))
        except requests.exceptions.ConnectionError:
            raise PywerschoolError("Could not connect to {}.".format(base_url))
        except requests.exceptions.HTTPError:
            raise PywerschoolError("Incorrect api credentials ({}, {})".format(api_username, api_password))
    def getStudent(self, username, password,toDict=False):
        service = self.client.create_service('{http://publicportal.rest.powerschool.pearson.com}PublicPortalServiceJSONSoap12Binding',self.url)
        result = service.loginToPublicPortal(username, password)["userSessionVO"]
        if result["userId"] == None:
            raise PywerschoolError("Could not log in to ({}, {})".format(username, password))
        userSessionVO = {
                "userId": result["userId"],
                "serviceTicket": result["serviceTicket"],
                "serverInfo": {
                    "apiVersion": result["serverInfo"]["apiVersion"]
                },
                "serverCurrentTime": result["serverCurrentTime"],
                "userType": result["userType"]
        }
        student = service.getStudentData(userSessionVO, result["studentIDs"][0], {"includes": "1"})["studentDataVOs"][0]
        if toDict:
            return zeep.helpers.serialize_object(student,target_cls=dict)
        return student
if __name__ == '__main__':
    client = Client("https://cms.powerschool.com")
    x = client.getStudent("steng","95340")
    y = client.getStudent("steng","95340",toDict=True)

