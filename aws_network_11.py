import json
import logging
import boto3
import time
logging.basicConfig(level="INFO",format='%(asctime)s:%(message)s')
class Aws_vpc:
	def __init__(self):
		self.V_Fp=open("network3.json")
		self.V_Ec2_Res=boto3.resource("ec2")
		self.V_Ec2_Client=boto3.client("ec2")
		try:
			self.V_Json=json.load(self.V_Fp)
			self.V_Fp.close()
			logging.info("network3.json is in good state...")
		except ValueError as V_Error:
			logging.error("{} in networ3.json".format(V_Error))
	def vpc_craete(self):
		V_Flag=False
		V_Vpcname=self.V_Json["aws_vpc"]["Vpc"]["VpcName"]
		V_Vpccidr=self.V_Json["aws_vpc"]["Vpc"]["VpcCidr"]
		logging.info("Checking Existance of Address Space :{}".format(V_Vpccidr))
		V_Vpc_Data=self.V_Ec2_Client.describe_vpcs()
		for i in range(len(V_Vpc_Data["Vpcs"])):
				if V_Vpccidr == V_Vpc_Data["Vpcs"][i]['CidrBlock']:
					V_Flag=True
		if V_Flag== True:
			logging.error("Address space {} is already exist...:".format(V_Vpccidr))
			time.sleep(10)
			exit(1234)
		logging.info("going to create virtual network...")
		self.vpc = self.V_Ec2_Res.create_vpc(CidrBlock=V_Vpccidr)
		self.vpc.create_tags(Tags=[{"Key": "Name", "Value": V_Vpcname}])
		logging.info("virtual network created sucessfully....with address sapce {}".format(V_Vpccidr))
V_Vpc=Aws_vpc()
V_Vpc.vpc_craete()
		
