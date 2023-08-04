from result_output import *
import sys
import json
import importlib.util
import urllib.request
from googleapiclient import discovery
from google.oauth2 import service_account
from pprint import pprint
from google.cloud import storage
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
                            is_present = True
                            actual=expected_result
                            break
                        else:
                            actual = cluster['name']
                            pass
            except Exception as e:
                is_present = False
            test_object.update_pre_result(testcase_description,expected_result)
            if is_present==True:
                test_object.update_result(1,expected_result,actual,"No Comment"," Congrats! You have done it right!") 
            else:
                test_object.update_result(0,expected_result,actual,"Check GKE Cluster","https://cloud.google.com/kubernetes-engine/docs/concepts/autopilot-overview?_ga=2.2930998.-76994253.1691030875")   

        except Exception as e:    
            test_object.update_result(-1,expected_result,"Internal Server error","Please check with Admin","")
            test_object.eval_message["testcase_check_GKE_Cluster_name"]=str(e)                

    def testcase_check_Node_numbers(self,test_object,credentials,project_id):
        testcase_description="Check GKE Cluster Nodes Count"
        expected_result=1
        try:
            is_present = False
            actual = 'GKE Cluster nodes is not '+ str(expected_result)
            try:
                service = discovery.build('container', 'v1', credentials=credentials)
                request = service.projects().zones().clusters().list(projectId=project_id, zone='-')
                response = request.execute()  
                if 'clusters' in response:
                    for cluster in response['clusters']:
                        if cluster['currentNodeCount'] == expected_result:
                            is_present = True
                            actual=expected_result
                            break
                        else:
                            actual=cluster['currentNodeCount']
                            pass
            except Exception as e:
                is_present = False
            test_object.update_pre_result(testcase_description,expected_result)
            if is_present==True:
                test_object.update_result(1,expected_result,actual,"No Comment"," Congrats! You have done it right!") 
            else:
                test_object.update_result(0,expected_result,actual,"Check Node","https://cloud.google.com/kubernetes-engine/docs")   

        except Exception as e:    
            test_object.update_result(-1,expected_result,"Internal Server error","Please check with Admin","")
            test_object.eval_message["testcase_check_Node_numbers"]=str(e)                

    def testcase_check_Workload_name(self,test_object,credentials,project_id):
        testcase_description="Check GKE Workload name"
        expected_result='gke-nginx'
        
        try:
            is_present = False
            actual = 'GKE Workload name is not '+ expected_result
            try:
                
                cluster_id="gke-cluster-1"
                zone = "us-central1-c"
                service = discovery.build('container', 'v1', credentials=credentials)
                request = service.projects().zones().clusters().list(projectId=project_id, zone='-')
                response = request.execute()  
                if 'clusters' in response:
                    for cluster in response['clusters']:
                        zone = cluster['zone']
                cluster_manager_client = container_v1.ClusterManagerClient(credentials=credentials)
                cluster = cluster_manager_client.get_cluster(name=f'projects/{project_id}/locations/{zone}/clusters/{cluster_id}')
                endpoint = cluster.endpoint
                
                configuration = client.Configuration()
                configuration.host = "https://"+endpoint+":443"
                configuration.verify_ssl = False
                #ctoken="ya29.c.b0Aaekm1I6TwWbv--BemJ9isutDZzUk1W0jTelKXdncJaYIhC_1MqvUZ6JBtFrOQsLrSiJKmVkNedJzfF5RzziR-h368ZcCUfs52qw5qWMZ19XtupdS9N-gHF4VdjR3J1TmReX3MIdBLt_Y35uv4m-dy6lS-P2kKy_pHFb9VVKKUxa5JwPqyhW_LBo36UC4y2F6qbUcssZ3JMoK307svkcwfNHh_qfFUG3j3kl4dgX7uY1k7byGsPcPRpR2gX_N9Xv3v9SR3KLZLooqBBICphZPQ-HQMOYlUjXb89bY3s7SkK4yyu1bSWkTZofoYc3iS_anqzCTy8eMQH339P2V28UqU8JyteM_craOOdF1biRen-OMQJq-c_2U9feyhR09cdJdsbcId3-UwJUS4uateMvOgartr1vqWMilwbZcZvX3-mxukher90s9mkjOzksWgzjolWMb4cqUOtJ5Y0vUkO_1wswiWOcjrVdlmBy-BrrQ5Rrtyqsg3quIXFMx-1thMX_urxXBdOtv_21Z_VzyYuxgQYfMQWZffvos4YsRWYeO0-XxwpWwk6coQJJUbQwJaFJUwuxdcj6qhs3Jk-IuX8zMWBhYq5-XFSgr404UzS4eww9aQdiikhf5YetJVj_jBQQbt3bkhdIU-iraci5-jpQtFpF2_Bsuxv-1jOcvUVkgQ8RQbw34bY_SWdQqOUyWX7BUzJ9p8fzQozmZ7BeFohwd0_Q-RWo2Y-ZvFcaQ7YVrIeomoeUwvV4iZmiv9-R_7X78I5sWt4flxrVXq9i8WxesmcZpd3Oyy0vMxibqwZpwlxfUe0d7mdzW441hsdrFs3fWib6IMVleBs1njlwoq9s6rZ51SJvZfUh9fxnfb2eUz34X55Wrga_pYzUoXXisQa33uS1Jfv2_snFiX_nBlwQz6ZzVmzudBV09yaVzM23d7ZskRavuW464bluJp0wyUs5rWbSkOX-gUZor_9di6l8QByFpbJQmoaIkfZaM19Sfctyjqx7muipS6w"
                configuration.api_key = {"authorization": "Bearer " + credentials.token}
                client.Configuration.set_default(configuration)
                v1 = client.CoreV1Api()
                pods = v1.list_pod_for_all_namespaces(watch=False)
                for i in pods.items:
                    wload = i.metadata.labels['app']
                    if (wload == expected_result):
                        is_present = True
                        actual=expected_result
                        break
                    else:
                        actual=wload
                        pass
            except Exception as e:
                is_present = False
            test_object.update_pre_result(testcase_description,expected_result)
            if is_present==True:
                test_object.update_result(1,expected_result,actual,"No Comment"," Congrats! You have done it right!") 
            else:
                test_object.update_result(0,expected_result,actual,"Check Workload name","https://cloud.google.com/kubernetes-engine/docs/")   

        except Exception as e:    
            test_object.update_result(-1,expected_result,"Internal Server error","Please check with Admin","")
            test_object.eval_message["testcase_check_Workload_name"]=str(e)                

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

