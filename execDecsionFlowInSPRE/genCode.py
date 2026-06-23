#!/opt/sasinside/anaconda3/bin/python3
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '/etc/sas/dec-spre/app')
import get_decision_code_SPRE as dc
def execute(uri, input_table, output_table, libs):
    decisionCode= dc.decisionSPRECode()
    decisionCode.setDecisionInfo(uri, input_table, output_table, libs)
    decisionCode.getAccessToken()
    decisionCode.getDecisionName()
    decisionCode.getDecisionCode()
    decisionCode.setProcDs2()
    decisionCode.modifyContactRecord()
    decisionCode.getDecisionParameters()
    decisionCode.prepareParameters()
    fileName= decisionCode.writeDecisionCode()
    return fileName



################################################################################
if __name__ == '__main__':
    
    print("-----")
    #uri= "/decisions/flows/a2de1494-038b-4ab3-9c81-0d2f5ca4e5b4/revisions/c47eb35f-9d49-4152-af58-b84d07a5709c"
    uri= "/decisions/flows/a2de1494-038b-4ab3-9c81-0d2f5ca4e5b4"
    input_table= "work.patient"
    output_table= "work.patient_out"
    libs= "WORK PGDATA"
    fileName= execute(uri, input_table, output_table, libs)
    
    print(fileName)
    print("-----")


