import boto3
import botocore.exceptions as b
import json
import logging
import time
logging.basicConfig(level="INFO")
class Aws_Vpc:
	def __init__(self,V_File):
		self.V_Netfile=V_File
	def subnet_create(self,vpc,V_Subnet,V_Ec2):
		V_Sub_List=[]
		for V_Sub in V_Subnet.keys():
			V_Subname=V_Subnet[V_Sub]["sub_name"]
			V_Subcidr=V_Subnet[V_Sub]["sub_cidr"]
			V_Stype=V_Subnet[V_Sub]["private"]
			logging.info("CREATING SUBNET")
			subnet = V_Ec2.create_subnet(CidrBlock=V_Subcidr, VpcId=vpc.id)
			time.sleep(10)
			subnet.create_tags(Tags=[{"Key":"Name","Value":V_Subname}])
			logging.info("subnet {} created sucessfully......".format(V_Subname))
			V_Sub_List.append(subnet)
		return V_Sub_List
	def create_router():
		pass
	def storing_info(self,vpc,ec2,V_Igw):	
		logging.info("storing vpc info into cmdb")
		logging.info("vpc info stored sucessfully....")
		logging.info("createing internet gatewat......")
		V_Ig = ec2.create_internet_gateway()
		V_Ig.create_tags(Tags=[{"Key":"Name","Value":V_Igw["Igwname"]}])
		V_Igw["VpcId"]=vpc.id
		logging.info("igw created sucessfully.... with name {} and id {}".format(V_Ig.tags,V_Ig.id))
		logging.info("Attaching the igw with vpc")
		time.sleep(5)
		vpc.attach_internet_gateway(InternetGatewayId=V_Ig.id)
		logging.info("igw attached with vpc sucessfully.....")
		return V_Ig
	def vpc_check_exist(self,V_Net_Info):
		V_Name=V_Net_Info["VpcName"]
		V_Cidr=V_Net_Info["VpcCidr"]
		logging.info("{} checking vpc ".format(V_Name))
		time.sleep(5)	
		ec2 = boto3.resource('ec2')
		try:
			
			vpc = ec2.create_vpc(CidrBlock=V_Cidr)	
			logging.info("{} virtual network is not exist".format(V_Cidr))
			vpc.create_tags(Tags=[{"Key": "Name", "Value": V_Name}])
			vpc.wait_until_available()
			logging.info("CREATING THE VPC.......")
			time.sleep(10)
			logging.info("{} virtual network with addresspace {} created sucessfully".format(V_Name,V_Cidr))
			return vpc,ec2
		except b.ClientError as V_Error:
			logging.error("{} network space already reserved".format(V_Cidr))
			logging.error("TERMINATING THE PROCESS.............")
			time.sleep(5)
			exit(1234)
	def vpc_processing(self):
		fp=open(self.V_Netfile)
		try:
			V_Net_Info=json.load(fp)
			fp.close()
			logging.info("{} file is in good state: sending for network existence".format(self.V_Netfile))
			V_Vpc,V_Ec2=self.vpc_check_exist(V_Net_Info["aws_vpc"]["Vpc"])
			V_Ig=self.storing_info(V_Vpc,V_Ec2,V_Net_Info["aws_vpc"]["Igw"])
			V_Sub_List=self.subnet_create(V_Vpc,V_Net_Info["aws_vpc"]["subnet"],V_Ec2)
			print V_Sub_List
		except ValueError as V_Error:
			logging.error("{} is not in good state check below lines".format(self.V_Netfile))
			print V_Error
		
A=Aws_Vpc("network1.json")
A.vpc_processing()

