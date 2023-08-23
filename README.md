# AutoLogonSapGUI

Logon SAP GUI on Macos

## change logon page layout to list
![screenshot](https://github.com/a87b01c14/AutoLogonSapGUI/blob/master/WX20230822-103503%402x.png)

## config login client by conf.json
```
{
  "ApplicationPath": "/Applications/SAP Clients/SAPGUI/SAPGUI.app",
  "ApplicationName": "SAPGUI",
  "WindowName": "SAP GUI for Java",
  "items": [
    {
      "index": 7,
      "title": "Antex DEV 200",
      "client": "200",
      "user": "AT-YUXS",
      "password": "#"
    },
    {
      "index": 7,
      "title": "Antex DEV 400",
      "client": "400",
      "user": "10013993",
      "password": "#"
    },
    {
      "index": 8,
      "title": "Antex PRD 800",
      "client": "800",
      "user": "10013993",
      "password": "#"
    },
    {
      "index": 4,
      "title": "PB S4D 110",
      "client": "110",
      "user": "YU.XIAOSAN",
      "password": "#"
    },
    {
      "index": 4,
      "title": "PB S4D 120",
      "client": "120",
      "user": "YU.XIAOSAN",
      "password": "#"
    },
    {
      "index": 5,
      "title": "PB S4P 800",
      "client": "800",
      "user": "YU.XIAOSAN",
      "password": "#"
    },
    {
      "index": 6,
      "title": "PB S4Q 300",
      "client": "300",
      "user": "YU.XIAOSAN",
      "password": "#"
    }
  ]
}
```

## GUI
![screenshot](https://github.com/a87b01c14/AutoLogonSapGUI/blob/master/saplogin.png)
