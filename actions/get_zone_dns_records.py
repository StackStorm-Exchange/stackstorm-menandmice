from st2common.runners.base_action import Action


class GetZoneDNSRecords(Action):

    def __init__(self, config):
        super(GetZoneDNSRecords, self).__init__(config)

    def get_dns_zone(self, url, client, dns_domain):
        """Query the Men and Mice API for the DNS Name to get the
        DNS zone that the DNS record will live in. Need to return just the
        record reference object so it can used later. Verify that the call
        was successful by checking the response code (Expecting: 200)
        Returns: string containing zone referenct ex: dnszone/44
        """
        dns_zone_filter = "type:^Master$ name:^{0}$".format(self.check_dns_name(dns_domain))
        dns_response = client.get("{0}/DNSZones?filter={1}".format(url, dns_zone_filter))
        dns_response.raise_for_status()
        dns_json = dns_response.json()
        dns_zones = dns_json["result"]["dnsZones"]

        return dns_zones[0]["ref"]

    def get_dns_records(self, url, client, dns_zone_ref):
        """Get all the DNS A records for the dns zone that was
        found before. We only care about A records. (Expecting: 200)
        Returns: Array of dictionaries containin all records withing
        zone
        """
        dns_record_filter = "?filter=type:^A$"
        dns_record_response = client.get("{0}/{1}/DNSRecords{2}".format(url,
                                                                        dns_zone_ref,
                                                                        dns_record_filter))
        dns_record_response.raise_for_status()
        dns_records = dns_record_response.json()

        return dns_records["result"]["dnsRecords"]

    def resolve_fqdn(self, url, client, dns_record):
        """Takes a DNS record weather that is a related
        record or a normal DNS record and finds the Zone name from
        the Zone Ref that is given with the record then combines it
        with the name of the dns record to make sure that the fqdn
        is correct.
        Returns: String
        """
        dns_zone_response = client.get("{0}/{1}".format(url, dns_record['dnsZoneRef']))
        dns_zone_response.raise_for_status()
        dns_zone = dns_zone_response.json()

        dns_zone_name = dns_zone['result']['dnsZone']['name']
        if dns_zone_name.endswith('.'):
            dns_zone_name = dns_zone_name[:-1]

        fqdn = "{0}.{1}".format(dns_record['name'], dns_zone_name)

        return fqdn

    def get_dns_related_records(self, url, client, dns_record_ref):
        """Gets all the related records from the DNS A record that was
        found above. If related records exist we need to generate the
        FQDN for the record before we continue
        Returns: Array of Dictionairies containing all related records
        """
        dns_related_record_response = client.get(("{0}/{1}/RelatedDNSRecords"
                                                  "".format(url, dns_record_ref)))
        dns_related_record_response.raise_for_status()
        dns_related_records_json = dns_related_record_response.json()

        # Always returned as an array maybe empty but will always be array.
        dns_related_records = []
        for related_record in dns_related_records_json["result"]["dnsRecords"]:
            related_record_fqdn = self.resolve_fqdn(url, client, related_record)
            related_record['name_fqdn'] = related_record_fqdn
            dns_related_records.append(related_record)

        return dns_related_records

    def build_dns_information(self, url, client, dns_records, dns_domain):
        """Takes all dns_records and looks for any related records and compiles
        that into 1 list to be returned.
        Returns: Dictionairies containing all dns records
        """
        dns_dict = {}
        for record in dns_records:
            record_fqdn = "{0}.{1}".format(record['name'], dns_domain)
            related_records = self.get_dns_related_records(url, client, record['ref'])
            dns_dict[record_fqdn] = record
            dns_dict[record_fqdn]['related_records'] = related_records

        return dns_dict

    def mm_build_client(self, kwargs_dict):
        """Build the rest client that will be used in all of our calls.
        Do auth here and pass that along with the client. Also we build
        the base url that can just be appended as needed in later calls
        """
        server = self.get_arg("server", kwargs_dict)
        username = self.get_arg("username", kwargs_dict)
        password = self.get_arg("password", kwargs_dict)
        transport = self.get_arg("transport", kwargs_dict)
        url = "{0}://{1}/mmws/api".format(transport, server)

        client = requests.Session()
        client.auth = (username, password)

        if transport == "https":
            client.verify = False

        return (url, client)

    def run(self, **kwargs):
        """Main entry point for the StackStorm actions to get all the information
        needed to build the dns entry from scratch.
        """
        kwargs_dict = dict(kwargs)

        dns_domain = kwargs['dns_domain']
        url, client = self.mm_build_client(kwargs_dict)

        dns_zone_ref = self.get_dns_zone(url, client, dns_domain)
        dns_records = self.get_dns_records(url, client, dns_zone_ref)
        dns_dict = self.build_dns_information(url, client, dns_records, dns_domain)

        return dns_dict
