# How to execute the plain Firmware Update using Python and Redfish(Without Docker)

## Pre-requisite

- Python 2.7
- LC Enabled on Dell Server
- Firmware stored under the same directory

## Steps

```
root@debian:~/mytest# python testupdate.py -i <iDRAC IP> -u root -p calvin -f BIOS_N88YC_WN64_1.2.71.EXE
IDRAC_IP calvin root /root/mytest/BIOS_N88YC_WN64_1.2.71.EXE

- WARNING, downloading DUP payload to iDRAC

File Name BIOS_N88YC_WN64_1.2.71.EXE
Image File /root/mytest/BIOS_N88YC_WN64_1.2.71.EXE

- PASS: Command passed, 201 status code returned

- Message:Package successfully downloaded.
- FW file version is: 1.2.71
/redfish/v1/UpdateService/FirmwareInventory/Available-159-1.2.71

- WARNING, installing downloaded firmware payload to device

PayLoad {"SoftwareIdentityURIs":["/redfish/v1/UpdateService/FirmwareInventory/Available-159-1.2.71"],"InstallUpon":"NextReboot"}
{'cookies': <RequestsCookieJar[]>, '_content': '{"@Message.ExtendedInfo":[{"Message":"Only one task ID is displayed in the response.","MessageArgs":[],"MessageArgs@odata.count":0,"MessageId":"iDRAC.1.5.SYS408","RelatedProperties":[],"RelatedProperties@odata.count":0,"Resolution":"To view all task IDs, run the \\"Tasks\\" Redfish API.","Severity":"Informational"}]}\n', 'headers': {'Content-Length': '317', 'Keep-Alive': 'timeout=60, max=100', 'Server': 'Apache/2.4', 'Connection': 'Keep-Alive', 'Location': '/redfish/v1/TaskService/Tasks/JID_161372702235', 'Cache-Control': 'no-cache', 'Date': 'Tue, 16 Jan 2018 21:14:29 GMT', 'OData-Version': '4.0', 'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json;odata.metadata=minimal;charset=utf-8', 'X-Frame-Options': 'DENY'}, 'url': u'https://iDRAC_IP/redfish/v1/UpdateService/Actions/Oem/DellUpdateService.Install', 'status_code': 202, '_content_consumed': True, 'encoding': 'utf-8', 'request': <PreparedRequest [POST]>, 'connection': <requests.adapters.HTTPAdapter object at 0x7fcbcc047dd0>, 'elapsed': datetime.timedelta(0, 10, 697809), 'raw': <requests.packages.urllib3.response.HTTPResponse object at 0x7fcbcc05a250>, 'reason': 'Accepted', 'history': []}

- PASS, JID_161372702235 job ID successfully created


- Query job ID command passed

- Job not marked completed, current status is: Starting
- Message: Package successfully downloaded.
```
