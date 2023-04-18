#!/usr/bin/env python3
import os
import sys
import argparse
import subprocess
from bs4 import BeautifulSoup

KEY = "C1000Z_1234"
xmlHeader = '<?xml version="1.0"?>\n'

def decodePassword(pwd):
	# openssl des -in <config file> -d -k C1000Z_1234 -a -md md5
	try:
		fn = "c3000z.enum"
		f = open(fn, "w")
		p = pwd + "\n"
		f.write(p)
		f.close()
		out = subprocess.Popen(["openssl", "des", "-in", fn, "-d", "-k", KEY, "-a", "-md", "md5"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
		stdout,stderr = out.communicate()
		sout = stdout.decode("utf-8")[:-1]
		os.remove(fn)

	except:
		print("Error decoding password: %x" % pwd)
	
	return sout


def getAdminPwd(d):
	adminPassword = d.find_all('AdminPassword')
	for ap in adminPassword:
		pwd = ap.get_text()
		r = decodePassword(pwd)
		print("\tAdmin Password:\t\t\t%s" % r)


def instanceUsers(d):
	iuser= d.find_all('User')
	
	for u in iuser:
		e = "False"
		un = "none"
		pw = "NA"
		remote = "False"
		lines = str(u).splitlines()

		for l in lines:
			if "Enable" in l:
				e = "True"
			elif "Username" in l:
				un = str(l).split(">")[1].split("<")[0]
			elif "Password" in l:
				pw = str(l).split(">")[1].split("<")[0]
			elif "RemoteAccessCapable" in l:
				remote = str(l).split(">")[1].split("<")[0]
			else:
				continue
				
		
		if un != "none":
			print("\tInstance Username:\t\t%s" % un)
			if pw != "NA":
				pw = decodePassword(pw)
			print("\tInstance Password:\t\t%s" % pw)
			print("\tInstance Enabled:\t\t%s" % e)
			print("\tInstance Remote Access Capable:\t%s" % remote)
			print()


def getManagementServer(d):
	managementServer = d.find_all('ManagementServer')
	m1 = xmlHeader + str(managementServer[0])
	bs = BeautifulSoup(m1, 'xml')
	URL = bs.find_all('URL')[0].get_text()
	print("\tManagementServer URL:\t\t%s" % URL)
	Username = bs.find_all('Username')[0].get_text()
	print("\tManagementServer Username:\t%s" % Username)
	Password = bs.find_all('Password')[0].get_text()
	print("\tManagementServer Password:\t%s" % decodePassword(Password))
	print()
	crURL = bs.find_all('ConnectionRequestURL')[0].get_text()
	print("\tConnectionRequest URL:\t\t%s" % crURL)
	crUsername = bs.find_all('ConnectionRequestUsername')[0].get_text()
	print("\tConnectionRequest Username:\t%s" % crUsername)
	crPassword = bs.find_all('ConnectionRequestPassword')[0].get_text()
	print("\tConnectionRequest Password:\t%s" % decodePassword(crPassword))


def getUserInterfaceCreds(d):
	interfaceCreds = d.find_all('UserInterface')
	i1 = xmlHeader + str(interfaceCreds[0])
	bs = BeautifulSoup(i1, 'xml')
	telnet = str(bs.find_all('X_404A03_Telnet')[0]).splitlines()
	telnetPwd = "NA"
	telnetEnabled = "False"
	for t in telnet:
		if "Enabled" in t:
			telnetEnabled = "True"
		elif "Password" in t:
			telnetPwd = decodePassword(t.split(">")[1].split("<")[0])
		else:
			continue

	print("\tTelnet Enabled::\t\t%s" % telnetEnabled)
	print("\tTelnet Password::\t\t%s" % telnetPwd)


	ssh = str(bs.find_all('X_404A03_SSH')[0]).splitlines()
	sshPwd = "NA"
	sshEnabled = "False"
	for t in ssh:
		if "Enable" in t:
			sshEnabled = "True"
		elif "Password" in t:
			sshPwd = decodePassword(t.split(">")[1].split("<")[0])
		else:
			continue

	print("\tSSH Enabled::\t\t\t%s" % sshEnabled)
	print("\tSSH Password::\t\t\t%s" % sshPwd)


def getWANPPP(d):
	wanppp = d.find_all('WANPPPConnection')
	wp = xmlHeader + str(wanppp[0])
	bs = BeautifulSoup(wp, 'xml')
	username = bs.find_all('Username')[0].get_text()
	password = bs.find_all('Password')[0].get_text()
	print("\tWANPPP Username:\t\t%s" % username)
	print("\tWANPPP Password:\t\t%s" % decodePassword(password))


def getDefaultPPP(d):
	defppp = d.find_all("X_404A03_DefaultPPPConfig")
	dp = xmlHeader + str(defppp[0])
	bs = BeautifulSoup(dp, 'xml')
	username = bs.find_all('BackupUsername')[0].get_text()
	password = bs.find_all('BackupPassword')[0].get_text()
	print("\tDefaultPPP Backup Username:\t%s" % username)
	print("\tDefaultPPP Backup Password:\t%s" % decodePassword(password))


def getWifi(d):
	wifi = d.find_all("WLANConfiguration")
	for i in wifi:
		w = xmlHeader + str(i)
		try:
			bs = BeautifulSoup(w, 'xml')
			ssid = bs.find_all('SSID')[0].get_text()
			psk = bs.find_all('PreSharedKey')[0].get_text()
			print("\tWifi SSID:\t\t\t%s" % ssid)
			print("\tWifi PSK:\t\t\t%s" % str(psk).lstrip().rstrip())
			print()
		except:
			continue

	

def parseConfig(confData):

	d = BeautifulSoup(confData, 'xml')
	print("[+] Successfully loaded config file into BeautifulSoup")
	print("[+] Decoded passwords are:")
	
	getAdminPwd(d)
	print()
	instanceUsers(d)
	getManagementServer(d)
	print()
	getUserInterfaceCreds(d)
	print()
	getWANPPP(d)
	print()
	getDefaultPPP(d)
	print()
	getWifi(d)
	print()
	print("[+] Completed parsing the config file")
	print()
	

def main():
	parser = argparse.ArgumentParser(description='Parse C3000z router config and decode the passwords.')
	parser.add_argument('--file', dest='configFile', action="store", default="none", help='router XML config file')
	parser.add_argument('--key', dest='key', action="store", default="C1000Z_1234", help='Key to use for decoding [default=C1000Z_1234]')
	args = parser.parse_args()
	
	if args.configFile == "none":
		parser.print_help()
		sys.exit(0)

	if args.key != "C1000Z_1234":
		global KEY
		KEY = args.key

	backup = args.configFile

	if os.path.exists(backup) and os.path.isfile(backup):	
		try:
			f = open(backup, "r")
			print("[+] Reading config file: %s" % backup)
			parseConfig(f)
		except:
			print("Error")
		finally:
			f.close()
	else:
		print("Invalid config file")
		sys.exit(0)
	

main()

