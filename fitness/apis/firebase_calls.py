import firebase_admin
import datetime
from firebase_admin import credentials , firestore
import pytz
IST = pytz.timezone('Asia/Kolkata')



class firebase_data_api:
    def __init__(self,path_to_certificate):
        self.cred = credentials.Certificate(path_to_certificate)
        firebase_admin.initialize_app(self.cred)
        self.db = firestore.client()

    def initialize_collection_object(self,collection_name):
        self.collection_name = collection_name
        self.collection = self.db.collection(self.collection_name)
        return self.collection

    def total_visit_count(self,gym_id):
        self.todays_visits = self.initialize_collection_object('attendance').where(u'gym_id',u'==',gym_id).stream()
        return sum(1 for _ in self.todays_visits)

    def members_added_today(self,gym_id):
        self.timestamp = datetime.datetime.now(IST)
        self.date = self.timestamp.strftime("%c").split(" ")
        self.today = "{0}{1}{2}".format(self.date[1],self.date[-3],self.date[-1])
        self.members_today = self.initialize_collection_object('memberships').where(u'gym_id',u'==',gym_id).stream()
        self.members_today_count = 0
        for self.record in self.members_today:
            self.data = self.record.to_dict()
            self.date_list = self.data["valid_from"].split(" ")
            if (self.date_list[0] + self.date_list[1].replace(",","")  + self.date_list[2]) == self.today:
                self.members_today_count += 1
        return self.members_today_count


    def total_visit_count_today(self,gym_id):
        self.timestamp = datetime.datetime.now(IST)
        self.date = self.timestamp.strftime("%c").split(" ")
        self.today = "{0}{1}{2}".format(self.date[1],self.date[-3],self.date[-1])
        self.total_visits_today = self.initialize_collection_object('attendance').where(u'gym_id',u'==',gym_id).stream()
        self.visits_today_count = 0
        for self.record in self.total_visits_today:
            self.data = self.record.to_dict()
            self.date_list = self.data["date"].split(" ")
            if (self.date_list[0] + self.date_list[1].replace(",","")  + self.date_list[2]) == self.today:
                self.visits_today_count += 1
        return self.visits_today_count


    def membership_exists(self,status,gym_id,user_id):
        self.memberships = self.initialize_collection_object('memberships').where(u'gym_id',u'==',gym_id).where(u'latest','==',bool(status)).where(u'user',u'==',user_id).stream()

        return len(list(self.memberships))

    def user_exists_in_system(self,user_id):
        self.users = self.initialize_collection_object('user').where(u'phone',u'==',user_id).stream();
        #self.users = self.initialize_collection_object('user').document(user_id).stream()
        return len(list(self.users))


    def available_dashboards(self,gym_id):
        self.dashboard, self.gym_dashboard, self.final_dashboards= [], [], []
        self.dashboards_available = self.initialize_collection_object('system_data').stream();
        for self.dashboards in self.dashboards_available:
            self.dashboard = self.dashboards.to_dict()["dashboards"]

        self.gym_dashboards = self.initialize_collection_object('gym').where(u'gym_id',u'==',gym_id).stream();
        for self.gym_dashboards_avai in self.gym_dashboards:
            self.gym_dashboard = self.gym_dashboards_avai.to_dict()["dashboards"]



        for self.i in self.dashboard:
            if self.i not in  self.gym_dashboard:
                self.final_dashboards.append(self.i)

        return self.final_dashboards





    def todays_visit(self,gym_id):
        self.attendance_record = self.initialize_collection_object('attendance').where(u'gym_id',u'==',gym_id).stream()
        self.attendance = []
        self.timestamp = datetime.datetime.now(IST)
        self.date = self.timestamp.strftime("%c").split(" ")
        self.today = "{0}{1}{2}".format(self.date[1],self.date[-3],self.date[-1])
        for self.i in self.attendance_record:
            self.records = self.i.to_dict()
            self.user_record = {}
            self.date_list = self.records["date"].split(" ")
            if (self.date_list[0] + self.date_list[1].replace(",","")  + self.date_list[2]) == self.today:
                self.users = list(self.initialize_collection_object('user').where(u'phone',u'==',self.records["user"]).stream())[0];
                self.user_details = self.users.to_dict()
                self.user_record['col1'] = self.records["date"]
                self.user_record['col2'] = self.user_details['first'] + ' ' + self.user_details["last"]
                self.user_record['col3'] = self.records["time"]
                self.attendance.append(self.user_record)
        return self.attendance


    def new_memebers(self,gym_id):
        self.attendance_record = self.initialize_collection_object('memberships').where(u'gym_id',u'==',gym_id).where(u'latest','==',True).stream()
        self.attendance = []
        self.timestamp = datetime.datetime.now(IST)
        self.date = self.timestamp.strftime("%c").split(" ")
        self.today = "{0}{1}{2}".format(self.date[1],self.date[-3],self.date[-1])
        for self.i in self.attendance_record:
            self.records = self.i.to_dict()
            self.user_record = {}
            self.date_list = self.records["valid_from"].split(" ")
            if (self.date_list[0] + self.date_list[1].replace(",","")  + self.date_list[2]) == self.today:
                self.users = list(self.initialize_collection_object('user').where(u'phone',u'==',self.records["user"]).stream())[0];
                self.user_details = self.users.to_dict()
                self.user_record['col1'] = self.records["valid"]
                self.user_record['col2'] = self.user_details['first'] + ' ' + self.user_details["last"]
                self.user_record['col3'] = self.records["price"]
                self.attendance.append(self.user_record)
        return self.attendance



    def expiring_membership(self,gym_id):
        self.attendance_record = self.initialize_collection_object('memberships').where(u'gym_id',u'==',gym_id).where(u'latest','==',True).stream()
        self.attendance = []
        self.timestamp = datetime.datetime.now(IST)
        self.date = self.timestamp.strftime("%c").split(" ")
        self.today = "{0}{1}{2}".format(self.date[1],self.date[-3],self.date[-1])
        for self.i in self.attendance_record:
            self.records = self.i.to_dict()
            self.user_record = {}
            self.date_list = self.records["valid"].split(" ")
            if (self.date_list[0] + self.date_list[1].replace(",","")  + self.date_list[2]) == self.today:
                self.users = list(self.initialize_collection_object('user').where(u'phone',u'==',self.records["user"]).stream())[0];
                self.user_details = self.users.to_dict()
                self.user_record['col1'] = self.records["valid_from"]
                self.user_record['col2'] = self.user_details['first'] + ' ' + self.user_details["last"]
                self.user_record['col3'] = self.records["price"]
                self.attendance.append(self.user_record)
        return self.attendance



    def add_dashoard(self,gym_id,dashboard):
        self.dash = self.initialize_collection_object('gym').where(u'gym_id',u'==',gym_id).stream()
        try:
            self.initialize_collection_object('gym').document(list(self.dash)[0].id).update({u'dashboards': firestore.ArrayUnion([dashboard])})
            return "cool"
        except:
            return "nope"

    def membership_expiring_today(self,gym_id):
        self.timestamp = datetime.datetime.now(IST)
        self.date = self.timestamp.strftime("%c").split(" ")
        self.today = "{0}{1}{2}".format(self.date[1],self.date[-3],self.date[-1])
        self.expiring_today = self.initialize_collection_object('memberships').where(u'gym_id',u'==',gym_id).stream()
        self.expiring_today_count = 0
        for self.record in self.expiring_today:
            self.data = self.record.to_dict()
            self.date_list = self.data["valid"].split(" ")
            if (self.date_list[0] + self.date_list[1].replace(",","")  + self.date_list[2]) == self.today:
                self.expiring_today_count += 1
        return self.expiring_today_count



    def membership_details(self,gym_id,user_id):
        self.attendance_record = self.initialize_collection_object('memberships').where(u'gym_id',u'==',gym_id).where(u'latest','==',True).where(u'user','==',user_id).stream()
        self.end_date, self.price, self.comments = "","",""
        for self.it in self.attendance_record:
            self.i = self.it.to_dict()
            self.end_date = self.i['valid']
            self.price = self.i['price']
            try:
                self.comments = self.i['comments']
            except:
                pass


        return {'valid':self.end_date,'price':self.price,'comments':self.comments}




