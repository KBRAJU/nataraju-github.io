import boto3
import json
import logging
import time
import botocore.exceptions as ex
logging.basicConfig(level="INFO",format='%(asctime)s:%(message)s')
class aws_vpc:
	def __init__(self):
		self.ec2=boto3.resource("ec2") 
		fp=open("network2.json")
		try:
			self.V_Data=json.load(fp)
			logging.info("network2.json file is in good state..")

		except ValueError as V_Error:
			logging.error("{} having in network2.json file".format(V_Error))
			exit(1234)
	def vpc_create(self):
		V_Vpcname=self.V_Data["aws_vpc"]["Vpc"]["VpcName"]
		V_Vpccidr=self.V_Data["aws_vpc"]["Vpc"]["VpcCidr"]
		logging.info("Go to check the exist of virtual network...")
  		VPC_obj=boto3.client("ec2")
		V_Vpc_info=VPC_obj.describe_vpcs()
		V_Flag=False
		for V_Vpcn in  range(len(V_Vpc_info['Vpcs'])):
			cidr= V_Vpc_info['Vpcs'][V_Vpcn]['CidrBlock']
			if cidr == V_Vpccidr:
				V_Flag=True
		if V_Flag == True:
			logging.error("{} Address Space overlapping.......".format(V_Vpccidr))
			time.sleep(5)	
			exit(1234)
		try:
			logging.info("Going to create virtual network with address space {}".format(V_Vpccidr))
			self.V_vpc = self.ec2.create_vpc(CidrBlock=V_Vpccidr)
			self.V_vpc.create_tags(Tags=[{"Key": "Name", "Value": V_Vpcname}])
			time.sleep(5)
			logging.info("virtual network {} created sucessfully...".format(V_Vpcname))
		except ex.EndpointConnectionError as V_Error:
			logging.error("{} error in config file".format(V_Error))
		except ex.ClientError as V_Client:
			logging.error("{} error in credentials file".format(V_Client))

	def subnet_create(self):
		#subnet = V_Ec2.create_subnet(CidrBlock=V_Subcidr, VpcId=vpc.id)
		for V_Sub in self.V_Data["aws_vpc"]["subnet"].keys():#[sun1,sunet2]
			V_Subname=self.V_Data["aws_vpc"]["subnet"][V_Sub]["sub_name"]
			V_Subcidr=self.V_Data["aws_vpc"]["subnet"][V_Sub]["sub_cidr"]
			logging.info("going to create subnet{} with address space {}".format(V_Subname,V_Subcidr))
			time.sleep(5)
			subnet = self.ec2.create_subnet(CidrBlock=V_Subcidr, VpcId=self.V_vpc.id)
			subnet.create_tags(Tags=[{"Key":"Name","Value":V_Subname}])
			logging.info(" subnet {} crerated sucessfully with address space {}".format(V_Subname,V_Subcidr))
			#print self.V_vpc.id
			#print V_Subname
			#print V_Subcidr
	def igw_create(self):
		#V_Ig = ec2.create_internet_gateway()
		V_Igname=self.V_Data["aws_vpc"]["Igw"]["Igwname"]
		logging.info("creating igw....")
		time.sleep(5)
		self.V_Igw=self.ec2.create_internet_gateway()
		self.V_Igw.create_tags(Tags=[{"Key":"Name","Value":V_Igname}])
		logging.info("igw created sucessfully....")
	def attch_igw(self):
		#vpc.attach_internet_gateway(InternetGatewayId=V_Ig.id)
		logging.info("attaching igw with vpc....")
		self.V_vpc.attach_internet_gateway(InternetGatewayId=self.V_Igw.id)
		time.sleep(5)
		logging.info("attached igw with vpc")
	def router_create(self):
		#route_table = vpc.create_route_table(VpcId='string')	
		self.route_list=[]
		for V_Router in self.V_Data["aws_vpc"]["router"].keys():
			V_Rname=self.V_Data["aws_vpc"]["router"][V_Router]["router_name"]
			logging.info("creating route table...")
			route_table = self.ec2.create_route_table(VpcId=self.V_vpc.id)
			route_table.create_tags(Tags=[{"Key":"Name","Value":V_Rname}])
			self.route_list.append(route_table)
			logging.info("{} route table created sucessfully...".format(V_Rname))
vpc=aws_vpc()
vpc.vpc_create()
vpc.subnet_create()
vpc.igw_create()
vpc.attch_igw()
vpc.router_create()
