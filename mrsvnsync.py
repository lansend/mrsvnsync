#! /usr/bin/env python3.2
import string, os, sys
import configparser,subprocess
import httplib2
import re


def callCommandAndPrintResult(command):
	print(command)
	print("".join(os.popen(command).readlines()))

def endWithSlash(config):
	if config:
		config=config.replace("\\","/")
	if  not  config.endswith("/"):
		config = config + "/"				
	return config

def multiRepoSvnSync(repoNames):
	for repoName in repoNames:  	    
	    	backupDestUrl = "file:///"+ SVNBackupDir  + repoName
	    	backupDestUrl = backupDestUrl.replace("file:////","file:///")

	    	localDestUrl = SVNBackupDir  + repoName
	    	backupSourceUrl = " " + SVNAccessUrl + repoName    	
	    	
	    	if not os.path.exists(SVNBackupDir+os.sep+repoName):
	    		#svnadmin create
	    		svnCreateCommand = svnCreate + localDestUrl
	    		callCommandAndPrintResult(svnCreateCommand)
	    		#hook for windows
	    		prcHook = open(localDestUrl+"/hooks/pre-revprop-change.bat",'a')
	    		prcHook.write("exit 0")
	    		prcHook.close()
	    		#hook for unix like system
	    		prcHook = open(localDestUrl+"/hooks/pre-revprop-change",'a')
	    		prcHook.write("#!/bin/sh\n")
	    		prcHook.write("exit 0\n")
	    		prcHook.close()
	    		#chmod 
	    		chmodCommand = "chmod 755 " +localDestUrl+"/hooks/pre-revprop-change"
	    		callCommandAndPrintResult(chmodCommand)

	    		#svnsync init
	    		svnsyncInitCommand = svnsyncInit + backupDestUrl + backupSourceUrl + userNameAndPassword + svnsyncParam
	    		callCommandAndPrintResult(svnsyncInitCommand)
	    		
	    	#svnsync sync
	    	svnsyncSyncCommand = svnsyncSync + backupDestUrl + userNameAndPassword + svnsyncParam
	    	callCommandAndPrintResult(svnsyncSyncCommand) 	


#get configuration from mrsvnsync.ini
config = configparser.ConfigParser()
config.read("mrsvnsync.ini")

mrSvnSyncConfig=config["MultiRepoSvnSyncConfig"]

SVNPathParentPath=mrSvnSyncConfig["SVNPathParentPath"]
SVNAccessUrl=mrSvnSyncConfig["SVNAccessUrl"]
SVNBackupDir=mrSvnSyncConfig["SVNBackupDir"]
UserName = mrSvnSyncConfig["UserName"]
Password = mrSvnSyncConfig["Password"]

#change the path to end with "/
SVNPathParentPath=endWithSlash(SVNPathParentPath)
SVNBackupDir=endWithSlash(SVNBackupDir)
SVNAccessUrl=endWithSlash(SVNAccessUrl)

#if the backup destination directory is not exist ,make the directory
if not os.path.exists(SVNBackupDir):
	os.mkdir(SVNBackupDir)

#the svn command
svnsyncInit = "svnsync init "
svnsyncSync = "svnsync sync "
svnsyncParam = " --trust-server-cert --non-interactive"
svnCreate = "svnadmin create "
userNameAndPassword = " --username " + UserName + " --password " + Password

#if SVNPathParentPath is not NONE,list the sub directory names in it as the repository names
if SVNPathParentPath!="/":
	repoNames = os.listdir(SVNPathParentPath) 
	for index in range(len(repoNames)-1,-1,-1):
	    if not os.path.isdir(SVNPathParentPath + os.sep + repoNames[index]):
	        del repoNames[index]
else:
	http = httplib2.Http(cache=".cache",disable_ssl_certificate_validation=True)
	http.add_credentials(UserName,Password)
	resp,content = http.request(SVNAccessUrl,headers={'cache-control':'no-cache'})
	content = content.decode('UTF-8')
	pattern = re.compile(r'<dir name="(.*?)".*?/>')
	repoNames = pattern.findall(content)


multiRepoSvnSync(repoNames)