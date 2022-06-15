from django.shortcuts import render
import pandas as pd
import csv
from alltasks.models import TakeExam, User
import collections
from django.db.models import Sum

# global variables
phone_col = 8
first_name_col = 2
last_name_col = 5
rate_col = 1


# read the csv file and check if a new user submit a response add that user to database"
def addusers(file):
    for i in range(0, file.shape[0]):
        if not User.objects.filter(phone=file.iloc[i, phone_col]).exists():
            new_user = User(first_name=file.iloc[i, first_name_col], last_name=file.iloc[i, last_name_col],
                            phone=file.iloc[i, phone_col])
            new_user.save()
            print(f'add new user{new_user.first_name}{new_user.last_name} , phone:{new_user.phone}')


# because phone number is a primary key it should be unique this method
# check that if a duplicated phone number exists or not
def check_unique_phones(file):
    duplicate_phones = []
    set_phones = set()
    for i in range(0, file.shape[0]):
        if (file.iloc[i, phone_col]) in set_phones:
            duplicate_phones.append(file.iloc[i, phone_col])
        else:
            set_phones.add(file.iloc[i, phone_col])
    if len(duplicate_phones) > 0:
        print("************************************************************")
        print("warning! you have duplicated phone number. check it manually")
        print(duplicate_phones)
        print("************************************************************")
        return False
    else:
        return True


# rate in csv file is not a int it should be parsed to int by this method
def correct_rate(str_rate):
    slashplace = str_rate.index('/')
    result = int(float(str_rate[0:slashplace]))
    return result


# this method add an exam result to take exam in database
def addexam(file, examno):
    for i in range(0, file.shape[0]):
        user = User.objects.get(phone=file.iloc[i, phone_col])
        rate = correct_rate(file.iloc[i, rate_col])
        if not TakeExam.objects.filter(user=user, exam_number=examno).exists():
            new_exam = TakeExam(exam_number=examno, user=user, rate=rate)
            new_exam.save()
            print(
                f'add new exam result for {new_exam.user.first_name}{new_exam.user.last_name} and reate is {new_exam.rate}')


# calculate sum of rate in different exams for each user
def show_final_result():
    all = TakeExam.objects.values('user__phone').annotate(sum_rate=Sum('rate')).order_by('-sum_rate')
    return all


# write final exam results and rating in final.csv in media directory
def writefinalresult():
    results = show_final_result()
    f = open('media/final.csv', 'w', encoding='utf-8')
    writer = csv.writer(f)
    writer.writerow(['نام', 'نام خانوادگی', 'شماره تماس', 'مجموع امتیازات'])
    print('started writing')
    for res in results:
        obj = User.objects.get(phone=res['user__phone'])
        writer.writerow([obj.first_name, obj.last_name, obj.phone, str(res['sum_rate'])])
    print('finish writing')
    f.close()


def main(filepath, examno):
    exam_no = int(input('enter exam number'))
    filepath = input('enter file name')
    file = pd.read_csv(filepath)
    addusers(file)
    if check_unique_phones(file):
        addexam(file, examno)


