Mac: pyinstaller -D -w --osx-bundle-identifier=com.yu.aotologonsapgui -n AutoLogonSapGUI -i sap.icns --add-data "conf.json:." --add-data "background.jpeg:." --add-data "GetNameAndTitleOfActiveWindow.scpt:." sapgui.py
Win: pyinstaller -D -w -n AutoLogonSapGUI -i sap.ico --add-data "conf.json;." --add-data "background.jpeg;."  sapgui.py

