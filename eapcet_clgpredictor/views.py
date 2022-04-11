from ctypes import sizeof
from django.forms.widgets import PasswordInput
from django.shortcuts import render
from django.urls.base import clear_script_prefix
from .forms import ClgPredictorForm
from .models import ClgsCutoffs
from django.db.models import Q,Count

"""
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
"""

"""
    AP_EAPCET_RANK = forms.IntegerField(widget=forms.TextInput)
    Gender = forms.ChoiceField(choices = gender_choices,widget = forms.RadioSelect)
    category = forms.ChoiceField(choices=category_choices)
"""

branch_type = (
        ("AI","ARTIFICIAL INTELLIGENCE"),
        ("DS","DATA SCIENCE"),
        ("AIM","ARTIFICIAL INTELLIGENCE AND MACHINE LEARNING"),
        ("AID","ARTIFICIAL INTELLIGENCE AND DATA SCIENCE"),
        ("CIC","CSE(IoT AND CYBER SECURITY INCLUDING BLOCKCHAIN)"),
        ("CSM","COMPUTER SCIENCE AND BUSINESS SYSTEM"),
        ("CSC","COMPUETER SCIENCE AND ENGINEERING (CYBER SECURITY)"),
        ("CSD","COMPUTER SCIENCE AND ENGINNERING(DATA SCIENCE)"),
        ("CSE","COMPUTER SCIENCE AND ENGINEERING"),
        ("CAI","COMPUTER SCIENCE AND ARTIFICIAL INTELLIGENCE"),
        ("CSI","COMPUTER SCIENCE AND INFORMATION TECHNOLOGY"),
        ("CSM","COMPUTER SCIENCE AND ENGINEERING(ARTIFICIAL INTELLIGENCE AND MACHINE LEARNING)"),
        ("CSN","COMPUTER SCIENCE AND ENGINEERING(COMPUTER NETWORKS)"),
        ("CSO","COMPUTER SCIENCE AND ENGINEERING(IoT)"),
        ("CSW","COMPUTER ENGINEERING(SOFTWARE ENGINEERING)"),
        ("INF","INFORMATION TECHNOLOGY"),
        ("CME","COMPUTER ENGINEERING"),
        ("CST","COMPUTER SCIENCE AND TECHNOLOGY"),
        ("DTD","DIGITAL TECHNIQUES AND DESIGN FOR PLANNING"),
        ("ITE","INFORMATION TECHNOLOGY AND ENGINEERING"),
        ("BME","BIO MEDICAL ENGINEERING"),
        ("ECE","ELECTRONICS AND COMMUNICATION ENGINEERING"),
        ("ECI","ELECTONICS COMMUNICATION AND INSTRUMENTATION ENGINEERING"),
        ("ECM","ELECTRONICS AND COMPUTER ENGINNERING"),
        ("EEE","ELECTONICS AND ELECTRICAL ENGINEERING"),
        ("EIE","ELECTRONICS AND INSTRUMENTATION ENGINEERING"),
        ("ETM","ELECTRONICS AND TELEMATICS"),
        ("ANE","AERONAUTICAL ENGINEERING"),
        ("AUT","AUTOMOBILE ENGINEERING"),
        ("CIV","CIVIL ENGINEERING"),
        ("IPE","INDUSTRIAL AND PRODUCTION ENGINEERING"),
        ("MCT","MECHANICAL(MECHTRONICS) ENGINEERING"),
        ("MEC","MECHANICAL ENGINEERING"),
        ("MET","METALLURGICAL ENGINEERING"),
        ("MMS","BTECH METALLURICAL AND MTECH MANUFACTURING SYSTEMS"),
        ("MMT","METALLURGY AND MATERIAL ENGINEERING"),
        ("MTE","BTECH MECHANICAL AND MTECH THERMAL ENGINEERING"),
        ("PLG","PLANNING ENGINEERING"),
        ("AGR","AGRICULTURE ENGINEERING"),
        ("BIO","BIO TECHNOLOGY ENGINEERING"),
        ("CHE","CHEMICAL ENGINEERING"),
        ("DRG","DAIRYING"),
        ("FDS","FOOD SCIENCE"),
        ("FPT","FOOD PROCESSING TECHNOLOGY"),
        ("FSP","FACILITIES AND SERVICE PLANNING"),
        ("MIN","MINING ENGINEERING"),
        ("TEX","TEXTILE TECHNOLOGY"),
        ("PHM","B.Pharmacy"),
        ("PET","PETROLEUM ENGINEERING TECHNOLOGY"),
        ("CAD","CSE (ARTIFICIAL INTELLIGENCE & DATA SCEINCE)"),
        ("PEE","PETROLEUM ENGINEERING"),
        ("CS","CYBER SECURITY"),
        ("PHD","PHARM.D(MPC STREAM)"),
        ("FDE","FOOD ENGINEERING"),
        ("PCE","PETRO CHEMICAL ENGINEERING"),
        ("CIT","COMPUTER SCIENCE AND INFORMATION TECHNOLOGY"),
        ("PHE","PHARMACEUTICAL ENGINEERING"),
        ("AMG","3D ANIMATIONS AND GRAPHICS"),
        ("CSB","COMPUTER SCIENCE AND BUSINESS SYSTEMS"),
        ("IOT","INTERNET OF THINGS"),
        ("CBA","COMPUTER SCIENCE ENGINEERING (BIG DATA ANALYTICS)"),
        ("ASE","AEROSPACE ENGINEERING"),
        ("CER","CERAMIC ENGINEERING"),
        ("GIN","GEO-INFORMATICS ENGINEERING"),
        ("IST","INSTRUMENTATION ENGINEERING AND TECHNOLOGY"),
        ("NAM","NAVAL ARCHITECTURE AND MARINE ENGINEERING"),
        ("MRB","MECHANICAL ENGINEERING (ROBOTICS)"),
        ("CSS","COMPUTER SCIENCE AND SYSTEMS ENGINEERING"),
        ("ECT","ELECTRONICS AND COMMUNICATION TECHNOLOGY"),
        ("RBT","ROBOTICS"),
        ("CCT","CONSTRUCTION TECHNOLOGY"),
        ("FDT","FOOD TECHNOLOGY"),

        
    )


# Create your views here.
all_clgs = ClgsCutoffs.objects.all()
branches = ClgsCutoffs.objects.values('branch_code').distinct()
clgs_charts = []
district_charts = []
region_charts = []
branch_charts = []
fees_lt30k_charts =0
fees_30k_70k_charts = 0
fee_gt70k_charts = 0
clgs_low_charts = 0
clgs_medium_charts =0
clgs_high_charts = 0

def get_colleges_oc(rank,gender):
    if rank <= 10000:
       low_comparator = 800+rank
       high_comparator = 2400+rank
    else:
        low_comparator = 800+rank+1000
        high_comparator = 2400+rank+1000
    global district_charts
    global region_charts
    global branch_charts
    global fees_lt30k_charts
    global fees_30k_70k_charts
    global fee_gt70k_charts
    global clgs_low_charts
    global clgs_medium_charts
    global clgs_high_charts
    clgs=[]
    if gender=="M":
        branch_charts = ClgsCutoffs.objects.values("branch_code").filter(oc_boys_cr__gte=rank).annotate(bcount=Count("branch_code"))
        region_charts = ClgsCutoffs.objects.values("reg_type","inst_code").annotate(rcount=Count("reg_type")).filter(oc_boys_cr__gte=rank)
        district_charts = ClgsCutoffs.objects.values("dist","inst_code").annotate(dcount=Count("dist")).filter(oc_boys_cr__gte=rank)
        fees_lt30k_charts = all_clgs.filter(oc_boys_cr__gte=rank,college_fee__lte = 30000).count()
        fees_30k_70k_charts = all_clgs.filter(oc_boys_cr__gte=rank,college_fee__gt = 30000,college_fee__lte=70000).count()
        fee_gt70k_charts = all_clgs.filter(oc_boys_cr__gte=rank,college_fee__gt = 70000).count()
        clgs_low_charts = all_clgs.filter(oc_boys_cr__gte=rank,oc_boys_cr__lte = low_comparator).count()
        clgs_medium_charts = all_clgs.filter(oc_boys_cr__gte=rank,oc_boys_cr__gt = low_comparator,oc_boys_cr__lte=high_comparator).count()
        clgs_high_charts =  all_clgs.filter(oc_boys_cr__gte=rank,oc_boys_cr__gt = high_comparator).count()
        clgs= all_clgs.filter(oc_boys_cr__gte=rank).order_by("oc_boys_cr")
        
    else:
        branch_charts = ClgsCutoffs.objects.values("branch_code").annotate(bcount=Count("branch_code")).filter(Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank))
        region_charts = ClgsCutoffs.objects.values("reg_type","inst_code").annotate(rcount=Count("reg_type")).filter(Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank))
        district_charts = ClgsCutoffs.objects.values("dist","inst_code").annotate(dcount=Count("dist")).filter(Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank))
        fees_lt30k_charts = all_clgs.filter(Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),college_fee__lte = 30000).count()
        fees_30k_70k_charts= all_clgs.filter(Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),college_fee__gt = 30000,college_fee__lte=70000).count()
        fee_gt70k_charts = all_clgs.filter(Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),college_fee__gt = 70000).count()
        clgs_low_charts = all_clgs.filter(Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),oc_girls_cr__lte = low_comparator).count()
        clgs_medium_charts = all_clgs.filter(Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),oc_girls_cr__gt = low_comparator,oc_girls_cr__lte = high_comparator).count()
        clgs_high_charts = all_clgs.filter(Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),oc_girls_cr__gt = high_comparator).count()
        clgs = all_clgs.filter(Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank)).order_by("oc_girls_cr")

    print(region_charts)
    print(district_charts)
    return clgs

def get_colleges_bca(rank,gender):
    if rank <= 10000:
       low_comparator = 800+rank
       high_comparator = 2400+rank
    else:
        low_comparator = 800+rank+1000
        high_comparator = 2400+rank+1000
    global district_charts
    global region_charts
    global branch_charts
    global fees_lt30k_charts
    global fees_30k_70k_charts
    global fee_gt70k_charts
    global clgs_low_charts
    global clgs_medium_charts
    global clgs_high_charts
    clgs=[]

    # oc_clgs = get_colleges_oc(rank,gender)
    if gender=="M":
        branch_charts = ClgsCutoffs.objects.values("branch_code").filter(Q(bca_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank)).annotate(bcount=Count("branch_code"))## linegraph
        region_charts = ClgsCutoffs.objects.values("reg_type","inst_code").filter(Q(bca_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank)).annotate(rcount = Count("reg_type")) ## pie
        district_charts = ClgsCutoffs.objects.values("dist","inst_code").filter(Q(bca_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank)).annotate(dcount = Count("dist")) ## bar 
        fees_lt30k_charts = all_clgs.filter(Q(bca_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank),college_fee__lte = 30000).count() ## pie
        fees_30k_70k_charts = all_clgs.filter(Q(bca_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank),college_fee__gt = 30000,college_fee__lte = 70000).count()
        fee_gt70k_charts = all_clgs.filter(Q(bca_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank),college_fee__gt = 70000).count()
        clgs_low_charts = all_clgs.filter(Q(bca_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank),bca_boys_cr__lte = low_comparator).count() ## doughnut 
        clgs_medium_charts = all_clgs.filter(Q(bca_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank),bca_boys_cr__gt = low_comparator,bca_boys_cr__lte = high_comparator).count()
        clgs_high_charts = all_clgs.filter(Q(bca_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank),bca_boys_cr__gt = high_comparator ).count()
        clgs=(all_clgs.filter(Q(bca_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank))).order_by("bca_boys_cr")

    else:
        branch_charts = ClgsCutoffs.objects.values("branch_code").filter(Q(bca_boys_cr__gte=rank)|Q(bca_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank)).annotate(bcount=Count("branch_code"))
        region_charts = ClgsCutoffs.objects.values("reg_type","inst_code").filter(Q(bca_boys_cr__gte=rank)|Q(bca_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank)).annotate(rcount = Count("reg_type"))
        district_charts = ClgsCutoffs.objects.values("dist","inst_code").filter(Q(bca_boys_cr__gte=rank)|Q(bca_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank)).annotate(dcount = Count("dist"))
        fees_lt30k_charts = all_clgs.filter(Q(bca_boys_cr__gte=rank)|Q(bca_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),college_fee__lte = 30000).count()
        fees_30k_70k_charts = all_clgs.filter(Q(bca_boys_cr__gte=rank)|Q(bca_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),college_fee__gt = 30000,college_fee__lte = 70000).count()
        fee_gt70k_charts = all_clgs.filter(Q(bca_boys_cr__gte=rank)|Q(bca_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),college_fee__gt = 70000).count()
        clgs_low_charts = all_clgs.filter(Q(bca_boys_cr__gte=rank)|Q(bca_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),bca_girls_cr__lte = low_comparator).count()
        clgs_medium_charts = all_clgs.filter(Q(bca_boys_cr__gte=rank)|Q(bca_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),bca_girls_cr__gt = low_comparator,bca_girls_cr__lte = high_comparator).count()
        clgs_high_charts = all_clgs.filter(Q(bca_boys_cr__gte=rank)|Q(bca_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),bca_girls_cr__gt = high_comparator ).count()
        clgs = all_clgs.filter(Q(bca_boys_cr__gte=rank)|Q(bca_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank)).order_by("bca_girls_cr")
    return clgs

def get_colleges_bcb(rank,gender):
    if rank <= 10000:
       low_comparator = 800+rank
       high_comparator = 2400+rank
    else:
        low_comparator = 800+rank+1000
        high_comparator = 2400+rank+1000
    global district_charts
    global region_charts
    global branch_charts
    global fees_lt30k_charts
    global fees_30k_70k_charts
    global fee_gt70k_charts
    global clgs_low_charts
    global clgs_medium_charts
    global clgs_high_charts
    clgs=[]
    # oc_clgs = get_colleges_oc(rank,gender)
    if gender=="M":
        branch_charts = ClgsCutoffs.objects.values("branch_code").filter(Q(bcb_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank)).annotate(bcount=Count("branch_code"))
        region_charts = ClgsCutoffs.objects.values("reg_type","inst_code").filter(Q(bcb_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank)).annotate(rcount = Count("reg_type"))
        district_charts = ClgsCutoffs.objects.values("dist","inst_code").filter(Q(bcb_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank)).annotate(dcount = Count("dist"))
        fees_lt30k_charts = all_clgs.filter(Q(bcb_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank),college_fee__lte = 30000).count()
        fees_30k_70k_charts = all_clgs.filter(Q(bcb_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank),college_fee__gt = 30000,college_fee__lte = 70000).count()
        fee_gt70k_charts = all_clgs.filter(Q(bcb_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank),college_fee__gt = 70000).count()
        clgs_low_charts = all_clgs.filter(Q(bcb_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank),bcb_boys_cr__lte = low_comparator).count()
        clgs_medium_charts = all_clgs.filter(Q(bcb_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank),bcb_boys_cr__gt = low_comparator,bcb_boys_cr__lte = high_comparator).count()
        clgs_high_charts = all_clgs.filter(Q(bcb_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank),bcb_boys_cr__gt = high_comparator ).count()
        clgs=(all_clgs.filter(Q(bcb_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank))).order_by("bcb_boys_cr")
    else:
        branch_charts = ClgsCutoffs.objects.values("branch_code").filter(Q(bcb_boys_cr__gte=rank)|Q(bcb_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank)).annotate(bcount=Count("branch_code"))
        region_charts = ClgsCutoffs.objects.values("reg_type","inst_code").filter(Q(bcb_boys_cr__gte=rank)|Q(bcb_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank)).annotate(rcount = Count("reg_type"))
        district_charts = ClgsCutoffs.objects.values("dist","inst_code").filter(Q(bcb_boys_cr__gte=rank)|Q(bcb_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank)).annotate(dcount = Count("dist"))
        fees_lt30k_charts = all_clgs.filter(Q(bcb_boys_cr__gte=rank)|Q(bcb_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),college_fee__lte = 30000).count()
        fees_30k_70k_charts = all_clgs.filter(Q(bcb_boys_cr__gte=rank)|Q(bcb_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),college_fee__gt = 30000,college_fee__lte = 70000).count()
        fee_gt70k_charts = all_clgs.filter(Q(bcb_boys_cr__gte=rank)|Q(bcb_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),college_fee__gt = 70000).count()
        clgs_low_charts = all_clgs.filter(Q(bcb_boys_cr__gte=rank)|Q(bcb_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),bcb_girls_cr__lte = low_comparator).count()
        clgs_medium_charts = all_clgs.filter(Q(bcb_boys_cr__gte=rank)|Q(bcb_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),bcb_girls_cr__gt = low_comparator,bcb_girls_cr__lte = high_comparator).count()
        clgs_high_charts = all_clgs.filter(Q(bcb_boys_cr__gte=rank)|Q(bcb_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),bcb_girls_cr__gt = high_comparator ).count()
        clgs = all_clgs.filter(Q(bcb_boys_cr__gte=rank)|Q(bcb_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank)).order_by("bcb_girls_cr")
    return clgs


def get_colleges_bcc(rank,gender):
    if rank <= 10000:
       low_comparator = 800+rank
       high_comparator = 2400+rank
    else:
        low_comparator = 800+rank+1000
        high_comparator = 2400+rank+1000
    global district_charts
    global region_charts
    global branch_charts
    global fees_lt30k_charts
    global fees_30k_70k_charts
    global fee_gt70k_charts
    global clgs_low_charts
    global clgs_medium_charts
    global clgs_high_charts
    clgs=[]
    # oc_clgs = get_colleges_oc(rank,gender)
    if gender=="M":
        branch_charts = ClgsCutoffs.objects.values("branch_code").filter(Q(bcc_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank)).annotate(bcount=Count("branch_code"))
        region_charts = ClgsCutoffs.objects.values("reg_type","inst_code").filter(Q(bcc_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank)).annotate(rcount = Count("reg_type"))
        district_charts = ClgsCutoffs.objects.values("dist","inst_code").filter(Q(bcc_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank)).annotate(dcount = Count("dist"))
        fees_lt30k_charts = all_clgs.filter(Q(bcc_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank),college_fee__lte = 30000).count()
        fees_30k_70k_charts = all_clgs.filter(Q(bcc_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank),college_fee__gt = 30000,college_fee__lte = 70000).count()
        fee_gt70k_charts = all_clgs.filter(Q(bcc_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank),college_fee__gt = 70000).count()
        clgs_low_charts = all_clgs.filter(Q(bcc_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank),bcc_boys_cr__lte = low_comparator).count()
        clgs_medium_charts = all_clgs.filter(Q(bcc_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank),bcc_boys_cr__gt = low_comparator,bcc_boys_cr__lte = high_comparator).count()
        clgs_high_charts = all_clgs.filter(Q(bcc_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank),bcc_boys_cr__gt = high_comparator ).count()
        clgs=(all_clgs.filter(Q(bcc_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank))).order_by("bcc_boys_cr")
    else:
        branch_charts = ClgsCutoffs.objects.values("branch_code").filter(Q(bcc_boys_cr__gte=rank)|Q(bcc_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank)).annotate(bcount=Count("branch_code"))
        region_charts = ClgsCutoffs.objects.values("reg_type","inst_code").filter(Q(bcc_boys_cr__gte=rank)|Q(bcc_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank)).annotate(rcount = Count("reg_type"))
        district_charts = ClgsCutoffs.objects.values("dist","inst_code").filter(Q(bcc_boys_cr__gte=rank)|Q(bcc_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank)).annotate(dcount = Count("dist"))
        fees_lt30k_charts = all_clgs.filter(Q(bcc_boys_cr__gte=rank)|Q(bcc_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),college_fee__lte = 30000).count()
        fees_30k_70k_charts = all_clgs.filter(Q(bcc_boys_cr__gte=rank)|Q(bcc_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),college_fee__gt = 30000,college_fee__lte = 70000).count()
        fee_gt70k_charts = all_clgs.filter(Q(bcc_boys_cr__gte=rank)|Q(bcc_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),college_fee__gt = 70000).count()
        clgs_low_charts = all_clgs.filter(Q(bcc_boys_cr__gte=rank)|Q(bcc_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),bcc_girls_cr__lte = low_comparator).count()
        clgs_medium_charts = all_clgs.filter(Q(bcc_boys_cr__gte=rank)|Q(bcc_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),bcc_girls_cr__gt = low_comparator,bcc_girls_cr__lte = high_comparator).count()
        clgs_high_charts = all_clgs.filter(Q(bcc_boys_cr__gte=rank)|Q(bcc_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),bcc_girls_cr__gt = high_comparator ).count()
        clgs = all_clgs.filter(Q(bcc_boys_cr__gte=rank)|Q(bcc_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank)).order_by("bcc_girls_cr")
    return clgs

def get_colleges_bcd(rank,gender):
    if rank <= 10000:
       low_comparator = 800+rank
       high_comparator = 2400+rank
    else:
        low_comparator = 800+rank+1000
        high_comparator = 2400+rank+1000

    global district_charts
    global region_charts
    global branch_charts
    global fees_lt30k_charts
    global fees_30k_70k_charts
    global fee_gt70k_charts
    global clgs_low_charts
    global clgs_medium_charts
    global clgs_high_charts
    clgs=[]
    # oc_clgs = get_colleges_oc(rank,gender)
    if gender=="M":
        branch_charts = ClgsCutoffs.objects.values("branch_code").filter(Q(bcd_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank)).annotate(bcount=Count("branch_code"))
        region_charts = ClgsCutoffs.objects.values("reg_type","inst_code").filter(Q(bcd_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank)).annotate(rcount = Count("reg_type"))
        district_charts = ClgsCutoffs.objects.values("dist","inst_code").filter(Q(bcd_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank)).annotate(dcount = Count("dist"))
        fees_lt30k_charts = all_clgs.filter(Q(bcd_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank),college_fee__lte = 30000).count()
        fees_30k_70k_charts = all_clgs.filter(Q(bcd_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank),college_fee__gt = 30000,college_fee__lte = 70000).count()
        fee_gt70k_charts = all_clgs.filter(Q(bcd_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank),college_fee__gt = 70000).count()
        clgs_low_charts = all_clgs.filter(Q(bcd_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank),bcd_boys_cr__lte = low_comparator).count()
        clgs_medium_charts = all_clgs.filter(Q(bcd_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank),bcd_boys_cr__gt = low_comparator,bcd_boys_cr__lte = high_comparator).count()
        clgs_high_charts = all_clgs.filter(Q(bcd_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank),bcd_boys_cr__gt = high_comparator ).count()
        clgs=(all_clgs.filter(Q(bcd_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank))).order_by("bcd_boys_cr")
    else:
        branch_charts = ClgsCutoffs.objects.values("branch_code").filter(Q(bcd_boys_cr__gte=rank)|Q(bcd_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank)).annotate(bcount=Count("branch_code"))
        region_charts = ClgsCutoffs.objects.values("reg_type","inst_code").filter(Q(bcd_boys_cr__gte=rank)|Q(bcd_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank)).annotate(rcount = Count("reg_type"))
        district_charts = ClgsCutoffs.objects.values("dist","inst_code").filter(Q(bcd_boys_cr__gte=rank)|Q(bcd_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank)).annotate(dcount = Count("dist"))
        fees_lt30k_charts = all_clgs.filter(Q(bcd_boys_cr__gte=rank)|Q(bcd_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),college_fee__lte = 30000).count()
        fees_30k_70k_charts = all_clgs.filter(Q(bcd_boys_cr__gte=rank)|Q(bcd_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),college_fee__gt = 30000,college_fee__lte = 70000).count()
        fee_gt70k_charts = all_clgs.filter(Q(bcd_boys_cr__gte=rank)|Q(bcd_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),college_fee__gt = 70000).count()
        clgs_low_charts = all_clgs.filter(Q(bcd_boys_cr__gte=rank)|Q(bcd_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),bcd_girls_cr__lte = low_comparator).count()
        clgs_medium_charts = all_clgs.filter(Q(bcd_boys_cr__gte=rank)|Q(bcd_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),bcd_girls_cr__gt = low_comparator,bcd_girls_cr__lte = high_comparator).count()
        clgs_high_charts = all_clgs.filter(Q(bcd_boys_cr__gte=rank)|Q(bcd_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),bcd_girls_cr__gt = high_comparator ).count()
        clgs = all_clgs.filter(Q(bcd_boys_cr__gte=rank)|Q(bcd_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank)).order_by("bcd_girls_cr")
    print(region_charts)
    return clgs

def get_colleges_bce(rank,gender):
    if rank <= 10000:
       low_comparator = 800+rank
       high_comparator = 2400+rank
    else:
        low_comparator = 800+rank+1000
        high_comparator = 2400+rank+1000
    
    
    global district_charts
    global region_charts
    global branch_charts
    global fees_lt30k_charts
    global fees_30k_70k_charts
    global fee_gt70k_charts
    global clgs_low_charts
    global clgs_medium_charts
    global clgs_high_charts
    clgs=[]
    # oc_clgs = get_colleges_oc(rank,gender)
    if gender=="M":
        branch_charts = ClgsCutoffs.objects.values("branch_code").filter(Q(bce_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank)).annotate(bcount=Count("branch_code"))
        region_charts = ClgsCutoffs.objects.values("reg_type","inst_code").filter(Q(bce_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank)).annotate(rcount = Count("reg_type"))
        district_charts = ClgsCutoffs.objects.values("dist","inst_code").filter(Q(bce_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank)).annotate(dcount = Count("dist"))
        fees_lt30k_charts = all_clgs.filter(Q(bce_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank),college_fee__lte = 30000).count()
        fees_30k_70k_charts = all_clgs.filter(Q(bce_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank),college_fee__gt = 30000,college_fee__lte = 70000).count()
        fee_gt70k_charts = all_clgs.filter(Q(bce_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank),college_fee__gt = 70000).count()
        clgs_low_charts = all_clgs.filter(Q(bce_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank),bce_boys_cr__lte = low_comparator).count()
        clgs_medium_charts = all_clgs.filter(Q(bce_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank),bce_boys_cr__gt = low_comparator,bce_boys_cr__lte = high_comparator).count()
        clgs_high_charts = all_clgs.filter(Q(bce_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank),bce_boys_cr__gt = high_comparator ).count()

        clgs=(all_clgs.filter(Q(bce_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank))).order_by("bce_boys_cr")
    else:
        branch_charts = ClgsCutoffs.objects.values("branch_code").filter(Q(bce_boys_cr__gte=rank)|Q(bce_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank)).annotate(bcount=Count("branch_code"))
        region_charts = ClgsCutoffs.objects.values("reg_type","inst_code").filter(Q(bce_boys_cr__gte=rank)|Q(bce_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank)).annotate(rcount = Count("reg_type"))
        district_charts = ClgsCutoffs.objects.values("dist","inst_code").filter(Q(bce_boys_cr__gte=rank)|Q(bce_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank)).annotate(dcount = Count("dist"))
        fees_lt30k_charts = all_clgs.filter(Q(bce_boys_cr__gte=rank)|Q(bce_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),college_fee__lte = 30000).count()
        fees_30k_70k_charts = all_clgs.filter(Q(bce_boys_cr__gte=rank)|Q(bce_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),college_fee__gt = 30000,college_fee__lte = 70000).count()
        fee_gt70k_charts = all_clgs.filter(Q(bce_boys_cr__gte=rank)|Q(bce_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),college_fee__gt = 70000).count()
        clgs_low_charts = all_clgs.filter(Q(bce_boys_cr__gte=rank)|Q(bce_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),bce_girls_cr__lte = low_comparator).count()
        clgs_medium_charts = all_clgs.filter(Q(bce_boys_cr__gte=rank)|Q(bce_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),bce_girls_cr__gt = low_comparator,bce_girls_cr__lte = high_comparator).count()
        clgs_high_charts = all_clgs.filter(Q(bce_boys_cr__gte=rank)|Q(bce_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),bce_girls_cr__gt = high_comparator ).count()
        clgs = all_clgs.filter(Q(bce_boys_cr__gte=rank)|Q(bce_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank)).order_by("bce_girls_cr")
    return clgs

def get_colleges_sc(rank,gender):
    if rank <= 10000:
       low_comparator = 800+rank
       high_comparator = 2400+rank
    else:
        low_comparator = 800+rank+1000
        high_comparator = 2400+rank+1000
    global district_charts
    global region_charts
    global branch_charts
    global fees_lt30k_charts
    global fees_30k_70k_charts
    global fee_gt70k_charts
    global clgs_low_charts
    global clgs_medium_charts
    global clgs_high_charts
    clgs=[]
    # oc_clgs = get_colleges_oc(rank,gender)
    if gender=="M":
        branch_charts = ClgsCutoffs.objects.values("branch_code").filter(Q(sc_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank)).annotate(bcount=Count("branch_code"))
        region_charts = ClgsCutoffs.objects.values("reg_type","inst_code").filter(Q(sc_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank)).annotate(rcount = Count("reg_type"))
        district_charts = ClgsCutoffs.objects.values("dist","inst_code").filter(Q(sc_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank)).annotate(dcount = Count("dist"))
        fees_lt30k_charts = all_clgs.filter(Q(sc_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank),college_fee__lte = 30000).count()
        fees_30k_70k_charts = all_clgs.filter(Q(sc_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank),college_fee__gt = 30000,college_fee__lte = 70000).count()
        fee_gt70k_charts = all_clgs.filter(Q(sc_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank),college_fee__gt = 70000).count()
        clgs_low_charts = all_clgs.filter(Q(sc_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank),sc_boys_cr__lte = low_comparator).count()
        clgs_medium_charts = all_clgs.filter(Q(sc_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank),sc_boys_cr__gt = low_comparator,sc_boys_cr__lte = high_comparator).count()
        clgs_high_charts = all_clgs.filter(Q(sc_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank),sc_boys_cr__gt = high_comparator ).count()
        clgs=(all_clgs.filter(Q(sc_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank))).order_by("sc_boys_cr")
    else:
        branch_charts = ClgsCutoffs.objects.values("branch_code").filter(Q(sc_boys_cr__gte=rank)|Q(sc_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank)).annotate(bcount=Count("branch_code"))
        region_charts = ClgsCutoffs.objects.values("reg_type","inst_code").filter(Q(sc_boys_cr__gte=rank)|Q(sc_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank)).annotate(rcount = Count("reg_type"))
        district_charts = ClgsCutoffs.objects.values("dist","inst_code").filter(Q(sc_boys_cr__gte=rank)|Q(sc_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank)).annotate(dcount = Count("dist"))
        fees_lt30k_charts = all_clgs.filter(Q(sc_boys_cr__gte=rank)|Q(sc_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),college_fee__lte = 30000).count()
        fees_30k_70k_charts = all_clgs.filter(Q(sc_boys_cr__gte=rank)|Q(sc_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),college_fee__gt = 30000,college_fee__lte = 70000).count()
        fee_gt70k_charts = all_clgs.filter(Q(sc_boys_cr__gte=rank)|Q(sc_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),college_fee__gt = 70000).count()
        clgs_low_charts = all_clgs.filter(Q(sc_boys_cr__gte=rank)|Q(sc_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),sc_girls_cr__lte = low_comparator).count()
        clgs_medium_charts = all_clgs.filter(Q(sc_boys_cr__gte=rank)|Q(sc_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),sc_girls_cr__gt = low_comparator,sc_girls_cr__lte = high_comparator).count()
        clgs_high_charts = all_clgs.filter(Q(sc_boys_cr__gte=rank)|Q(sc_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),sc_girls_cr__gt = high_comparator ).count()
        clgs = all_clgs.filter(Q(sc_boys_cr__gte=rank)|Q(sc_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank)).order_by("sc_girls_cr")
    return clgs

def get_colleges_st(rank,gender):
    if rank <= 10000:
       low_comparator = 800+rank
       high_comparator = 2400+rank
    else:
        low_comparator = 800+rank+1000
        high_comparator = 2400+rank+1000

    global district_charts
    global region_charts
    global branch_charts
    global fees_lt30k_charts
    global fees_30k_70k_charts
    global fee_gt70k_charts
    global clgs_low_charts
    global clgs_medium_charts
    global clgs_high_charts
    clgs=[]
    # oc_clgs = get_colleges_oc(rank,gender)
    if gender=="M":
        branch_charts = ClgsCutoffs.objects.values("branch_code").filter(Q(st_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank)).annotate(bcount=Count("branch_code"))
        region_charts = ClgsCutoffs.objects.values("reg_type","inst_code").filter(Q(st_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank)).annotate(rcount = Count("reg_type"))
        district_charts = ClgsCutoffs.objects.values("dist","inst_code").filter(Q(st_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank)).annotate(dcount = Count("dist"))
        fees_lt30k_charts = all_clgs.filter(Q(st_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank),college_fee__lte = 30000).count()
        fees_30k_70k_charts = all_clgs.filter(Q(st_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank),college_fee__gt = 30000,college_fee__lte = 70000).count()
        fee_gt70k_charts = all_clgs.filter(Q(st_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank),college_fee__gt = 70000).count()
        clgs_low_charts = all_clgs.filter(Q(st_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank),st_boys_cr__lte = low_comparator).count()
        clgs_medium_charts = all_clgs.filter(Q(st_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank),st_boys_cr__gt = low_comparator,sc_boys_cr__lte = high_comparator).count()
        clgs_high_charts = all_clgs.filter(Q(st_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank),st_boys_cr__gt = high_comparator ).count()
        clgs=(all_clgs.filter(Q(st_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank))).order_by("st_boys_cr")
    else:
        branch_charts = ClgsCutoffs.objects.values("branch_code").filter(Q(st_boys_cr__gte=rank)|Q(st_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank)).annotate(bcount=Count("branch_code"))
        region_charts = ClgsCutoffs.objects.values("reg_type","inst_code").filter(Q(st_boys_cr__gte=rank)|Q(st_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank)).annotate(rcount = Count("reg_type"))
        district_charts = ClgsCutoffs.objects.values("dist","inst_code").filter(Q(st_boys_cr__gte=rank)|Q(st_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank)).annotate(dcount = Count("dist"))
        fees_lt30k_charts = all_clgs.filter(Q(st_boys_cr__gte=rank)|Q(st_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),college_fee__lte = 30000).count()
        fees_30k_70k_charts = all_clgs.filter(Q(st_boys_cr__gte=rank)|Q(st_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),college_fee__gt = 30000,college_fee__lte = 70000).count()
        fee_gt70k_charts = all_clgs.filter(Q(st_boys_cr__gte=rank)|Q(st_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),college_fee__gt = 70000).count()
        clgs_low_charts = all_clgs.filter(Q(st_boys_cr__gte=rank)|Q(st_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),st_girls_cr__lte = low_comparator).count()
        clgs_medium_charts = all_clgs.filter(Q(st_boys_cr__gte=rank)|Q(st_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),st_girls_cr__gt = low_comparator,st_girls_cr__lte = high_comparator).count()
        clgs_high_charts = all_clgs.filter(Q(st_boys_cr__gte=rank)|Q(st_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),st_girls_cr__gt = high_comparator ).count()
        clgs = all_clgs.filter(Q(st_boys_cr__gte=rank)|Q(st_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank)).order_by("st_girls_cr")
    return clgs

def get_colleges_ews(rank,gender):
    if rank <= 10000:
       low_comparator = 800+rank
       high_comparator = 2400+rank
    else:
        low_comparator = 800+rank+1000
        high_comparator = 2400+rank+1000

    global district_charts
    global region_charts
    global branch_charts
    global fees_lt30k_charts
    global fees_30k_70k_charts
    global fee_gt70k_charts
    global clgs_low_charts
    global clgs_medium_charts
    global clgs_high_charts
    clgs=[]
    # oc_clgs = get_colleges_oc(rank,gender)
    if gender=="M":
        branch_charts = ClgsCutoffs.objects.values("branch_code").filter(Q(oc_ews_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank),Q(oc_ews_boys_cr__isnull = False)).annotate(bcount=Count("branch_code"))
        region_charts = ClgsCutoffs.objects.values("reg_type","inst_code").filter(Q(oc_ews_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank),Q(oc_ews_boys_cr__isnull = False)).annotate(rcount = Count("reg_type"))
        district_charts = ClgsCutoffs.objects.values("dist","inst_code").filter(Q(oc_ews_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank),Q(oc_ews_boys_cr__isnull = False)).annotate(dcount = Count("dist"))
        fees_lt30k_charts = all_clgs.filter(Q(oc_ews_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank),Q(oc_ews_boys_cr__isnull = False),college_fee__lte = 30000).count()
        fees_30k_70k_charts = all_clgs.filter(Q(oc_ews_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank),Q(oc_ews_boys_cr__isnull = False),college_fee__gt = 30000,college_fee__lte = 70000).count()
        fee_gt70k_charts = all_clgs.filter(Q(oc_ews_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank),Q(oc_ews_boys_cr__isnull = False),college_fee__gt = 70000).count()
        clgs_low_charts = all_clgs.filter(Q(oc_ews_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank),Q(oc_ews_boys_cr__isnull = False),oc_ews_boys_cr__lte = low_comparator).count()
        clgs_medium_charts = all_clgs.filter(Q(oc_ews_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank),Q(oc_ews_boys_cr__isnull = False),oc_ews_boys_cr__gt = low_comparator,oc_ews_boys_cr__lte = high_comparator).count()
        clgs_high_charts = all_clgs.filter(Q(oc_ews_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank),Q(oc_ews_boys_cr__isnull = False),oc_ews_boys_cr__gt = high_comparator ).count()
        clgs=(all_clgs.filter(Q(oc_ews_boys_cr__gte=rank)|Q(oc_boys_cr__gte=rank),Q(oc_ews_boys_cr__isnull = False))).order_by("oc_ews_boys_cr")
    else:
        branch_charts = ClgsCutoffs.objects.values("branch_code").filter(Q(oc_ews_boys_cr__gte=rank)|Q(oc_ews_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),Q(oc_ews_boys_cr__isnull = False),Q(oc_ews_girls_cr__isnull = False)).annotate(bcount=Count("branch_code"))
        region_charts = ClgsCutoffs.objects.values("reg_type","inst_code").filter(Q(oc_ews_boys_cr__gte=rank)|Q(oc_ews_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),Q(oc_ews_boys_cr__isnull = False),Q(oc_ews_girls_cr__isnull = False)).annotate(rcount = Count("reg_type"))
        district_charts = ClgsCutoffs.objects.values("dist","inst_code").filter(Q(oc_ews_boys_cr__gte=rank)|Q(oc_ews_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),Q(oc_ews_boys_cr__isnull = False),Q(oc_ews_girls_cr__isnull = False)).annotate(dcount = Count("dist"))
        fees_lt30k_charts = all_clgs.filter(Q(oc_ews_boys_cr__gte=rank)|Q(oc_ews_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),Q(oc_ews_boys_cr__isnull = False),Q(oc_ews_girls_cr__isnull = False),college_fee__lte = 30000).count()
        fees_30k_70k_charts = all_clgs.filter(Q(oc_ews_boys_cr__gte=rank)|Q(oc_ews_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),Q(oc_ews_boys_cr__isnull = False),Q(oc_ews_girls_cr__isnull = False),college_fee__gt = 30000,college_fee__lte = 70000).count()
        fee_gt70k_charts = all_clgs.filter(Q(oc_ews_boys_cr__gte=rank)|Q(oc_ews_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),Q(oc_ews_boys_cr__isnull = False),Q(oc_ews_girls_cr__isnull = False),college_fee__gt = 70000).count()
        clgs_low_charts = all_clgs.filter(Q(oc_ews_boys_cr__gte=rank)|Q(oc_ews_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),Q(oc_ews_boys_cr__isnull = False),Q(oc_ews_girls_cr__isnull = False),oc_ews_girls_cr__lte = low_comparator).count()
        clgs_medium_charts = all_clgs.filter(Q(oc_ews_boys_cr__gte=rank)|Q(oc_ews_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),Q(oc_ews_boys_cr__isnull = False),Q(oc_ews_girls_cr__isnull = False),oc_ews_girls_cr__gt = low_comparator,oc_ews_girls_cr__lte = high_comparator).count()
        clgs_high_charts = all_clgs.filter(Q(oc_ews_boys_cr__gte=rank)|Q(oc_ews_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),Q(oc_ews_boys_cr__isnull = False),Q(oc_ews_girls_cr__isnull = False),oc_ews_girls_cr__gt = high_comparator ).count()
        clgs = all_clgs.filter(Q(oc_ews_boys_cr__gte=rank)|Q(oc_ews_girls_cr__gte=rank)|Q(oc_boys_cr__gte=rank)|Q(oc_girls_cr__gte=rank),Q(oc_ews_boys_cr__isnull = False),Q(oc_ews_girls_cr__isnull = False)).order_by("oc_ews_girls_cr")
    return clgs



def display_form (request):
    
    
    if request.method == 'POST':
        global district_charts
        district_charts = []
        global region_charts
        region_charts = []
        global branch_charts
        branch_charts = []
        global fees_lt30k_charts
        fees_lt30k_charts = 0
        global fees_30k_70k_charts
        fees_30k_70k_charts = 0 
        global fee_gt70k_charts
        fee_gt70k_charts = 0
        global clgs_low_charts
        clgs_low_charts = 0
        global clgs_medium_charts
        clgs_medium_charts= 0
        global clgs_high_charts
        clgs_high_charts = 0
        clgs_list=[]
        form = ClgPredictorForm(request.POST or None)
        if  form.is_valid():
            gender = form.cleaned_data["Gender"]
            rank = form.cleaned_data["AP_EAPCET_RANK"]
            rank_org = form.cleaned_data["AP_EAPCET_RANK"]
            category = form.cleaned_data["category"]
            branch = dict(branch_type)
            if rank_org>=10000:
                rank = rank - 1000
            if category =="OC":
                global clgs_charts
                clgs_charts =  get_colleges_oc(rank,gender)
                clgs_list = list(get_colleges_oc(rank,gender))
            elif category =="BC-A":
                
                clgs_charts =  get_colleges_bca(rank,gender)
                clgs_list = list(get_colleges_bca(rank,gender))
            elif category =="BC-B":
                
                clgs_charts =  get_colleges_bcb(rank,gender)
                clgs_list = list(get_colleges_bcb(rank,gender))
            elif category =="BC-C":
            
                clgs_charts =  get_colleges_bcc(rank,gender)
                clgs_list = list(get_colleges_bcc(rank,gender))
            elif category =="BC-D":
                
                clgs_charts =  get_colleges_bcd(rank,gender)
                clgs_list = list(get_colleges_bcd(rank,gender))
            elif category =="BC-E":
                
                clgs_charts =  get_colleges_bce(rank,gender)
                clgs_list = list(get_colleges_bce(rank,gender))
            elif category =="SC":
                
                clgs_charts =  get_colleges_sc(rank,gender)
                clgs_list = list(get_colleges_sc(rank,gender))
            elif category =="ST":
                
                clgs_charts =  get_colleges_st(rank,gender)
                clgs_list = list(get_colleges_st(rank,gender))
            elif category =="GEN_EWS":
                
                clgs_charts =  get_colleges_ews(rank,gender)
                clgs_list = list(get_colleges_ews(rank,gender))
            else:
                
                clgs_charts =  get_colleges_st(rank,gender)
                clgs_list = list(get_colleges_st(rank,gender))
            records = len(clgs_list)
             
            return render(request,"eapcet_clgpredictor/template.html",{"clgs_list":clgs_list,"rank":rank_org,"category":category,"records":records,"branch":branch,"gender":gender,"is_paginated" : True})
        return render(request,"eapcet_clgpredictor/forms.html",{"form":form})   
    if request.method == 'GET':
        form = ClgPredictorForm()
        return render(request,"eapcet_clgpredictor/forms.html",{"form":form})

def charts_data (request):
    global district_charts
    global region_charts
    global branch_charts
    global fees_lt30k_charts
    global fees_30k_70k_charts
    global fee_gt70k_charts
    global clgs_low_charts
    global clgs_medium_charts
    global clgs_high_charts

    atp_count =0
    ctr_count =0
    eg_count = 0
    gtr_count = 0
    kdp_count = 0
    kri_count = 0
    knl_count = 0
    nlr_count = 0
    pks_count = 0
    skl_count = 0
    vsp_count = 0
    vzm_count = 0
    wg_count = 0

    svu_count =0
    au_count = 0
    

    for district in district_charts:
        if district["dist"] == "ATP":
            atp_count+=1
        elif district["dist"] == "CTR":
            ctr_count+=1
        elif district["dist"] == "EG":
            eg_count+=1
        elif district["dist"] == "GTR":
            gtr_count+=1
        elif district["dist"] == "KDP":
            kdp_count +=1
        elif district["dist"] == "KRI":
            kri_count +=1
        elif district["dist"] == "KNL":
            knl_count += 1
        elif district["dist"] == "NLR":
            nlr_count +=1
        elif district["dist"] == "PKS":
            pks_count += 1
        elif district["dist"] == "SKL":
            skl_count+= 1
        elif district["dist"] == "VSP":
            vsp_count += 1
        elif district["dist"] == "VZM":
            vzm_count += 1
        elif district["dist"] == "WG":
            wg_count += 1

    for region in region_charts:
        if region["reg_type"] == "SVU":
            svu_count += 1
        elif region["reg_type"] == "AU":
            au_count += 1
         

    districts_charts_dict = [
        {"dist":"ATP","dist_count":atp_count},
        {"dist":"CTR","dist_count":ctr_count},
        {"dist":"EG","dist_count":eg_count},
        {"dist":"GTR","dist_count":gtr_count},
        {"dist":"KDP","dist_count":kdp_count} ,
        {"dist":"KRI","dist_count":kri_count},
        {"dist":"KNL","dist_count":knl_count},
        {"dist":"NLR","dist_count":nlr_count},
        {"dist":"PKS","dist_count":pks_count},
        {"dist":"SKL","dist_count":skl_count},
        {"dist":"VSP","dist_count":vsp_count},
        {"dist":"VZM","dist_count":vzm_count},
        {"dist":"WG","dist_count":wg_count}
        ]

    region_charts_dict = [
        {"region":"SVU","reg_count":svu_count},
        {"region":"AU","reg_count":au_count}
    ]

    branch_charts_dict = branch_charts

    fees_charts_dict = [
        {"fees_cutoff":"FEE<=30,000", "clgs_count":fees_lt30k_charts},
        {"fees_cutoff":"FEE>30,000 and FEE<=70,000", "clgs_count":fees_30k_70k_charts},
        {"fees_cutoff":"FEE>70,000", "clgs_count":fee_gt70k_charts}
    ]

    chances_chart_dict = [
        {"chances":"LOW", "clgs_count":clgs_low_charts},
        {"chances":"MEDIUM", "clgs_count":clgs_medium_charts},
        {"chances":"HIGH", "clgs_count":clgs_high_charts}
    ]

    return render(request,"eapcet_clgpredictor/clgs.html",{"district_charts":districts_charts_dict,"region_charts":region_charts_dict,"branches_charts":branch_charts_dict,"fees_charts":fees_charts_dict,"chances_charts":chances_chart_dict})


