from result_output import *
import sys
import json
import importlib.util
import urllib.request
from googleapiclient import discovery
from google.oauth2 import service_account
from pprint import pprint
from google.cloud import storage
# from google.cloud import storage_transfer_v1
from google.cloud import container_v1
from googleapiclient import discovery
from google.cloud.container_v1 import ClusterManagerClient
from kubernetes import client

class Activity():

    def testcase_check_GKE_Cluster_name(self,test_object,credentials,project_id):
        testcase_description="Check GKE Cluster name"
        expected_result='gke-cluster-1'
        try:
            is_present = False
            actual = 'GKE Cluster name is not '+ expected_result
            try:
                service = discovery.build('container', 'v1', credentials=credentials)
                request = service.projects().zones().clusters().list(projectId=project_id, zone='-')
                response = request.execute()  
                if 'clusters' in response:
                    for cluster in response['clusters']:
                        if cluster['name'] == expected_result:
                            print("%s,%s,%d" % (project_id, cluster['name'], cluster['currentNodeCount']))  
                            is_present = True
                            break
            except Exception as e:
                is_present = False
            test_object.update_pre_result(testcase_description,expected_result)
            if is_present==True:
                test_object.update_result(1,expected_result,actual,"No Comment"," Congrats! You have done it right!") 
            else:
                test_object.update_result(0,expected_result,actual,"Check instance name","https://cloud.google.com/bigtable/docs/")   

        except Exception as e:    
            test_object.update_result(-1,expected_result,"Internal Server error","Please check with Admin","")
            test_object.eval_message["testcase_check_ServiceAccount_name"]=str(e)                

    def testcase_check_Node_numbers(self,test_object,credentials,project_id):
        testcase_description="Check GKE Cluster Nodes Count"
        expected_result=3
        try:
            is_present = False
            actual = 'GKE Cluster nodes is not '+ expected_result
            try:
                service = discovery.build('container', 'v1', credentials=credentials)
                request = service.projects().zones().clusters().list(projectId=project_id, zone='-')
                response = request.execute()  
                if 'clusters' in response:
                    for cluster in response['clusters']:
                        print("%s,%s,%d" % (project_id, cluster['name'], cluster['currentNodeCount']))  
                        if cluster['currentNodeCount'] == expected_result:
                            is_present = True
                            break
                        
                cluster_manager_client = container_v1.ClusterManagerClient(credentials=credentials)
                zone = "us-central1-a"
                cluster = cluster_manager_client.get_cluster(name=f'projects/{project_id}/locations/{zone}/clusters/{expected_result}')
                print (cluster.endpoint)
            except Exception as e:
                is_present = False
            test_object.update_pre_result(testcase_description,expected_result)
            if is_present==True:
                test_object.update_result(1,expected_result,actual,"No Comment"," Congrats! You have done it right!") 
            else:
                test_object.update_result(0,expected_result,actual,"Check instance name","https://cloud.google.com/bigtable/docs/")   

        except Exception as e:    
            test_object.update_result(-1,expected_result,"Internal Server error","Please check with Admin","")
            test_object.eval_message["testcase_check_ServiceAccount_name"]=str(e)                

    def testcase_check_Workload_name(self,test_object,credentials,project_id):
        testcase_description="Check GKE Workload name"
        expected_result='gke-nginx'
        
        try:
            is_present = False
            actual = 'GKE Workload name is not '+ expected_result
            try:
                
                service = discovery.build('container', 'v1', credentials=credentials)
                
                cluster_manager_client = container_v1.ClusterManagerClient(credentials=credentials)
                Cluster_id = "gke-cluster-1"
                zone = "us-central1-a"
                cluster = cluster_manager_client.get_cluster(name=f'projects/{project_id}/locations/{zone}/clusters/{Cluster-id}')
                print (cluster.endpoint)
                request = service.projects().zones().clusters().list(projectId=project_id, zone='-')
                response = request.execute()  
                if 'clusters' in response:
                    for cluster in response['clusters']:
                        print("%s,%s,%d" % (project_id, cluster['name'], cluster['currentNodeCount']))  
                        if cluster['currentNodeCount'] == expected_result:
                            is_present = True
                            break
                        
            except Exception as e:
                is_present = False
            test_object.update_pre_result(testcase_description,expected_result)
            if is_present==True:
                test_object.update_result(1,expected_result,actual,"No Comment"," Congrats! You have done it right!") 
            else:
                test_object.update_result(0,expected_result,actual,"Check instance name","https://cloud.google.com/bigtable/docs/")   

        except Exception as e:    
            test_object.update_result(-1,expected_result,"Internal Server error","Please check with Admin","")
            test_object.eval_message["testcase_check_ServiceAccount_name"]=str(e)                

def start_tests(credentials, project_id, args):

    if "result_output" not in sys.modules:
        importlib.import_module("result_output")
    else:
        importlib.reload(sys.modules[ "result_output"])
    
    test_object=ResultOutput(args,Activity)
    challenge_test=Activity()
    challenge_test.testcase_check_GKE_Cluster_name(test_object,credentials,project_id)
    challenge_test.testcase_check_Node_numbers(test_object,credentials,project_id)
    challenge_test.testcase_check_Workload_name(test_object,credentials,project_id)

    json.dumps(test_object.result_final(),indent=4)
    return test_object.result_final()

