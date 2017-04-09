jenkinsServerUrl="http://localhost"
jenkinsServerPort=8080

__author__ = 'montana'

import jenkinsapi
import sys
from jenkinsapi.jenkins import Jenkins

def connectToJenkins():
    server = Jenkins(jenkinsServerUrl+":"+jenkinsServerPort.__str__())
    return server

def getJenkinsJobs(server):
    return server.keys()

def runJenkinsJob(job, paramsMap):
    if(len(job.get_params_list()) != len(sys.argv)-3):
        print "Error: Argument length mismatch. Please ensure that you're supplying enough arguments for the jenkins job."
        exit()

    if(job.has_params()):
        builder = {}
        counter = 3
        for param in job.get_params_list():
            builder[param] = sys.argv[counter]
            counter = counter + 1
        print "Starting job '" + job.name + "'."
        job.invoke(None,False,False,3,15,builder,None,None)

    else:
        job.invoke()

def main():
    if(len(sys.argv) == 2):
        print "You need to specify a job name, task, and any arguements needed."
        print "If you're trying to deploy jenkinsTestApp (version 2.0.0) to beta."
        print "Try this: > Finch jenkinsTestApp deploy beta 2.0.0"
        print "If still having problems, contact the author Montana Mendy at montana@getprowl.com"
        exit()
    else:
        server = connectToJenkins()
        jobs = getJenkinsJobs(server)
        jobName = sys.argv[1] + " " + sys.argv[2]
        if(jobs.__contains__(jobName)):
            job = server[jobName]
            runJenkinsJob(job, sys.argv)
        else:
            print 'Could not find the job that was entered.'
            print 'Ensure the jenkins job is [name] [action] and that you\'re giving Finch the right parameters!'
            print 'For instance, you\'ve entered \'' + sys.argv[1] + ' ' + sys.argv[2] + '\' for your name and action.'

main()
