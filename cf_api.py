# #############################################################################################
# SCRIPTNAME: cloudflare_api.py                                                               #
# AUTHOR:     Benjamin Hofmann                                                                #
# PURPOSE:    Handling with the CloudFlare API                                                #
# DATE:       27.05.2017                                                                      #
# CHANGED:    not yet                                                                         #
###############################################################################################
# TODO: Fehler Abfangen bei Getids
class CloudFlare:
    api_url = "https://api.cloudflare.com/client/v4/"

    def __init__(self, cf_email, cf_apiky):
        self.headers = {
            'X-Auth-Email': cf_email,
            'X-Auth-Key': cf_apiky,
            'Content-Type': 'application/json'
            }

    def cf_api_req(self, call_type, url, data=None):
        import requests
        from requests.exceptions import RequestException
        call=getattr(requests,call_type)
        if data == None:
            try:
                r = call(url, headers=self.headers)
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                raise
            json_r = r.json()
            return json_r
        else:
            try:
                r = call(url, headers=self.headers, json=data)
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                raise
            json_r = r.json()
            return json_r

    def get_zone_info(self, zone):

        url = self.api_url+"zones?name="+zone
        json_data = self.cf_api_req("get",url)
        return json_data



    def get_record_info(self, zone_id, record, dns_type):

        url = self.api_url+"zones/"+zone_id+"/dns_records?type="+dns_type+"&name="+record
        json_data = self.cf_api_req("get",url)
        return json_data

    def get_record_ip(self, zone, record, dns_type):

        return self.get_record_info(self.get_zone_info(zone)["result"][0]["id"], record, dns_type)["result"][0]["content"]



    def update_dns_record(self, zone, record, dns_type, content):

        zone_id = self.get_zone_info(zone)["result"][0]["id"]
        record_info = self.get_record_info(zone_id, record, dns_type)

        url = self.api_url+"zones/"+zone_id+"/dns_records/"+record_info["result"][0]["id"]

        data = {    'type': record_info["result"][0]["type"],
                    'name': record_info["result"][0]["name"],
                    'content': content
                    }
        json_data = self.cf_api_req("put",url,data)
        return json_data
