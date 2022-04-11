from django.db import models
from django.db.models import Q

# Create your models here.
class ClgsCutoffs (models.Model):
    ownership_type = (
        ("PVT","PRIVATE"),
        ("SF","SELF FUNDED"),
        ("UNIV","UNIVERSITY"),
    )
    # region_type = (
    #     ("AU","ANDHRA UNIVERSITY"),
    #     ("SVU","SRI VENKATESWARA UNIVERSITY"),
    #     ("OU","OSMANIA UNIVERSITY"),
    # )
    # branch_type = (
    #     ("AI","ARTIFICIAL INTELLIGENCE"),
    #     ("AID","ARTIFICIAL INTELLIGENCE AND DATA SCIENCE"),
    #     ("CIC","CSE(IoT AND CYBER SECURITY INCLUDING BLOCKCHAIN)"),
    #     ("CSM","COMPUTER SCIENCE AND BUSINESS SYSTEM"),
    #     ("CSC","COMPUETER SCIENCE AND ENGINEERING (CYBER SECURITY)"),
    #     ("CSD","COMPUTER SCIENCE AND ENGINNERING(DATA SCIENCE)"),
    #     ("CSE","COMPUTER SCIENCE AND ENGINEERING"),
    #     ("CSI","COMPUTER SCIENCE AND INFORMATION TECHNOLOGY"),
    #     ("CSM","COMPUTER SCIENCE AND ENGINEERING(ARTIFICIAL INTELLIGENCE AND MACHINE LEARNING)"),
    #     ("CSN","COMPUTER SCIENCE AND ENGINEERING(COMPUTER NETWORKS)"),
    #     ("CSO","COMPUTER SCIENCE AND ENGINEERING(IoT)"),
    #     ("CSW","COMPUTER ENGINEERING(SOFTWARE ENGINEERING)"),
    #     ("INF","INFORMATION TECHNOLOGY"),
    #     ("CME","COMPUTER ENGINEERING"),
    #     ("CST","COMPUTER SCIENCE AND TECHNOLOGY"),
    #     ("DTD","DIGITAL TECHNIQUES AND DESIGN FOR PLANNING"),
    #     ("ITE","INFORMATION TECHNOLOGY AND ENGINEERING"),
    #     ("BME","BIO MEDICAL ENGINEERING"),
    #     ("ECE","ELECTRONICS AND COMMUNICATION ENGINEERING"),
    #     ("ECI","ELECTONICS COMMUNICATION AND INSTRUMENTATION ENGINEERING"),
    #     ("ECM","ELECTRONICS AND COMPUTER ENGINNERING"),
    #     ("EEE","ELECTONICS AND ELECTRICAL ENGINEERING"),
    #     ("EIE","ELECTRONICS AND INSTRUMENTATION ENGINEERING"),
    #     ("ETM","ELECTRONICS AND TELEMATICS"),
    #     ("ANE","AERONAUTICAL ENGINEERING"),
    #     ("AUT","AUTOMOBILE ENGINEERING"),
    #     ("CIV","CIVIL ENGINEERING"),
    #     ("IPE","INDUSTRIAL AND PRODUCTION ENGINEERING"),
    #     ("MCT","MECHANICAL(MECHTRONICS) ENGINEERING"),
    #     ("MEC","MECHANICAL ENGINEERING"),
    #     ("MET","METALLURGICAL ENGINEERING"),
    #     ("MMS","BTECH METALLURICAL AND MTECH MANUFACTURING SYSTEMS"),
    #     ("MMT","METALLURGY AND MATERIAL ENGINEERING"),
    #     ("MTE","BTECH MECHANICAL AND MTECH THERMAL ENGINEERING"),
    #     ("PLG","PLANNING ENGINEERING"),
    #     ("AGR","AGRICULTURE ENGINEERING"),
    #     ("BIO","BIO TECHNOLOGY ENGINEERING"),
    #     ("CHE","CHEMICAL ENGINEERING"),
    #     ("DRG","DAIRYING"),
    #     ("FDS","FOOD SCIENCE"),
    #     ("FPT","FOOD PROCESSING TECHNOLOGY"),
    #     ("FSP","FACILITIES AND SERVICE PLANNING"),
    #     ("MIN","MINING ENGINEERING"),
    #     ("TEX","TEXTILE TECHNOLOGY"),
    # )
    inst_code = models.CharField(max_length=10)
    inst_name = models.CharField( max_length=100)
    own_type  = models.CharField(max_length=5,choices=ownership_type)
    reg_type = models.CharField(max_length=5)
    dist      = models.CharField(max_length=25)
    place     = models.CharField(max_length=100)
    coed_type = models.CharField(max_length=10)
    affliated_univ = models.CharField(max_length=100)
    estd_year  = models.CharField(max_length=50)
    branch_code =models.CharField(max_length=50)
    oc_boys_cr = models.PositiveIntegerField(null=True)
    oc_girls_cr = models.PositiveIntegerField(null=True)
    sc_boys_cr =  models.PositiveIntegerField(null=True)
    sc_girls_cr = models.PositiveIntegerField(null=True)
    st_boys_cr = models.PositiveIntegerField(null=True)
    st_girls_cr = models.PositiveIntegerField(null=True)
    bca_boys_cr = models.PositiveIntegerField(null=True)
    bca_girls_cr = models.PositiveIntegerField(null=True)
    bcb_boys_cr = models.PositiveIntegerField(null=True)
    bcb_girls_cr = models.PositiveIntegerField(null=True)
    bcc_boys_cr = models.PositiveIntegerField(null=True)
    bcc_girls_cr = models.PositiveIntegerField(null=True)
    bcd_boys_cr = models.PositiveIntegerField(null=True)
    bcd_girls_cr = models.PositiveIntegerField(null=True)
    bce_boys_cr = models.PositiveIntegerField(null=True)
    bce_girls_cr =models.PositiveIntegerField(null=True)
    oc_ews_boys_cr = models.PositiveIntegerField(null=True)
    oc_ews_girls_cr = models.PositiveIntegerField(null=True)
    college_fee   = models.PositiveIntegerField(null=True)
    

    def __str__ (self):
        return f"{self.inst_code} {self.inst_name}  {self.branch_code} "