from odoo import models
#from datetime import datetime
from zk import ZK, const
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError , AccessDenied
import pandas as pd
#from datetime import timedelta
import datetime
#from datetime import datetime, timedelta
from datetime import  timedelta
#import datetime
import time

class AttendanceXlsxReport(models.AbstractModel):
    _name = "report.hr.attendance_report_hr_xls_employee"
    _inherit = "report.report_xlsx.abstract"
    def generate_xlsx_report(self ,workbook,data,partners):
        sheet = workbook.add_worksheet('Attendance Sheet')
        conn = None
        for branch in partners:
            if branch.choose_branch =='a':
                zk = ZK('192.168.200.233', port=4370, timeout=5)
            else:
                zk = ZK('192.168.40.40', port=4370, timeout=5)
                print('saudi')
        conn = zk.connect()
        j=0
        users = conn.get_users()
        result = conn.get_attendance()
        empty_list_group_a =[]
        empty_list_all_groups =[]
        list_temp_test_morning = []
        row_group_A = 3
        row_group_B = 3
        row_group_C = 3
        row_Saudi_Mor= 3
        row_Saudi_night= 3
        # res_branch = [('b','MorningShift')]
        shift = ''
        branch = ''
        res_group = [('a')]
        sum_worked_hours = 0
        row_all_groups = 3
        date_group_B = 1
        date_group_A = 1
        date_group_C = 1
        date_all_groups =1
        counter_group_A = 0
        counter_group_B = 0
        counter_group_C = 0
        counter_all_groups = 0
        counter_all_groups = 0
        come_employee_time = ''
        leave_employee_time = ''
        list_come_employee_time = []
        list_leave_employee_time= []
        dict_of_name ={}
        list_of_date_all_data = []
        i = 0
        temp_dict = {}
        temp_dict_night = {}
        list_of_date = []
        list_of_date_pandas = []
        list_of_pandas_month_day = []
        ninteen =19
        temp_dict_night_morning = {}
        temp_dict_night_night={}
        list_of_ids_night =[]
        mid_day =12
        temp_dict_date_leave ={}
        temp_dict_date_attend ={}
        temp_dict_date_attend_zero ={}
        temp_dict_date_leave_one ={}
        temp_dict_date_leave_one_pandas ={}
        temp_dict_date_attend_zero_pandas = {}
        list_of_ids_attend_pandas = []
        list_of_ids_e = []
        temp_dict_date_attend_zero_pandas_morning= {}
        temp_dict_date_leave_one_pandas_morning ={}
        temp_list=[]
        list_of_ids_leave=[]
        list_of_ids_attend=[]
        list_of_hours_df = []
        list_of_hours_df_madina = []
        list_of_ids_df = []
        row_temp=1
        ####################################################################
        ####              DEFINING SHEET FORMAT AND STYLE               ####
        ####################################################################
        bold = workbook.add_format({'bold': True})
        format_center = workbook.add_format({'bold': True,'align':'center'})
        format_late = workbook.add_format({'bold': True,'align':'center','bg_color':'#9A86A4'})
        format_date = workbook.add_format({'bold': True,'align':'center','bg_color':'#D0C9C0'})
        sheet.write(1,0 ,'Name' ,bold)
        sheet.write(2, 1, 'Attend',bold)
        sheet.write(2, 2, 'Leave',bold)
        sheet.write(2, 0, 'Date',bold)
        sheet.set_column('A:A' ,20)
        sheet.set_column('B:B' ,20)
        sheet.set_column('C:C' ,15)
        sheet.set_column('M:M' ,20)
        sheet.set_column('D:D' ,20)
        sheet.set_column('E:E' ,20)
        sheet.set_column('F:F' ,20)
        sheet.set_column('G:G' ,20)
        sheet.set_column('H:H' ,20)
        sheet.set_column('J:J' ,20)
        sheet.set_column('K:K' ,20)
        sheet.set_column('I:I' ,20)
        sheet.set_column('L:L' ,20)
        for obj in partners:
            print('biometric' , obj.employee_id.biometric_id)
            for user in users:
                privilege = 'User'
                if user.privilege == const.USER_ADMIN:
                    privilege = 'Admin'
                temp_list.append(user.user_id)
                temp_dict.update({user.user_id: user.name})
                conn.enable_device()
            for day in result:
                i += 1
                temp_var = str(day).split(" ")[1]
                temp_date = str(day).split(" ")[3]
                global date_worked_hours
                date_worked_hours = temp_date
                col =2
                ## nothing will change here
                if obj.choose_branch=='a':
                    if str(day).split(' ')[6] == '1)':
                        if str(temp_var + ' ' + temp_date) in temp_dict_date_leave_one_pandas:
                            duplicate_leave = temp_dict_date_leave_one_pandas.get(str(temp_var + ' ' + temp_date))
                            list_of_date_pandas.append(temp_date.split('-')[0] + '-' + temp_date.split('-')[1])
                            list_of_ids_attend_pandas.append(str(temp_var + ' ' + temp_date))
                            list_of_pandas_month_day.append(temp_date.split('-')[0] + '-' + temp_date.split('-')[1] + '-' + temp_date.split('-')[2])
                            temp_dict_date_attend_zero_pandas.update({str(temp_var + ' ' + temp_date): duplicate_leave})
                        else:
                            temp_dict_date_leave_one_pandas.update({str(temp_var + ' ' + temp_date): str(day).split(" ")[4]})
                        temp_dict_date_leave_one_pandas.update({str(temp_var + ' ' + temp_date): str(day).split(" ")[4]})
                    elif str(day).split(' ')[6] == '0)':
                        if str(temp_var + ' ' + temp_date) in temp_dict_date_attend_zero_pandas:
                            temp_dict_date_leave_one_pandas.update({str(temp_var + ' ' + temp_date): str(day).split(" ")[4]})
                        else:
                            list_of_ids_attend_pandas.append(str(temp_var + ' ' + temp_date))
                            list_of_date_pandas.append(temp_date.split('-')[0] + '-' + temp_date.split('-')[1])
                            list_of_pandas_month_day.append(
                                temp_date.split('-')[0] + '-' + temp_date.split('-')[1] + '-' + temp_date.split('-')[2])
                            temp_dict_date_attend_zero_pandas.update({str(temp_var + ' ' + temp_date): str(day).split(" ")[4]})
                elif obj.choose_branch=='b':
                    hour_no_zero = str(day).split(" ")[4].split(':')[0]
                    print('hour_no_zero', hour_no_zero)
                    if hour_no_zero[0] == '0':
                        hour_no_zero = hour_no_zero[1:]
                    try:
                        if hour_no_zero[1] == '0' and hour_no_zero[0] == '0':
                            hour_no_zero = '24'
                    except:
                        pass
                    if  (hour_no_zero >='16' and hour_no_zero <='19'):
                        list_of_ids_attend_pandas.append(str(temp_var + ' ' + temp_date))
                        list_of_date_pandas.append(temp_date.split('-')[0] + '-' + temp_date.split('-')[1])
                        list_of_pandas_month_day.append(temp_date.split('-')[0] + '-' + temp_date.split('-')[1] + '-' + temp_date.split('-')[2])
                        temp_dict_date_attend_zero_pandas.update({str(temp_var + ' ' + temp_date): str(day).split(" ")[4]})
                    elif (hour_no_zero >= '4' and hour_no_zero <='9'):
                        temp_dict_date_attend_zero_pandas_morning.update({str(temp_var + ' ' + temp_date): str(day).split(" ")[4]})
                    elif  (hour_no_zero >='20' and hour_no_zero <='24'):
                        temp_dict_date_leave_one_pandas.update({str(temp_var + ' ' + temp_date): str(day).split(" ")[4]})
                    elif (hour_no_zero >= '12' and hour_no_zero <='13'):
                        temp_dict_date_leave_one_pandas_morning.update({str(temp_var + ' ' + temp_date): str(day).split(" ")[4]})
                    ####################################################################################################################################
                hours_splited = str(day).split(" ")[4].split(":")[0]
                #########  UNTIL HERE ######
                if obj.choose_branch == 'a':
                    BioTime_id = obj.employee_id.biometric_id
                elif obj.choose_branch == 'b':
                    BioTime_id = obj.employee_id_Madina.biometric_id
                if obj.dat and obj.employee_id and  obj.choose_option =='b' and obj.date_end :
                    if temp_date >=str(obj.dat) and temp_date <= str(obj.date_end) and  BioTime_id == int(temp_var):
                        if hours_splited[0] =='0':
                            temp_time = hours_splited[1:]
                            hours_splited = temp_time
                        if str(day).split(' ')[6] == '1)':
                            if str(temp_var + ' ' + temp_date) in temp_dict_date_leave_one  and str(temp_var + ' ' + temp_date) not in temp_dict_date_attend_zero:
                                duplicate_leave = temp_dict_date_leave_one.get(str(temp_var + ' ' + temp_date))
                                try:
                                    list_of_ids_attend.remove(str(temp_var + ' ' + temp_date))
                                    list_of_date.remove(temp_date)
                                except:
                                    pass
                                list_of_ids_attend.append(str(temp_var + ' ' + temp_date))
                                list_of_date.append(temp_date)
                                temp_dict_date_attend_zero.update(
                                    {str(temp_var + ' ' + temp_date): duplicate_leave})
                                temp_dict_date_leave_one.update(
                                    {str(temp_var + ' ' + temp_date): str(day).split(" ")[4]})
                            else:
                                temp_dict_date_leave_one.update({str(temp_var + ' ' + temp_date): str(day).split(" ")[4]})
                        elif str(day).split(' ')[6] == '0)':
                            if str(temp_var + ' ' + temp_date) in temp_dict_date_attend_zero:
                                temp_dict_date_leave_one.update({str(temp_var + ' ' + temp_date): str(day).split(" ")[4]})
                            else:
                                list_of_ids_attend.append(str(temp_var + ' ' + temp_date))
                                list_of_date.append(temp_date)
                                temp_dict_date_attend_zero.update({str(temp_var + ' ' + temp_date): str(day).split(" ")[4]})
                elif obj.dat and obj.employee_id and obj.choose_option == 'b' and not obj.date_end:
                    if str(obj.dat) <= temp_date:
                        if temp_var == str(obj.employee_id.biometric_id):
                            temp_var == str(obj.employee_id.biometric_id)
                            if str(day).split(' ')[6] == '1)':
                                if str(temp_var + ' ' + temp_date) in temp_dict_date_leave_one  and str(temp_var + ' ' + temp_date) not in temp_dict_date_attend_zero:
                                    duplicate_leave = temp_dict_date_leave_one.get(str(temp_var + ' ' + temp_date))
                                    try:
                                        list_of_ids_attend.remove(str(temp_var + ' ' + temp_date))
                                        list_of_date.remove(temp_date)
                                    except:
                                        pass
                                    list_of_ids_attend.append(str(temp_var + ' ' + temp_date))
                                    list_of_date.append(temp_date)
                                    temp_dict_date_attend_zero.update(
                                        {str(temp_var + ' ' + temp_date): duplicate_leave})
                                    temp_dict_date_leave_one.update(
                                        {str(temp_var + ' ' + temp_date): str(day).split(" ")[4]})

                                else:
                                    temp_dict_date_leave_one.update({str(str(obj.employee_id.biometric_id) + ' ' + temp_date): str(day).split(" ")[4]})
                                # temp_dict_date_leave_one.update({str(str(obj.employee_id.biometric_id) + ' ' + temp_date): str(day).split(" ")[4]})
                            if str(day).split(' ')[6] == '0)':
                                if str(temp_var + ' ' + temp_date) in temp_dict_date_attend_zero:
                                    temp_dict_date_leave_one.update({str(temp_var + ' ' + temp_date): str(day).split(" ")[4]})
                                else:
                                    list_of_ids_attend.append(str(temp_var + ' ' + temp_date))
                                    list_of_date.append(temp_date)
                                    temp_dict_date_attend_zero.update({str(temp_var + ' ' + temp_date): str(day).split(" ")[4]})
                ####################### BRANCH SAUDI ARABIA  #####################
                elif obj.choose_branch =='b' and obj.choose_option == 'a' and not obj.date_end:
                    gDate = datetime.datetime(int(temp_date.split('-')[0]), int(temp_date.split('-')[1]), int(temp_date.split('-')[2]))
                    Today = gDate + timedelta(days=-1)
                    if str(obj.dat) <= temp_date:
                        hour_no_zero = str(day).split(" ")[4].split(':')[0]
                        print('hour_no_zero',hour_no_zero)
                        if hour_no_zero[0] == '0':
                            hour_no_zero = hour_no_zero[1:]
                        if str(day).split(' ')[6] == '1)':
                            if hour_no_zero == str(0)  and hour_no_zero < str(4) and str(temp_var + ' ' + temp_date) not in temp_dict_date_leave_one :
                                duplicate_leave = temp_dict_date_leave_one.get(str(temp_var + ' ' + temp_date))
                                temp_dict_date_leave_one.update({str(temp_var + ' ' + str(Today).split(' ')[0] +' '+'night'):str(day).split(" ")[4]})
                                print(str(Today).split(' ')[0],'date')
                            if str(temp_var + ' ' + temp_date) in temp_dict_date_leave_one and str(temp_var + ' ' + temp_date) in temp_dict_date_attend_zero  \
                                    and str(temp_var + ' ' + temp_date  + ' '  +'night') not in temp_dict_date_leave_one:
                                temp_dict_date_leave_one.update(
                                    {str(temp_var + ' ' + temp_date  + ' '  +'night'): str(day).split(" ")[4]})
                                print('dictionary',
                                      temp_dict_date_leave_one.get(str(temp_var + ' ' + temp_date + ' ' + 'night')))
                            elif str(temp_var + ' ' + temp_date) in temp_dict_date_leave_one and str(temp_var + ' ' + temp_date) in temp_dict_date_attend_zero \
                                and str(temp_var + ' ' + temp_date  + ' '  +'night') in temp_dict_date_leave_one and hour_no_zero <'21':
                                duplicate_leave = temp_dict_date_leave_one.get(str(temp_var + ' ' + temp_date + ' '  +'night'))
                                try:
                                    list_of_ids_attend.remove(str(temp_var + ' ' + temp_date + ' '  +'night'))
                                    list_of_date.remove(temp_date)
                                except:
                                    pass
                                list_of_ids_attend.append(str(temp_var + ' ' + temp_date  + ' '  +'night'))
                                list_of_date.append(temp_date)
                                temp_dict_date_attend_zero.update(
                                    {str(temp_var + ' ' + temp_date  + ' '  +'night'): duplicate_leave})
                                temp_dict_date_leave_one.update(
                                    {str(temp_var + ' ' + temp_date + ' '  +'night'): str(day).split(" ")[4]})
                            elif str(temp_var + ' ' + temp_date) in temp_dict_date_leave_one and str(
                                    temp_var + ' ' + temp_date) in temp_dict_date_attend_zero \
                                    and str(temp_var + ' ' + temp_date + ' ' + 'night') in temp_dict_date_attend_zero:
                                temp_dict_date_leave_one.update(
                                    {str(temp_var + ' ' + temp_date + ' ' + 'night'): str(day).split(" ")[4]})
                            elif str(temp_var + ' ' + temp_date) in temp_dict_date_leave_one and str(
                                    temp_var + ' ' + temp_date) in temp_dict_date_attend_zero \
                                    and str(temp_var + ' ' + temp_date + ' ' + 'night') not in temp_dict_date_attend_zero:
                                temp_dict_date_leave_one.update(
                                    {str(temp_var + ' ' + temp_date + ' ' + 'night'): str(day).split(" ")[4]})
                            elif str(temp_var + ' ' + temp_date) not in temp_dict_date_leave_one and str(temp_var + ' ' + temp_date) in temp_dict_date_attend_zero :
                                temp_dict_date_leave_one.update({str(temp_var + ' ' + temp_date): str(day).split(" ")[4]})
                            if str(temp_var + ' ' + temp_date) in temp_dict_date_leave_one and str(
                                    temp_var + ' ' + temp_date) in temp_dict_date_attend_zero \
                                    and str(temp_var + ' ' + temp_date + ' ' + 'night') in temp_dict_date_attend_zero and hour_no_zero >= str(14):
                                temp_dict_date_leave_one.update(
                                    {str(temp_var + ' ' + temp_date + ' ' + 'night'): str(day).split(" ")[4]})
                        if str(day).split(' ')[6] == '0)':
                            if hour_no_zero[0]=='0':
                                hour_no_zero = hour_no_zero[1:]
                            if str(temp_var + ' ' + temp_date) in temp_dict_date_attend_zero and str(temp_var + ' ' + temp_date) not in temp_dict_date_leave_one:
                                # temp_dict_date_leave_one.update({str(temp_var + ' ' + temp_date): ' '})
                                temp_dict_date_leave_one.update({str(temp_var + ' ' + temp_date): str(day).split(" ")[4]})
                            if str(temp_var + ' ' + temp_date) not in list_of_ids_attend:
                                list_of_ids_attend.append(str(temp_var + ' ' + temp_date))
                                list_of_date.append(temp_date)
                                temp_dict_date_attend_zero.update({str(temp_var + ' ' + temp_date): str(day).split(" ")[4]})
                            if str(temp_var + ' ' + temp_date) in list_of_ids_attend and str(temp_var + ' ' + temp_date) in temp_dict_date_attend_zero:
                                list_of_ids_attend.append(str(temp_var + ' ' + temp_date) + ' '  +'night')
                                temp_dict_date_attend_zero.update({str(temp_var + ' ' + temp_date + ' '  +'night'): str(day).split(" ")[4]})
                                list_of_date.append(temp_date)
                            if temp_dict_date_attend_zero.get(str(temp_var + ' ' + temp_date + ' ' + 'night')) == temp_dict_date_attend_zero.get(str(temp_var + ' ' + temp_date )):
                                get_leave_morning = temp_dict_date_attend_zero.get(str(temp_var + ' ' + temp_date + ' ' + 'night'))
                                temp_dict_date_attend_zero.update({str(temp_var + ' ' + temp_date+ ' '  +'night'):get_leave_morning})
                            # if str(temp_var + ' ' + temp_date + ' '  +'night')  in temp_dict_date_attend_zero :
                            #     list_of_ids_attend.append(str(temp_var + ' ' + temp_date) + ' ' + 'night')
                            #     temp_dict_date_attend_zero.update({str(temp_var + ' ' + temp_date + ' ' + 'night'): str(day).split(" ")[4]})
                            #     list_of_date.append(temp_date)
                ##############################    SPECIFIC EMPLOYEE , BRANCH MADINA       ###################################
                elif obj.choose_branch =='b' and obj.choose_option == 'b' and not obj.date_end:
                    if temp_var == str(obj.employee_id_Madina.biometric_id):
                        gDate = datetime.datetime(int(temp_date.split('-')[0]), int(temp_date.split('-')[1]), int(temp_date.split('-')[2]))
                        Today = gDate + timedelta(days=-1)
                        if str(obj.dat) <= temp_date:
                            hour_no_zero = str(day).split(" ")[4].split(':')[0]
                            if hour_no_zero[0] == '0':
                                hour_no_zero = hour_no_zero[1:]
                            if str(day).split(' ')[6] == '1)':
                                if hour_no_zero == str(0)  and hour_no_zero < str(4) and str(temp_var + ' ' + temp_date) not in temp_dict_date_leave_one :
                                    duplicate_leave = temp_dict_date_leave_one.get(str(temp_var + ' ' + temp_date))
                                    temp_dict_date_leave_one.update({str(temp_var + ' ' + str(Today).split(' ')[0] +' '+'night'):str(day).split(" ")[4]})
                                    print(str(Today).split(' ')[0],'date')
                                if str(temp_var + ' ' + temp_date) in temp_dict_date_leave_one and str(temp_var + ' ' + temp_date) in temp_dict_date_attend_zero  \
                                        and str(temp_var + ' ' + temp_date  + ' '  +'night') not in temp_dict_date_leave_one:
                                    temp_dict_date_leave_one.update(
                                        {str(temp_var + ' ' + temp_date  + ' '  +'night'): str(day).split(" ")[4]})
                                    print('dictionary',
                                          temp_dict_date_leave_one.get(str(temp_var + ' ' + temp_date + ' ' + 'night')))
                                elif str(temp_var + ' ' + temp_date) in temp_dict_date_leave_one and str(temp_var + ' ' + temp_date) in temp_dict_date_attend_zero \
                                    and str(temp_var + ' ' + temp_date  + ' '  +'night') in temp_dict_date_leave_one and hour_no_zero <'21':
                                    duplicate_leave = temp_dict_date_leave_one.get(str(temp_var + ' ' + temp_date + ' '  +'night'))
                                    try:
                                        list_of_ids_attend.remove(str(temp_var + ' ' + temp_date + ' '  +'night'))
                                        list_of_date.remove(temp_date)
                                    except:
                                        pass
                                    list_of_ids_attend.append(str(temp_var + ' ' + temp_date  + ' '  +'night'))
                                    list_of_date.append(temp_date)
                                    temp_dict_date_attend_zero.update(
                                        {str(temp_var + ' ' + temp_date  + ' '  +'night'): duplicate_leave})
                                    temp_dict_date_leave_one.update(
                                        {str(temp_var + ' ' + temp_date + ' '  +'night'): str(day).split(" ")[4]})
                                elif str(temp_var + ' ' + temp_date) in temp_dict_date_leave_one and str(
                                        temp_var + ' ' + temp_date) in temp_dict_date_attend_zero \
                                        and str(temp_var + ' ' + temp_date + ' ' + 'night') in temp_dict_date_attend_zero:
                                    temp_dict_date_leave_one.update(
                                        {str(temp_var + ' ' + temp_date + ' ' + 'night'): str(day).split(" ")[4]})
                                elif str(temp_var + ' ' + temp_date) in temp_dict_date_leave_one and str(
                                        temp_var + ' ' + temp_date) in temp_dict_date_attend_zero \
                                        and str(temp_var + ' ' + temp_date + ' ' + 'night') not in temp_dict_date_attend_zero:
                                    temp_dict_date_leave_one.update(
                                        {str(temp_var + ' ' + temp_date + ' ' + 'night'): str(day).split(" ")[4]})
                                elif str(temp_var + ' ' + temp_date) not in temp_dict_date_leave_one and str(temp_var + ' ' + temp_date) in temp_dict_date_attend_zero :
                                    temp_dict_date_leave_one.update({str(temp_var + ' ' + temp_date): str(day).split(" ")[4]})
                                if str(temp_var + ' ' + temp_date) in temp_dict_date_leave_one and str(
                                        temp_var + ' ' + temp_date) in temp_dict_date_attend_zero \
                                        and str(temp_var + ' ' + temp_date + ' ' + 'night') in temp_dict_date_attend_zero and hour_no_zero >= str(14):
                                    temp_dict_date_leave_one.update(
                                        {str(temp_var + ' ' + temp_date + ' ' + 'night'): str(day).split(" ")[4]})
                            if str(day).split(' ')[6] == '0)':
                                if hour_no_zero[0]=='0':
                                    hour_no_zero = hour_no_zero[1:]
                                if str(temp_var + ' ' + temp_date) in temp_dict_date_attend_zero and str(temp_var + ' ' + temp_date) not in temp_dict_date_leave_one:
                                    # temp_dict_date_leave_one.update({str(temp_var + ' ' + temp_date): ' '})
                                    temp_dict_date_leave_one.update({str(temp_var + ' ' + temp_date): str(day).split(" ")[4]})
                                if str(temp_var + ' ' + temp_date  + ' '  +'night') in temp_dict_date_attend_zero:
                                    temp_dict_date_leave_one.update({str(temp_var + ' ' + temp_date + ' '  +'night'): str(day).split(" ")[4]})
                                if str(temp_var + ' ' + temp_date) not in list_of_ids_attend:
                                    list_of_ids_attend.append(str(temp_var + ' ' + temp_date))
                                    list_of_date.append(temp_date)
                                    temp_dict_date_attend_zero.update({str(temp_var + ' ' + temp_date): str(day).split(" ")[4]})
                                if str(temp_var + ' ' + temp_date) in list_of_ids_attend and str(temp_var + ' ' + temp_date) in temp_dict_date_attend_zero:
                                    try:
                                        var = temp_dict_date_attend_zero.pop(str(temp_var + ' ' + temp_date) + ' '  +'night')
                                        # list_of_ids_attend.remove(str(temp_var + ' ' + temp_date) + ' ' + 'night')
                                    except:
                                        pass
                                    list_of_ids_attend.append(str(temp_var + ' ' + temp_date) + ' '  +'night')
                                    temp_dict_date_attend_zero.update({str(temp_var + ' ' + temp_date + ' '  +'night'): str(day).split(" ")[4]})
                                    list_of_date.append(temp_date)
                                if temp_dict_date_attend_zero.get(str(temp_var + ' ' + temp_date + ' ' + 'night')) == temp_dict_date_attend_zero.get(str(temp_var + ' ' + temp_date )):
                                    get_leave_morning = temp_dict_date_attend_zero.get(str(temp_var + ' ' + temp_date + ' ' + 'night'))
                                    temp_dict_date_attend_zero.update({str(temp_var + ' ' + temp_date+ ' '  +'night'):get_leave_morning})
                                # if str(temp_var + ' ' + temp_date + ' '  +'night') in temp_dict_date_attend_zero:
                                #     temp_dict_date_leave_one.update({str(temp_var + ' ' + temp_date + ' ' + 'night'): str(day).split(" ")[4]})
                ######################################################################################################################
                elif obj.choose_branch =='b' and obj.choose_option == 'b' and  obj.date_end:
                    if temp_var == str(obj.employee_id_Madina.biometric_id):
                        gDate = datetime.datetime(int(temp_date.split('-')[0]), int(temp_date.split('-')[1]), int(temp_date.split('-')[2]))
                        Today = gDate + timedelta(days=-1)
                        if temp_date >=str(obj.dat) and temp_date <= str(obj.date_end):
                            hour_no_zero = str(day).split(" ")[4].split(':')[0]
                            if hour_no_zero[0] == '0':
                                hour_no_zero = hour_no_zero[1:]
                            if str(day).split(' ')[6] == '1)':
                                if hour_no_zero == str(0)  and hour_no_zero < str(4) and str(temp_var + ' ' + temp_date) not in temp_dict_date_leave_one :
                                    duplicate_leave = temp_dict_date_leave_one.get(str(temp_var + ' ' + temp_date))
                                    temp_dict_date_leave_one.update({str(temp_var + ' ' + str(Today).split(' ')[0] +' '+'night'):str(day).split(" ")[4]})
                                    print(str(Today).split(' ')[0],'date')
                                if str(temp_var + ' ' + temp_date) in temp_dict_date_leave_one and str(temp_var + ' ' + temp_date) in temp_dict_date_attend_zero  \
                                        and str(temp_var + ' ' + temp_date  + ' '  +'night') not in temp_dict_date_leave_one:
                                    temp_dict_date_leave_one.update(
                                        {str(temp_var + ' ' + temp_date  + ' '  +'night'): str(day).split(" ")[4]})
                                    print('dictionary',
                                          temp_dict_date_leave_one.get(str(temp_var + ' ' + temp_date + ' ' + 'night')))
                                elif str(temp_var + ' ' + temp_date) in temp_dict_date_leave_one and str(temp_var + ' ' + temp_date) in temp_dict_date_attend_zero \
                                    and str(temp_var + ' ' + temp_date  + ' '  +'night') in temp_dict_date_leave_one and hour_no_zero <'21':
                                    duplicate_leave = temp_dict_date_leave_one.get(str(temp_var + ' ' + temp_date + ' '  +'night'))
                                    try:
                                        list_of_ids_attend.remove(str(temp_var + ' ' + temp_date + ' '  +'night'))
                                        list_of_date.remove(temp_date)
                                    except:
                                        pass
                                    list_of_ids_attend.append(str(temp_var + ' ' + temp_date  + ' '  +'night'))
                                    list_of_date.append(temp_date)
                                    temp_dict_date_attend_zero.update(
                                        {str(temp_var + ' ' + temp_date  + ' '  +'night'): duplicate_leave})
                                    temp_dict_date_leave_one.update(
                                        {str(temp_var + ' ' + temp_date + ' '  +'night'): str(day).split(" ")[4]})
                                elif str(temp_var + ' ' + temp_date) in temp_dict_date_leave_one and str(
                                        temp_var + ' ' + temp_date) in temp_dict_date_attend_zero \
                                        and str(temp_var + ' ' + temp_date + ' ' + 'night') in temp_dict_date_attend_zero:
                                    temp_dict_date_leave_one.update(
                                        {str(temp_var + ' ' + temp_date + ' ' + 'night'): str(day).split(" ")[4]})
                                elif str(temp_var + ' ' + temp_date) in temp_dict_date_leave_one and str(
                                        temp_var + ' ' + temp_date) in temp_dict_date_attend_zero \
                                        and str(temp_var + ' ' + temp_date + ' ' + 'night') not in temp_dict_date_attend_zero:
                                    temp_dict_date_leave_one.update(
                                        {str(temp_var + ' ' + temp_date + ' ' + 'night'): str(day).split(" ")[4]})
                                elif str(temp_var + ' ' + temp_date) not in temp_dict_date_leave_one and str(temp_var + ' ' + temp_date) in temp_dict_date_attend_zero :
                                    temp_dict_date_leave_one.update({str(temp_var + ' ' + temp_date): str(day).split(" ")[4]})
                                if str(temp_var + ' ' + temp_date) in temp_dict_date_leave_one and str(
                                        temp_var + ' ' + temp_date) in temp_dict_date_attend_zero \
                                        and str(temp_var + ' ' + temp_date + ' ' + 'night') in temp_dict_date_attend_zero and hour_no_zero >= str(14):
                                    temp_dict_date_leave_one.update(
                                        {str(temp_var + ' ' + temp_date + ' ' + 'night'): str(day).split(" ")[4]})
                            if str(day).split(' ')[6] == '0)':
                                if hour_no_zero[0]=='0':
                                    hour_no_zero = hour_no_zero[1:]
                                if str(temp_var + ' ' + temp_date) in temp_dict_date_attend_zero and str(temp_var + ' ' + temp_date) not in temp_dict_date_leave_one:
                                    # temp_dict_date_leave_one.update({str(temp_var + ' ' + temp_date): ' '})
                                    temp_dict_date_leave_one.update({str(temp_var + ' ' + temp_date): str(day).split(" ")[4]})
                                if str(temp_var + ' ' + temp_date  + ' '  +'night') in temp_dict_date_attend_zero:
                                    temp_dict_date_leave_one.update({str(temp_var + ' ' + temp_date + ' '  +'night'): str(day).split(" ")[4]})
                                if str(temp_var + ' ' + temp_date) not in list_of_ids_attend:
                                    list_of_ids_attend.append(str(temp_var + ' ' + temp_date))
                                    list_of_date.append(temp_date)
                                    temp_dict_date_attend_zero.update({str(temp_var + ' ' + temp_date): str(day).split(" ")[4]})
                                if str(temp_var + ' ' + temp_date) in list_of_ids_attend and str(temp_var + ' ' + temp_date) in temp_dict_date_attend_zero:
                                    try:
                                        var = temp_dict_date_attend_zero.pop(str(temp_var + ' ' + temp_date) + ' '  +'night')
                                        # list_of_ids_attend.remove(str(temp_var + ' ' + temp_date) + ' ' + 'night')
                                    except:
                                        pass
                                    list_of_ids_attend.append(str(temp_var + ' ' + temp_date) + ' '  +'night')
                                    temp_dict_date_attend_zero.update({str(temp_var + ' ' + temp_date + ' '  +'night'): str(day).split(" ")[4]})
                                    list_of_date.append(temp_date)
                                if temp_dict_date_attend_zero.get(str(temp_var + ' ' + temp_date + ' ' + 'night')) == temp_dict_date_attend_zero.get(str(temp_var + ' ' + temp_date )):
                                    get_leave_morning = temp_dict_date_attend_zero.get(str(temp_var + ' ' + temp_date + ' ' + 'night'))
                                    temp_dict_date_attend_zero.update({str(temp_var + ' ' + temp_date+ ' '  +'night'):get_leave_morning})
                ####################### BRANCH SAUDI ARABIA  #####################
                elif obj.choose_branch =='b' and obj.choose_option == 'a' and  obj.date_end:
                    gDate = datetime.datetime(int(temp_date.split('-')[0]), int(temp_date.split('-')[1]), int(temp_date.split('-')[2]))
                    Today = gDate + timedelta(days=-1)
                    if temp_date >= str(obj.dat) and temp_date <= str(obj.date_end):
                        hour_no_zero = str(day).split(" ")[4].split(':')[0]
                        if hour_no_zero[0] == '0':
                            hour_no_zero = hour_no_zero[1:]
                        if str(day).split(' ')[6] == '1)':
                            if hour_no_zero == str(0)  and hour_no_zero < str(4) and str(temp_var + ' ' + temp_date) not in temp_dict_date_leave_one:
                                duplicate_leave = temp_dict_date_leave_one.get(str(temp_var + ' ' + temp_date))
                                print('duplicate',duplicate_leave)
                                print('duplicate',hour_no_zero)
                                print("Given date is: ", gDate, str(day).split(" ")[4])
                                temp_dict_date_leave_one.update({str(temp_var + ' ' + str(Today).split(' ')[0] +' '+'night'):str(day).split(" ")[4]})
                                print(str(Today).split(' ')[0],'date')
                            if str(temp_var + ' ' + temp_date) in temp_dict_date_leave_one and str(temp_var + ' ' + temp_date) in temp_dict_date_attend_zero  \
                                    and str(temp_var + ' ' + temp_date  + ' '  +'night') not in temp_dict_date_leave_one:
                                temp_dict_date_leave_one.update(
                                    {str(temp_var + ' ' + temp_date  + ' '  +'night'): str(day).split(" ")[4]})
                                print('dictionary',
                                      temp_dict_date_leave_one.get(str(temp_var + ' ' + temp_date + ' ' + 'night')))
                            elif str(temp_var + ' ' + temp_date) in temp_dict_date_leave_one and str(temp_var + ' ' + temp_date) in temp_dict_date_attend_zero \
                                and str(temp_var + ' ' + temp_date  + ' '  +'night') in temp_dict_date_leave_one:
                                duplicate_leave = temp_dict_date_leave_one.get(str(temp_var + ' ' + temp_date + ' '  +'night'))
                                try:
                                    list_of_ids_attend.remove(str(temp_var + ' ' + temp_date + ' '  +'night'))
                                    list_of_date.remove(temp_date)
                                except:
                                    pass
                                list_of_ids_attend.append(str(temp_var + ' ' + temp_date  + ' '  +'night'))
                                list_of_date.append(temp_date)
                                temp_dict_date_attend_zero.update(
                                    {str(temp_var + ' ' + temp_date  + ' '  +'night'): duplicate_leave})
                                temp_dict_date_leave_one.update(
                                    {str(temp_var + ' ' + temp_date + ' '  +'night'): str(day).split(" ")[4]})
                            elif str(temp_var + ' ' + temp_date) in temp_dict_date_leave_one and str(
                                    temp_var + ' ' + temp_date) in temp_dict_date_attend_zero \
                                    and str(temp_var + ' ' + temp_date + ' ' + 'night') in temp_dict_date_attend_zero:
                                temp_dict_date_leave_one.update(
                                    {str(temp_var + ' ' + temp_date + ' ' + 'night'): str(day).split(" ")[4]})
                            elif str(temp_var + ' ' + temp_date) not in temp_dict_date_leave_one and str(temp_var + ' ' + temp_date) in temp_dict_date_attend_zero:
                                temp_dict_date_leave_one.update({str(temp_var + ' ' + temp_date): str(day).split(" ")[4]})
                            if str(temp_var + ' ' + temp_date) in temp_dict_date_leave_one and str(
                                    temp_var + ' ' + temp_date) in temp_dict_date_attend_zero \
                                    and str(temp_var + ' ' + temp_date + ' ' + 'night') in temp_dict_date_attend_zero and hour_no_zero >= str(14):
                                temp_dict_date_leave_one.update(
                                    {str(temp_var + ' ' + temp_date + ' ' + 'night'): str(day).split(" ")[4]})
                            # temp_dict_date_leave_one.update({str(temp_var + ' ' + temp_date): str(day).split(" ")[4]})
                        if str(day).split(' ')[6] == '0)':
                            if hour_no_zero[0]=='0':
                                hour_no_zero = hour_no_zero[1:]
                            if str(temp_var + ' ' + temp_date) in temp_dict_date_attend_zero and str(temp_var + ' ' + temp_date) not in temp_dict_date_leave_one:
                                temp_dict_date_leave_one.update({str(temp_var + ' ' + temp_date): ' '})
                            if str(temp_var + ' ' + temp_date) not in list_of_ids_attend:
                                list_of_ids_attend.append(str(temp_var + ' ' + temp_date))
                                list_of_date.append(temp_date)
                                temp_dict_date_attend_zero.update({str(temp_var + ' ' + temp_date): str(day).split(" ")[4]})
                            if str(temp_var + ' ' + temp_date) in list_of_ids_attend and str(temp_var + ' ' + temp_date) in temp_dict_date_attend_zero:
                                list_of_ids_attend.append(str(temp_var + ' ' + temp_date) + ' '  +'night')
                                temp_dict_date_attend_zero.update({str(temp_var + ' ' + temp_date + ' '  +'night'): str(day).split(" ")[4]})
                                list_of_date.append(temp_date)
                            if temp_dict_date_attend_zero.get(str(temp_var + ' ' + temp_date + ' ' + 'night')) == temp_dict_date_attend_zero.get(str(temp_var + ' ' + temp_date )):
                                get_leave_morning = temp_dict_date_attend_zero.get(str(temp_var + ' ' + temp_date + ' ' + 'night'))
                                temp_dict_date_attend_zero.update({str(temp_var + ' ' + temp_date+ ' '  +'night'):get_leave_morning})
                                ########################################################
                elif obj.choose_option == 'c' and not obj.date_end and obj.choose_branch =='a':
                    if str(obj.dat) <= temp_date:
                        if str(day).split(' ')[6] == '1)':
                            if str(temp_var + ' ' + temp_date) in temp_dict_date_leave_one  and str(temp_var + ' ' + temp_date) not in temp_dict_date_attend_zero:
                                duplicate_leave = temp_dict_date_leave_one.get(str(temp_var + ' ' + temp_date))
                                try:
                                    list_of_ids_attend.remove(str(temp_var + ' ' + temp_date))
                                    list_of_date.remove(temp_date)
                                except:
                                    pass
                                list_of_ids_attend.append(str(temp_var + ' ' + temp_date))
                                list_of_date.append(temp_date)
                                temp_dict_date_attend_zero.update(
                                    {str(temp_var + ' ' + temp_date): duplicate_leave})
                                temp_dict_date_leave_one.update(
                                    {str(temp_var + ' ' + temp_date): str(day).split(" ")[4]})

                            else:
                                temp_dict_date_leave_one.update({str(temp_var + ' ' + temp_date): str(day).split(" ")[4]})
                            temp_dict_date_leave_one.update({str(temp_var + ' ' + temp_date): str(day).split(" ")[4]})
                        if str(day).split(' ')[6] == '0)':
                            if str(temp_var + ' ' + temp_date) in temp_dict_date_attend_zero:
                                temp_dict_date_leave_one.update({str(temp_var + ' ' + temp_date): str(day).split(" ")[4]})
                            else:
                                list_of_ids_attend.append(str(temp_var + ' ' + temp_date))
                                list_of_date.append(temp_date)
                                temp_dict_date_attend_zero.update({str(temp_var + ' ' + temp_date): str(day).split(" ")[4]})
                elif obj.choose_option== 'c' and obj.date_end and obj.choose_branch=='a':
                    if temp_date >= str(obj.dat) and temp_date <= str(obj.date_end):
                        if str(day).split(' ')[6] == '1)':
                            if str(temp_var + ' ' + temp_date) in temp_dict_date_leave_one  and str(temp_var + ' ' + temp_date) not in temp_dict_date_attend_zero:
                                duplicate_leave = temp_dict_date_leave_one.get(str(temp_var + ' ' + temp_date))
                                try:
                                    list_of_ids_attend.remove(str(temp_var + ' ' + temp_date))
                                    list_of_date.remove(temp_date)
                                except:
                                    pass
                                list_of_ids_attend.append(str(temp_var + ' ' + temp_date))
                                list_of_date.append(temp_date)
                                temp_dict_date_attend_zero.update(
                                    {str(temp_var + ' ' + temp_date): duplicate_leave})
                                temp_dict_date_leave_one.update(
                                    {str(temp_var + ' ' + temp_date): str(day).split(" ")[4]})

                            else:
                                temp_dict_date_leave_one.update({str(temp_var + ' ' + temp_date): str(day).split(" ")[4]})
                            temp_dict_date_leave_one.update({str(temp_var + ' ' + temp_date): str(day).split(" ")[4]})
                        if str(day).split(' ')[6] == '0)':
                            if str(temp_var + ' ' + temp_date) in temp_dict_date_attend_zero:
                                temp_dict_date_leave_one.update({str(temp_var + ' ' + temp_date): str(day).split(" ")[4]})
                            else:
                                list_of_ids_attend.append(str(temp_var + ' ' + temp_date))
                                list_of_date.append(temp_date)
                                temp_dict_date_attend_zero.update({str(temp_var + ' ' + temp_date): str(day).split(" ")[4]})
                #################################################
                elif obj.choose_option== 'a' and not obj.date_end and obj.choose_branch=='a':
                    if str(obj.dat) <= temp_date:
                        if str(day).split(' ')[6] == '1)' :
                            if str(temp_var + ' ' + temp_date) in (temp_dict_date_leave_one) and str(temp_var + ' ' + temp_date) not in temp_dict_date_attend_zero:
                                duplicate_leave = temp_dict_date_leave_one.get(str(temp_var + ' ' + temp_date))
                                try:
                                    list_of_ids_attend.remove(str(temp_var + ' ' + temp_date))
                                    list_of_date.remove(temp_date)
                                except:
                                    pass
                                list_of_ids_attend.append(str(temp_var + ' ' + temp_date))
                                list_of_date.append(temp_date)
                                temp_dict_date_attend_zero.update(
                                    {str(temp_var + ' ' + temp_date): duplicate_leave})
                                temp_dict_date_leave_one.update(
                                    {str(temp_var + ' ' + temp_date): str(day).split(" ")[4]})
                            else:
                                # temp_dict_date_leave_one.update({str(temp_var + ' ' + temp_date): str(day).split(" ")[4]})
                                # pass
                                temp_dict_date_leave_one.update(
                                    {str(temp_var + ' ' + temp_date): str(day).split(" ")[4]})
                        elif str(day).split(' ')[6] == '0)':

                            if str(temp_var + ' ' + temp_date) in temp_dict_date_attend_zero:
                                temp_dict_date_leave_one.update({str(temp_var + ' ' + temp_date): str(day).split(" ")[4]})
                            else:
                                list_of_ids_attend.append(str(temp_var + ' ' + temp_date))
                                list_of_date.append(temp_date)
                                temp_dict_date_attend_zero.update({str(temp_var + ' ' + temp_date): str(day).split(" ")[4]})
                elif obj.choose_option== 'a' and obj.date_end and obj.choose_branch=='a':
                    if  temp_date >=str(obj.dat) and temp_date <= str(obj.date_end):
                        if str(day).split(' ')[6] == '1)':
                            if str(temp_var + ' ' + temp_date) in temp_dict_date_leave_one:
                                duplicate_leave = temp_dict_date_leave_one.get(str(temp_var + ' ' + temp_date))
                                # print('duplicate ',duplicate_leave)
                                # list_of_date.append(temp_date)
                                # list_of_ids_attend.append(str(temp_var + ' ' + temp_date))
                                try:
                                    list_of_ids_attend.remove(str(temp_var + ' ' + temp_date))
                                    list_of_date.remove(temp_date)
                                except:
                                    pass
                                list_of_ids_attend.append(str(temp_var + ' ' + temp_date))
                                list_of_date.append(temp_date)
                                temp_dict_date_attend_zero.update(
                                    {str(temp_var + ' ' + temp_date): duplicate_leave})
                                temp_dict_date_leave_one.update(
                                    {str(temp_var + ' ' + temp_date): str(day).split(" ")[4]})
                            else:
                                temp_dict_date_leave_one.update({str(temp_var + ' ' + temp_date): str(day).split(" ")[4]})
                            # temp_dict_date_leave_one.update({str(temp_var + ' ' + temp_date): str(day).split(" ")[4]})
                        if str(day).split(' ')[6] == '0)':
                            if str(temp_var + ' ' + temp_date) in temp_dict_date_attend_zero:
                                temp_dict_date_leave_one.update({str(temp_var + ' ' + temp_date): str(day).split(" ")[4]})
                            else:
                                list_of_ids_attend.append(str(temp_var + ' ' + temp_date))
                                list_of_date.append(temp_date)
                                temp_dict_date_attend_zero.update({str(temp_var + ' ' + temp_date): str(day).split(" ")[4]})
            print('list', list_of_ids_attend)
            print(temp_dict_date_leave_one)
            print(temp_dict_date_attend_zero)
            for i in range(len(list_of_ids_attend)):
                temp_group =''
                if 'd' in list_of_ids_attend[i]:
                    temp_id_duplicates = list_of_ids_attend[i].split(' ')[0]
                    print(temp_id_duplicates,'id dulpicates')
                # print(list_of_ids_attend[i])
                temp_id = list_of_ids_attend[i].split(' ')[0]
                temp_time_dif_attend = temp_dict_date_attend.get(list_of_ids_attend[i])
                temp_time_dif_leave  = temp_dict_date_leave.get(list_of_ids_attend[i])
                if obj.choose_branch == 'a':
                    self._cr.execute('''
                                   SELECT group_name FROM hr_employee where biometric_id = %s
                                        ''', [temp_id])
                    res_group = self._cr.fetchall()
                if obj.choose_branch == 'b':
                    self._cr.execute('''
                                                       SELECT choose_branch  , choose_shift FROM hr_employee where biometric_id = %s
                                                            ''', [temp_id])
                    res_branch = self._cr.fetchall()
                    try:
                        branch = str(res_branch[0][0])
                        shift = str(res_branch[0][1])

                    except:
                        pass
                    #diff = divmod(c.days * seconds_in_day + c.seconds, 60)
                # print(res_branch,'branch',temp_id)
                try:
                    if res_group[0][0] == 'd':
                        sheet.write(11, 4, temp_dict.get(temp_id))
                        sheet.write(11, 5, temp_dict_date_attend.get(list_of_ids_attend[i]))
                        sheet.write(11, 6, temp_dict_date_leave.get(list_of_ids_attend[i]))
                        sheet.write(11, 7, list_of_date[i])
                except:
                    pass
                try:
                    #and not obj.employee_id
                    if res_group[0][0] == 'a' and  obj.choose_option == 'b' and obj.choose_branch=='a':
                        sheet.write(row_group_A, 0, temp_dict_date_attend_zero.get(list_of_ids_attend[i]))
                        sheet.write(row_group_A, 1, temp_dict_date_leave_one.get(list_of_ids_attend[i]))
                        sheet.write(row_group_A, 2, list_of_date[i])
                        sheet.merge_range(0, 0, 0, 1, 'Group A', format_center)
                        if counter_group_A ==0:
                            sheet.merge_range(0, 0, 0, 1, 'Group A', format_center)
                            sheet.write(1, 1, temp_dict.get(temp_id), bold)
                            counter_group_A +=1
                           # sheet.write(row_group_A, 0, temp_dict.get(temp_id))
                        print('date = ',list_of_date[i])
                        check_late = temp_dict_date_attend_zero.get(list_of_ids_attend[i])
                        if (int(str(check_late).split(':')[1]) >=15 and int(str(check_late).split(':')[0]) >=9):
                            time_diff_late_group_A = int(str(check_late).split(':')[0]) - 9
                            sheet.write(row_group_A, 3, 'Late: '+str(time_diff_late_group_A)+'H '+str(check_late).split(':')[1]+'M',format_late)
                        temp_dict_date_attend_zero[list_of_ids_attend[i]] = ''
                        temp_dict_date_leave_one[list_of_ids_attend[i]] = ''
                        row_group_A += 1
                except:
                    pass
                try:
                    # and not obj.employee_id
                    if res_group[0][0] == 'b' and  obj.choose_option == 'b' and obj.date_end and obj.choose_branch=='a':
                        print(temp_dict.get(temp_id), " names ")
                        if counter_group_B == 0:
                            sheet.merge_range(0, 0, 0, 1, 'Group B', format_center)
                            sheet.write(1,1 ,temp_dict.get(temp_id) , bold)
                            counter_group_B += 1
                        sheet.write(row_group_B, 1, temp_dict_date_attend_zero.get(list_of_ids_attend[i]))
                        sheet.write(row_group_B, 2, temp_dict_date_leave_one.get(list_of_ids_attend[i]))
                        sheet.write(row_group_B, 0, list_of_date[i])
                        check_late_group_B = temp_dict_date_attend_zero.get(list_of_ids_attend[i])
                        # print('value of check_late_group_B', check_late_group_B)
                        if (int(str(check_late_group_B).split(':')[1]) >=15 and int(str(check_late_group_B).split(':')[0])>=10):
                            print('late')
                            time_diff_late_group_B = int(str(check_late_group_B).split(':')[0]) - 10
                            sheet.write(row_group_B, 3, 'Late: '+str(time_diff_late_group_B)+'H '+str(check_late_group_B).split(':')[1]+'M',format_late)
                        row_group_B +=1
                        temp_dict_date_attend_zero[list_of_ids_attend[i]] = ''
                        temp_dict_date_leave_one[list_of_ids_attend[i]] = ''
                    elif res_group[0][0] == 'b' and obj.choose_option == 'b' and obj.employee_id and not obj.date_end and obj.choose_branch=='a':
                        string_biometric = str(obj.employee_id.biometric_id)
                        print(temp_dict.get(temp_id), " names ")
                        if counter_group_B == 0:
                            sheet.merge_range(0, 0, 0, 1, 'Group B', format_center)
                            sheet.write(1, 1, temp_dict.get(string_biometric), bold)
                            counter_group_B += 1
                        sheet.write(row_group_B, 1, temp_dict_date_attend_zero.get(string_biometric +' '+list_of_date[i]))
                        sheet.write(row_group_B, 2, temp_dict_date_leave_one.get(string_biometric +' '+list_of_date[i]))
                        sheet.write(row_group_B, 0, list_of_date[i])
                        check_late_group_B = temp_dict_date_attend_zero.get(list_of_ids_attend[i])
                        # print('value of check_late_group_B', check_late_group_B)
                        if (int(str(check_late_group_B).split(':')[1]) >= 15 and int(
                                str(check_late_group_B).split(':')[0]) >= 10):
                            print('late')
                            time_diff_late_group_B = int(str(check_late_group_B).split(':')[0]) - 10
                            # if list_of_ids_attend[i].split(' ')[0] =='188':
                            #     pass
                            # else:
                            sheet.write(row_group_B, 3, 'Late: ' + str(time_diff_late_group_B) + 'H ' +str(check_late_group_B).split(':')[1] + 'M', format_late)
                        row_group_B += 1
                        temp_dict_date_attend_zero[string_biometric] = ''
                        temp_dict_date_leave_one[string_biometric] = ''
                    ##########################  SAUDI ARABIA   ######################
                    elif obj.choose_branch =='b' and obj.choose_option=='a':
                        if date_group_B ==1:
                            sheet.write(2, 0, 'Date',format_date)
                            sheet.write(2, 1, list_of_date[0],format_date)
                            sheet.write(2, 4, 'Date', format_date)
                            sheet.write(2, 5, list_of_date[0], format_date)
                        if 'night' in list_of_ids_attend[i]:
                            if int(temp_dict_date_attend_zero.get(list_of_ids_attend[i]).split(':')[0]) <=12 :
                                pass
                            else:
                                sheet.write(row_Saudi_night, 4, temp_dict_date_attend_zero.get(list_of_ids_attend[i]))
                            if int(temp_dict_date_leave_one.get(list_of_ids_attend[i]).split(':')[0]) <= 18 and int(temp_dict_date_leave_one.get(list_of_ids_attend[i]).split(':')[0]) >=17:
                                pass
                            else:
                                sheet.write(row_Saudi_night, 5, temp_dict_date_leave_one.get(list_of_ids_attend[i]))
                            if temp_dict_date_leave_one.get(list_of_ids_attend[i]) !='' and temp_dict_date_attend_zero.get(list_of_ids_attend[i])!='':
                                sheet.write(row_Saudi_night, 6, temp_dict.get(temp_id))
                            if temp_dict_date_attend_zero.get(list_of_ids_attend[i]) !='':
                                row_Saudi_night +=1
                        if 'night' not in list_of_ids_attend[i]:
                            if int(temp_dict_date_attend_zero.get(list_of_ids_attend[i]).split(':')[0]) > 12 :
                                pass
                            else:
                                sheet.write(row_Saudi_Mor, 0, temp_dict_date_attend_zero.get(list_of_ids_attend[i]))
                                if int(temp_dict_date_leave_one.get(list_of_ids_attend[i]).split(':')[0]) >= 16 :
                                    pass
                                else:
                                    sheet.write(row_Saudi_Mor, 1, temp_dict_date_leave_one.get(list_of_ids_attend[i]))
                                sheet.write(row_Saudi_Mor, 2, temp_dict.get(temp_id))
                                row_Saudi_Mor += 1
                        if counter_group_B == 0:
                            sheet.merge_range(0, 0, 0, 1, 'Morning shift', format_center)
                            sheet.write(1, 1, 'Leave', bold)
                            sheet.write(1, 0, 'Attend', bold)
                            sheet.write(1, 2, 'Name', bold)
                            counter_group_B += 1
                        date_group_B +=1
                        temp_dict_date_attend_zero[list_of_ids_attend[i]] = ''
                        temp_dict_date_leave_one[list_of_ids_attend[i]] = ''
                        ##########################  SAUDI ARABIA  SPECIFIC EMPLOYEE ######################
                    elif obj.choose_branch == 'b' and obj.choose_option == 'b' and obj.employee_id_Madina:
                        if date_group_B == 1:
                            sheet.write(2, 0, 'Date', format_date)
                            sheet.write(2, 1, list_of_date[0], format_date)
                            sheet.write(2, 4, 'Date', format_date)
                            sheet.write(2, 5, list_of_date[0], format_date)
                        if 'night' in list_of_ids_attend[i]:
                            if int(temp_dict_date_attend_zero.get(list_of_ids_attend[i]).split(':')[0]) <= 12 :
                                pass
                            else:
                                sheet.write(row_Saudi_night, 4, temp_dict_date_attend_zero.get(list_of_ids_attend[i]))
                            if int(temp_dict_date_leave_one.get(list_of_ids_attend[i]).split(':')[0]) <= 18 and int(temp_dict_date_leave_one.get(list_of_ids_attend[i]).split(':')[0]) >=17:
                                pass
                            else:
                                sheet.write(row_Saudi_night, 5, temp_dict_date_leave_one.get(list_of_ids_attend[i]))
                            if temp_dict_date_leave_one.get(
                                    list_of_ids_attend[i]) != '' and temp_dict_date_attend_zero.get(
                                    list_of_ids_attend[i]) != '':
                                sheet.write(row_Saudi_night, 6, temp_dict.get(temp_id))
                            if temp_dict_date_attend_zero.get(list_of_ids_attend[i]) != '':
                                row_Saudi_night += 1
                        if 'night' not in list_of_ids_attend[i]:
                            if int(temp_dict_date_attend_zero.get(list_of_ids_attend[i]).split(':')[0]) > 12:
                                pass
                            else:
                                sheet.write(row_Saudi_Mor, 0, temp_dict_date_attend_zero.get(list_of_ids_attend[i]))
                                if int(temp_dict_date_leave_one.get(list_of_ids_attend[i]).split(':')[0]) >= 16:
                                    pass
                                else:
                                    sheet.write(row_Saudi_Mor, 1, temp_dict_date_leave_one.get(list_of_ids_attend[i]))
                                sheet.write(row_Saudi_Mor, 2, temp_dict.get(temp_id))
                                row_Saudi_Mor += 1
                        if counter_group_B == 0:
                            sheet.merge_range(0, 0, 0, 1, 'Morning shift', format_center)
                            sheet.write(1, 1, 'Leave', bold)
                            sheet.write(1, 0, 'Attend', bold)
                            sheet.write(1, 2, 'Name', bold)
                            counter_group_B += 1
                        date_group_B += 1
                        temp_dict_date_attend_zero[list_of_ids_attend[i]] = ''
                        temp_dict_date_leave_one[list_of_ids_attend[i]] = ''
                        #################################################################
                    elif res_group[0][0] == 'b' and obj.choose_option == 'a' and obj.choose_branch=='a':
                        temp_group = 'b'
                        if date_group_B ==1:
                            sheet.write(2, 4, 'Date',format_date)
                            sheet.write(2, 7, 'Date', format_date)
                            sheet.write(2, 5, list_of_date[0],format_date)
                        sheet.write(row_group_B, 5, temp_dict_date_attend_zero.get(list_of_ids_attend[i]))
                        sheet.write(row_group_B, 6, temp_dict_date_leave_one.get(list_of_ids_attend[i]))
                        sheet.write(row_group_B, 4, temp_dict.get(temp_id))
                        if counter_group_B == 0:
                            sheet.merge_range(0, 4, 0, 5, 'Group B', format_center)
                            sheet.write(1, 6, 'Leave', bold)
                            sheet.write(1, 5, 'Attend', bold)
                            sheet.write(1, 4, 'Name', bold)
                            counter_group_B += 1
                        check_late_group_B = temp_dict_date_attend_zero.get(list_of_ids_attend[i])
                        # print('value of check_late_group_B', check_late_group_B)
                        if (int(str(check_late_group_B).split(':')[1]) >=15 and int(str(check_late_group_B).split(':')[0])>=10):
                            # print('late')
                            time_diff_late_group_B = int(str(check_late_group_B).split(':')[0]) - 10
                            sheet.write(row_group_B, 7, 'Late: '+str(time_diff_late_group_B)+'H '+str(check_late_group_B).split(':')[1]+'M',format_late)
                        row_group_B +=1
                        date_group_B +=1
                        temp_dict_date_attend_zero[list_of_ids_attend[i]] = ''
                        temp_dict_date_leave_one[list_of_ids_attend[i]] = ''
                    elif res_group[0][0] == 'a' and obj.choose_option == 'a' and obj.choose_branch=='a':
                        if date_group_A ==1:
                            sheet.write(2, 0, 'Date',format_date)
                            sheet.write(2, 1, list_of_date[0],format_date)
                        sheet.write(row_group_A, 1, temp_dict_date_attend_zero.get(list_of_ids_attend[i]))
                        sheet.write(row_group_A, 2, temp_dict_date_leave_one.get(list_of_ids_attend[i]))
                        sheet.write(row_group_A, 0, temp_dict.get(temp_id))
                        row_group_A += 1
                        # print('info group a',list_of_date[i],temp_dict_date_attend_zero.get(list_of_ids_attend[i]),temp_dict_date_leave_one.get(list_of_ids_attend[i]),temp_dict.get(temp_id))
                        if counter_group_A == 0:
                            sheet.merge_range(0, 4, 0, 5, 'Group B', format_center)
                            sheet.write(1, 2, 'Leave', bold)
                            sheet.write(1, 1, 'Attend', bold)
                            sheet.write(1, 0, 'Name', bold)
                            counter_group_A += 1
                        check_late_group_A = temp_dict_date_attend_zero.get(list_of_ids_attend[i])
                        print('value of check_late_group_B', check_late_group_A)
                        if (int(str(check_late_group_A).split(':')[1]) >=15 and int(str(check_late_group_A).split(':')[0])>=10):
                            print('late')
                            time_diff_late_group_A = int(str(check_late_group_B).split(':')[0]) - 10
                            sheet.write(row_group_A, 7, 'Late: '+str(time_diff_late_group_A)+'H '+str(check_late_group_A).split(':')[1]+'M',format_late)
                        date_group_A +=1
                        temp_dict_date_attend_zero[list_of_ids_attend[i]] = ''
                        temp_dict_date_leave_one[list_of_ids_attend[i]] = ''
                    elif res_group[0][0] == 'c' and obj.choose_option == 'a' and obj.choose_branch=='a':
                        if date_group_C ==1:
                            sheet.write(2, 8, 'Date',format_date)
                            sheet.write(2, 9, list_of_date[0],format_date)
                        sheet.write(row_group_C, 8, temp_dict.get(temp_id))
                        sheet.write(row_group_C, 9, temp_dict_date_attend_zero.get(list_of_ids_attend[i]))
                        sheet.write(row_group_C, 10, temp_dict_date_leave_one.get(list_of_ids_attend[i]))
                        if counter_group_C == 0:
                            sheet.merge_range(0, 8, 0, 9, 'Group C', format_center)
                            sheet.write(1, 10, 'Leave', bold)
                            sheet.write(1, 9, 'Attend', bold)
                            sheet.write(1, 8, 'Name', bold)
                        counter_group_C += 1
                        check_late_group_C = temp_dict_date_attend_zero.get(list_of_ids_attend[i])
                        if (int(str(check_late_group_C).split(':')[1]) >=15 and int(str(check_late_group_C).split(':')[0])>=10):
                            time_diff_late_group_C = int(str(check_late_group_C).split(':')[0]) - 10
                            print('late group c',time_diff_late_group_C)
                            print('minutes ',check_late_group_C)
                            # sheet.write(row_group_C, 12, 'Late: ')
                            sheet.write(row_group_C, 11, 'Late: '+str(time_diff_late_group_C)+'H '+str(check_late_group_C).split(':')[1]+'M',format_late)
                           # sheet.write(row_group_C, 12, 'Late: ')

                        date_group_C +=1
                        temp_dict_date_attend_zero[list_of_ids_attend[i]] = ''
                        temp_dict_date_leave_one[list_of_ids_attend[i]] = ''
                        row_group_C += 1
                    ##############################

                    ############################
                       # Based on group
                    # +-
                    ###################

                    if res_group[0][0] == obj.choose_group and obj.choose_option == 'c' and obj.choose_group and obj.choose_branch=='a':
                        empty_list_all_groups.append(list_of_date[i])
                        if date_all_groups ==1:
                            sheet.write(2, 0, 'Date',format_date)
                            sheet.write(2, 1, list_of_date[i],format_date)
                            sheet.write(0, 0, 'Group name ' + obj.choose_group,format_date)
                            sheet.write(1,1 , 'Attend', bold)
                            sheet.write(1,2 , 'Leave', bold)
                            sheet.write(1, 0, 'Name', bold)
                        sheet.write(row_all_groups, 2, temp_dict.get(temp_id))
                        sheet.write(row_all_groups, 0, temp_dict_date_attend_zero.get(list_of_ids_attend[i]))
                        sheet.write(row_all_groups, 1, temp_dict_date_leave_one.get(list_of_ids_attend[i]))
                        check_late_group_C = temp_dict_date_attend_zero.get(list_of_ids_attend[i])
                        print('value of check_late_group_C', check_late_group_C)
                        if res_group[0][0] =='a':
                            late_time = 9
                        elif res_group[0][0] =='b':
                            late_time = 10
                        elif res_group[0][0] =='c':
                            late_time = 12
                        if (int(str(check_late_group_C).split(':')[1]) >=15 and int(str(check_late_group_C).split(':')[0])>=late_time):
                            # print('late group c' )
                            time_diff_late_group_C = int(str(check_late_group_C).split(':')[0]) - late_time
                            # print('late group c',time_diff_late_group_C)
                            # print('minutes ',check_late_group_C)
                            sheet.write(row_all_groups, 3, 'Late: '+str(time_diff_late_group_C)+'H '+str(check_late_group_C).split(':')[1]+'M',format_late)
                        date_all_groups +=1
                        temp_dict_date_attend_zero[list_of_ids_attend[i]] = ''
                        temp_dict_date_leave_one[list_of_ids_attend[i]] = ''
                        row_all_groups += 1
                        counter_all_groups +=1
                        if i >= 1:
                            if empty_list_all_groups[counter_all_groups] != empty_list_all_groups[counter_all_groups - 1]:
                                sheet.write(row_all_groups, 0, 'Date', format_date)
                                sheet.write(row_all_groups, 1, empty_list_all_groups[counter_all_groups], format_date)
                                row_all_groups += 1
                                pass
                    try:
                        if obj.choose_option == 'a' and obj.choose_branch=='a':
                            if list_of_date[i] != list_of_date[i + 1]:
                                sheet.write(row_group_A, 0, 'Date', format_date)
                                sheet.write(row_group_A, 1, list_of_date[i + 1], format_date)
                                # print(list_of_date[i + 1])
                                # print(list_of_date[i], 'current')
                                row_group_A += 1
                                sheet.write(row_group_B, 4, 'Date', format_date)
                                sheet.write(row_group_B, 5, list_of_date[i + 1], format_date)
                                row_group_B += 1
                                sheet.write(row_group_C, 8, 'Date', format_date)
                                sheet.write(row_group_C, 9, list_of_date[i + 1], format_date)
                                row_group_C += 1

                        if i >= 1 and obj.choose_option == 'c' and obj.choose_branch=='a':
                            if list_of_date[i] != list_of_date[i + 1]:
                                # row_all_groups += 1
                                sheet.write(row_all_groups, 0, 'Date', format_date)
                                sheet.write(row_all_groups, 1, list_of_date[i+1], format_date)
                                # print('next date', list_of_date[i])
                                row_all_groups += 1
                        if   obj.choose_branch=='b':
                            if list_of_date[i] != list_of_date[i + 1]:
                                sheet.write(row_Saudi_Mor, 0, 'Date', format_date)
                                sheet.write(row_Saudi_Mor, 1, list_of_date[i + 1], format_date)
                                row_Saudi_Mor += 1
                                sheet.write(row_Saudi_night, 4, 'Date', format_date)
                                sheet.write(row_Saudi_night, 5, list_of_date[i + 1], format_date)
                                row_Saudi_night += 1
                    except:
                        pass
                except Exception as e:
                    print ("Process terminate : {}".format(e))
                    print('exception')
                    try:
                        if obj.choose_option == 'a' and obj.choose_branch=='a':
                            if list_of_date[i] != list_of_date[i + 1]:
                                sheet.write(row_group_A, 0, 'Date', format_date)
                                sheet.write(row_group_A, 1, list_of_date[i + 1], format_date)
                                print(list_of_date[i + 1])
                                print(list_of_date[i], 'current')
                                row_group_A += 1
                                sheet.write(row_group_B, 4, 'Date', format_date)
                                sheet.write(row_group_B, 5, list_of_date[i + 1], format_date)
                                row_group_B += 1
                                sheet.write(row_group_C, 8, 'Date', format_date)
                                sheet.write(row_group_C, 9, list_of_date[i + 1], format_date)
                                row_group_C += 1

                        if i >= 1 and obj.choose_option == 'c' and obj.choose_branch=='a':
                            if list_of_date[i] != list_of_date[i + 1]:
                                # row_all_groups += 1
                                sheet.write(row_all_groups, 0, 'Date', format_date)
                                sheet.write(row_all_groups, 1, list_of_date[i+1], format_date)
                                print('next date', list_of_date[i])
                                row_all_groups += 1
                        if   obj.choose_branch=='b':
                            if list_of_date[i] != list_of_date[i + 1]:
                                sheet.write(row_Saudi_Mor, 0, 'Date', format_date)
                                sheet.write(row_Saudi_Mor, 1, list_of_date[i + 1], format_date)
                                sheet.write(row_Saudi_night, 4, 'Date', format_date)
                                sheet.write(row_Saudi_night, 5, list_of_date[i + 1], format_date)
                                row_Saudi_Mor += 1
                                row_Saudi_night += 1
                    except:
                        # print('exception',list_of_ids_attend[i])
                        pass
            # print('lengt of pandas ',list_of_date_pandas)
            print('lengt of pandas ',temp_dict_date_leave_one_pandas_morning)
            print('lengt of pandas ',temp_dict_date_attend_zero_pandas_morning)
            for i in range(len(list_of_ids_attend_pandas)):
                temp_id = list_of_ids_attend_pandas[i].split(' ')[0]
                temp_time_dif_attend = temp_dict_date_attend_zero_pandas.get(list_of_ids_attend_pandas[i])
                temp_time_dif_leave = temp_dict_date_leave_one_pandas.get(list_of_ids_attend_pandas[i])
                temp_time_dif_attend_morning = temp_dict_date_attend_zero_pandas_morning.get(list_of_ids_attend_pandas[i])
                temp_time_dif_leave_morning = temp_dict_date_leave_one_pandas_morning.get(list_of_ids_attend_pandas[i])
                list_of_ids_attend_pandas.append(str(temp_var + ' ' + temp_date))
                a = datetime.datetime(int(list_of_date_pandas[i].split("-")[0]),
                                      int(list_of_date_pandas[i].split("-")[1]),
                                      int(list_of_ids_attend_pandas[i].split(' ')[1].split('-')[2])
                                      , int(temp_time_dif_attend.split(":")[0]),
                                      int(temp_time_dif_attend.split(":")[1]), int(temp_time_dif_attend.split(":")[2]))
                try:
                    time_diff_madina_morning = datetime.datetime(int(list_of_date_pandas[i].split("-")[0]),
                                              int(list_of_date_pandas[i].split("-")[1]),
                                              int(list_of_ids_attend_pandas[i].split(' ')[1].split('-')[2])
                                              , int(temp_time_dif_attend_morning.split(":")[0]),
                                              int(temp_time_dif_attend_morning.split(":")[1]), int(temp_time_dif_attend_morning.split(":")[2]))
                except:
                    pass
                try:
                    b = datetime.datetime(int(list_of_date_pandas[i].split("-")[0]), int(list_of_date_pandas[i].split("-")[1]),
                                         int(list_of_ids_attend_pandas[i].split(' ')[1].split('-')[2]),
                                          int(temp_time_dif_leave.split(":")[0]),
                                          int(temp_time_dif_leave.split(":")[1]),
                                          int(temp_time_dif_leave.split(":")[2]))

                    c = b - a
                    new = str(c).split(":")[0] + ':' + str(c).split(":")[1] + ':' + '00'
                except:
                    new = str('00:00:00')
                    pass
                try:
                    time_diff_madina_night = datetime.datetime(int(list_of_date_pandas[i].split("-")[0]),
                                                               int(list_of_date_pandas[i].split("-")[1]),
                                                               int(list_of_ids_attend_pandas[i].split(' ')[1].split(
                                                                   '-')[2]),
                                                               int(temp_time_dif_leave_morning.split(":")[0]),
                                                               int(temp_time_dif_leave_morning.split(":")[1]),
                                                               int(temp_time_dif_leave_morning.split(":")[2]))
                    differnce_time = time_diff_madina_night - time_diff_madina_morning
                    differnce_time_string = str(differnce_time).split(":")[0] + ':' + str(differnce_time).split(":")[1] + ':' + '00'
                except:
                    differnce_time_string = str('00:00:00')
                if 'day' in differnce_time_string or 'days' in differnce_time_string:
                    differnce_time_string = differnce_time_string.split(' ')[2]
                var = list_of_ids_attend_pandas[i].split(" ")[1].split('-')[:2]
                var = str(var[1])
                list_of_date_all_data.append(list_of_ids_attend_pandas[i].split(" ")[1].split('-')[2])
                list_of_hours_df.append(new)
                list_of_hours_df_madina.append(differnce_time_string)
                list_of_ids_df.append(temp_id)
            dict_of_data = {'id': list_of_ids_df,
                                'date': list_of_date_pandas,
                                'Worked_Hours': list_of_hours_df,
                                'Worked_Hours_morning': list_of_hours_df_madina,
                                'Month_year': list_of_pandas_month_day,
                                 'day': list_of_date_all_data
                                 }
            df = pd.DataFrame(dict_of_data)
            df['Worked_Hours'] = pd.to_timedelta(df.Worked_Hours)
            df['Worked_Hours_morning'] = pd.to_timedelta(df.Worked_Hours_morning)
            print(date_worked_hours , 'last date')
            if obj.choose_option=='b' and obj.choose_branch=='a':
                if not obj.date_end:
                    val = df.loc[(df['id'] == str(obj.employee_id.biometric_id)) & (df['Month_year'] >= str(obj.dat)) & (df['Month_year'] <= date_worked_hours) , 'Worked_Hours'].sum()
                elif obj.date_end:
                    val = df.loc[(df['id'] == str(obj.employee_id.biometric_id)) & (df['Month_year'] >= str(obj.dat)) & (df['Month_year'] <= str(obj.date_end)), 'Worked_Hours'].sum()
                Hours = int(str(val).split(' ')[2].split(':')[0])
                mins = int(str(val).split(' ')[2].split(':')[1])
                total = datetime.timedelta(days=int(str(val).split(' ')[0]), hours=Hours, minutes=mins)
                total_minutes = int(total.total_seconds() // 60)
                hours, minutes = total_minutes // 60, total_minutes % 60
                print(hours, minutes)
                print(str(hours)+'.'+str(minutes))
                print(df['date'])
                print(df['id'])
                print(df['Worked_Hours'])
                print(temp_dict_date_attend_zero)
                print(temp_dict_date_leave_one)
                if not obj.date_end:
                    query_date_end = date_worked_hours
                elif obj.date_end:
                    query_date_end = str(obj.date_end)
                self._cr.execute('''
                                            SELECT user_id,hr_attendance.worked_hours ,year_month_day_attend ,year_month_attend FROM  hr_attendance
                                            INNER JOIN  hr_employee
                                            on hr_employee.biometric_id = %s  
                                            and hr_attendance.create_uid = hr_employee.user_id 
                                            and hr_attendance.year_month_day_attend >= %s 
                                            and hr_attendance.year_month_day_attend <= %s                          
                                                ''', [obj.employee_id.biometric_id, str(obj.dat), query_date_end])
                user_id_worked_hours = self._cr.fetchall()

                print(user_id_worked_hours)
                for i in range(len(user_id_worked_hours)):
                    sum_worked_hours += user_id_worked_hours[i][1]
                print(sum_worked_hours +float(str(hours)+'.'+str(minutes)))
                hours_minutes = sum_worked_hours + float(str(hours) + '.' + str(minutes))
                ## Minutes
                string_minutes = str(hours_minutes).split('.')[1][0:2]
                ## Hours
                string_hours = str(hours_minutes).split('.')[0]
                sheet.write(1, 2, 'Worked hours', format_date)
                sheet.write(1, 3, string_hours+' '+'H'+' '+string_minutes+' '+'M', format_date)
                print(df)
            ####################################################################################
            elif obj.choose_option=='b' and obj.choose_branch=='b':
                if not obj.date_end:
                    val = df.loc[(df['id'] == str(obj.employee_id_Madina.biometric_id)) & (df['Month_year'] >= str(obj.dat)) & (df['Month_year'] <= date_worked_hours) , 'Worked_Hours'].sum()
                    val_madina = df.loc[(df['id'] == str(obj.employee_id_Madina.biometric_id)) & (df['Month_year'] >= str(obj.dat)) & (df['Month_year'] <= date_worked_hours) , 'Worked_Hours_morning'].sum()
                elif obj.date_end:
                    val_madina = df.loc[
                        (df['id'] == str(obj.employee_id_Madina.biometric_id)) & (df['Month_year'] >= str(obj.dat)) & (df['Month_year'] <= date_worked_hours), 'Worked_Hours_morning'].sum()
                    val = df.loc[(df['id'] == str(obj.employee_id_Madina.biometric_id)) & (df['Month_year'] >= str(obj.dat)) & (df['Month_year'] <= str(obj.date_end)), 'Worked_Hours'].sum()
                Hours = int(str(val).split(' ')[2].split(':')[0])
                mins = int(str(val).split(' ')[2].split(':')[1])
                Hours_madina = int(str(val_madina).split(' ')[2].split(':')[0])
                mins_madina = int(str(val_madina).split(' ')[2].split(':')[1])
                total = datetime.timedelta(days=int(str(val).split(' ')[0]), hours=Hours, minutes=mins)
                total_madina = datetime.timedelta(days=int(str(val_madina).split(' ')[0]), hours=Hours_madina, minutes=mins_madina)
                total_minutes = int(total.total_seconds() // 60)
                total_minutes_madina = int(total_madina.total_seconds() // 60)
                hours, minutes = total_minutes // 60, total_minutes % 60
                hours_madina, minutes_madina = total_minutes_madina // 60, total_minutes_madina % 60
                if not obj.date_end:
                    query_date_end = date_worked_hours
                elif obj.date_end:
                    query_date_end = str(obj.date_end)
                print(list_of_hours_df)
                print(len(list_of_hours_df))
                print(len(list_of_ids_attend_pandas))
                print(len(list_of_date_pandas))
                self._cr.execute('''
                                            SELECT user_id,hr_attendance.worked_hours ,year_month_day_attend ,year_month_attend FROM  hr_attendance
                                            INNER JOIN  hr_employee
                                            on hr_employee.biometric_id = %s  
                                            and hr_attendance.create_uid = hr_employee.user_id 
                                            and hr_attendance.year_month_day_attend >= %s 
                                            and hr_attendance.year_month_day_attend <= %s         
                                                ''', [obj.employee_id.biometric_id, str(obj.dat), query_date_end])
                user_id_worked_hours = self._cr.fetchall()
                print(user_id_worked_hours)
                for i in range(len(user_id_worked_hours)):
                    sum_worked_hours += user_id_worked_hours[i][1]
                print(sum_worked_hours +float(str(hours)+'.'+str(minutes)))
                hours_minutes = sum_worked_hours + float(str(hours) + '.' + str(minutes)) + + float(str(hours_madina) + '.' + str(minutes_madina))
                ## Minutes
                string_minutes = str(hours_minutes).split('.')[1][0:2]
                ## Hours
                string_hours = str(hours_minutes).split('.')[0]
                sheet.write(1, 2, 'Worked hours', format_date)
                sheet.write(1, 3, string_hours+' '+'H'+' '+string_minutes+' '+'M', format_date)
                print(df)
                print(val_madina)
                print(val)
                print(list_of_hours_df)
                print(list_of_hours_df_madina)



