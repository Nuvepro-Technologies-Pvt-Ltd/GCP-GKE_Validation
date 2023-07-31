import json,os,time,logging

class ResultOutput:

    #index =0
    def __init__(self,args,class_object):
        # logging.info("step 1")
        # print("entered init block")
        self.index=-1
        self.output=None
        self.testcases=[]
        self.testcase_method=""
        self.method_list=None
        #current_testcase_method=""
        self.summary= {
            "totalTests": 0,
            "Passed": 0,
            "Failed": 0,
            "Errored": 0,
            "eval":1
        }
        self.eval_message={}
        time.sleep(1)
        try:
            #logging.info("step 2")
            logging.info("Opening file resultTemplate.json")
            result_resource=open(str(os.path.dirname(os.path.realpath(__file__)).replace('\\','/'))+"/resultTemplate.json")
            logging.info("opening file resultTemplate.json complete")
            logging.info("loading contents of resultTemplate.json")
            self.output=json.load(result_resource)
            #logging.info("step 3")
            logging.info("loaded contents of resultTemplate.json")
            result_resource.close()
            logging.info("closed file resultTemplate.json")
            #logging.info("step 4")
        except Exception as e:
            logging.info(str(e))   
     
        
        try: 
            if "token" in json.loads(args).keys():
            #logging.info("step 5")
                print(json.loads(args).keys())
                self.output["context"]["token"]=json.loads(args)['token']
                #logging.info("step 6")
            else:
            #logging.info("step 7")
                self.output["context"]["args"]=json.loads(args)
                #logging.info("step 8")
        except Exception as e:
            logging.info(str(e))
            logging.info("Malformed json input argumnets") 

        self.method_list = [attribute for attribute in dir(class_object) if callable(getattr(class_object, attribute)) and attribute.startswith('testcase') is True]

        #self.testcases=testcase_list
        #logging.info("step 11")

    def update_pre_result(self,description="",expected=""):

        template={"index":0,
            "testCase": "",
            "expected": "",
            "actual": "",
            "status": "",
            "comments": "",
            "ref": ""
            }
        self.index+=1
    #self.testcase_method != self.method_list[ self.index+=1]:
        self.testcase_method=self.method_list[ self.index]
        template["index"]=self.index
        template["testCase"]="{{"+str(self.method_list[self.index])+"_description"+"}}"
        template["expected"]="{{"+str(self.method_list[self.index])+"_expected"+"}}"
        template["actual"]="{{"+str(self.method_list[self.index])+"_actual"+"}}"
        template["status"]=0
        template["comments"]="{{"+str(self.method_list[self.index])+"_comments"+"}}"
        template["ref"]="{{"+str(self.method_list[self.index])+"_ref"+"}}"
        self.testcases.append(template)
        self.testcases[self.index]["testCase"]=description
        self.testcases[self.index]["expected"]=expected
        self.summary["totalTests"]+=1
            

    def update_result(self,result,expected=None,actual=None,comment=None,ref=None):
        if actual !=None:
            self.testcases[self.index]["expected"]=expected 
        if comment !=None:
            self.testcases[self.index]["comments"]=comment
        if actual !=None:
            self.testcases[self.index]["actual"]=actual 
        if ref !=None:
            self.testcases[self.index]["ref"]=ref        
        self.testcases[self.index]["status"]=result

        if result == 1:
            self.summary["Passed"]+=1
            #self.summary["totalTests"]+=1
        elif result == 0:
            self.summary["Failed"]+=1
            #self.summary["totalTests"]+=1
        elif result == -1:
            self.summary["Errored"]+=1
            self.summary["eval"]=0
            #self.summary["totalTests"]+=1
        #print(self.testcases)
        return 

    def result_final(self):
        self.output["testCases"]=self.testcases
        self.output["summary"]["totalTests"]=self.summary["totalTests"]+self.summary["Errored"]
        self.output["summary"]["Passed"]=self.summary["Passed"]
        self.output["summary"]["Failed"]=self.summary["Failed"]
        self.output["summary"]["Errored"]=self.summary["Errored"]
        self.output["evaluation"]["status"]=self.summary["eval"]
        self.output["evaluation"]["message"]=self.eval_message
        return json.dumps(self.output)
