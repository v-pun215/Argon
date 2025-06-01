import datetime
import json
import os
currn_dir = os.getcwd()
def getTime(instance_name):
    os.chdir(currn_dir)
    with open("launcherProfiles.json", "r") as js_read:
        s = js_read.read()
        s = s.replace('\t','')  #Trailing commas in dict cause file read problems, these lines will fix it.
        s = s.replace('\n','')  #Found this on stackoverflow.
        s = s.replace(',}','}')
        s = s.replace(',]',']')
        data = json.loads(s)
        #print(json.dumps(data, indent=4,))
    timePlayed = data['all-instances'][0][instance_name][0]['timePlayed']
    if timePlayed == 0:
        return "00:00:00"
    else:
        return timePlayed
    
def addTime(instance_name, time_amt):
    if instance_name == "Latest Release" or instance_name == "Latest Snapshot":
        print("Cannot add time to the latest release or snapshot instance.")
        return
    os.chdir(currn_dir)
    with open("launcherProfiles.json", "r") as js_read:
        s = js_read.read()
        s = s.replace('\t','')  #Trailing commas in dict cause file read problems, these lines will fix it.
        s = s.replace('\n','')  #Found this on stackoverflow.
        s = s.replace(',}','}')
        s = s.replace(',]',']')
        data = json.loads(s)
        #print(json.dumps(data, indent=4,))
    timePlayed = data['all-instances'][0][instance_name][0]['timePlayed']

    hrs,mins,secs=timePlayed.split(':')
    oghrs = int(hrs)
    ogmins = int(mins)
    ogsecs = int(secs)

    originalTime=datetime.datetime.combine(datetime.date.today(), datetime.time(hour=oghrs,minute=ogmins,second=ogsecs))


    hd,md,sd=str(time_amt).split(':')

    newhrs = int(hd)
    newmins = int(md)
    newsecs = int(sd)

    addedTime=datetime.timedelta(hours=newhrs, minutes=newmins, seconds=newsecs)

    updatedTime = originalTime + addedTime

    timeToPut = updatedTime.time()

    data['all-instances'][0][instance_name][0]['timePlayed'] = str(timeToPut)

    with open("launcherProfiles.json", "w") as js_write:
        js_write.write(json.dumps(data, indent=4))
    
def timeToWords(time_str):
    """Formats a time string (HH:MM:SS) into words."""

    hour, minute, second = map(int, time_str.split(':'))

    return f"{hour}h {minute}m {second}s"

def fancyTimeToWords(time_str):
    """Formats a time string (HH:MM:SS) into words."""

    hour, minute, second = map(int, time_str.split(':'))
    if hour == 0:
        return f"{minute} minutes"
    else:
        return f"{hour} hours and {minute} minutes"

def getTotalTimePlayed():
    with open("launcherProfiles.json") as f:
        data = json.load(f)

    all_insts = data['all-instances']
    all_time = "00:00:00"
    for inst_dict in all_insts:
        for instance_name, instance_data_list in inst_dict.items():
            instance_data = instance_data_list[0]
            time_amt = instance_data["timePlayed"]
            timePlayed = all_time

            hrs,mins,secs=timePlayed.split(':')
            oghrs = int(hrs)
            ogmins = int(mins)
            ogsecs = int(secs)

            originalTime=datetime.datetime.combine(datetime.date.today(), datetime.time(hour=oghrs,minute=ogmins,second=ogsecs))


            hd,md,sd=str(time_amt).split(':')

            newhrs = int(hd)
            newmins = int(md)
            newsecs = int(sd)

            addedTime=datetime.timedelta(hours=newhrs, minutes=newmins, seconds=newsecs)

            updatedTime = originalTime + addedTime

            timeToPut = updatedTime.time()

            timeToPut = str(timeToPut)
            all_time = timeToPut

    return all_time

def getFavInstance():
    with open("launcherProfiles.json") as f:
        data = json.load(f)

    all_insts = data['all-instances']
    if all_insts == [{}]:
        return "No instance"
    all_time = "00:00:00"
    fav_instance = ""
    fav_time = "00:00:00"
    playTimes = []
    for inst_dict in all_insts:
        for instance_name, instance_data_list in inst_dict.items():
            instance_data = instance_data_list[0]
            time_amt = instance_data["timePlayed"]
            timePlayed = all_time
            hd,md,sd=str(time_amt).split(':')

            newhrs = int(hd)
            newmins = int(md)
            newsecs = int(sd)

            addedTime=datetime.timedelta(hours=newhrs, minutes=newmins, seconds=newsecs)


            playTimes.append(str(addedTime))


    time_objects = [datetime.datetime.strptime(t, '%H:%M:%S') for t in playTimes]
    max_time = max(time_objects)
    max_time_str = max_time.strftime('%H:%M:%S')

    for inst_dict in all_insts:
        for instance_name, instance_data_list in inst_dict.items():
            instance_data = instance_data_list[0]
            time_amt = instance_data["timePlayed"]
            timePlayed = all_time

            hrs,mins,secs=timePlayed.split(':')
            oghrs = int(hrs)
            ogmins = int(mins)
            ogsecs = int(secs)

            originalTime=datetime.datetime.combine(datetime.date.today(), datetime.time(hour=oghrs,minute=ogmins,second=ogsecs))


            hd,md,sd=str(time_amt).split(':')

            newhrs = int(hd)
            newmins = int(md)
            newsecs = int(sd)

            addedTime=datetime.timedelta(hours=newhrs, minutes=newmins, seconds=newsecs)

            updatedTime = originalTime + addedTime
            updatedTime = updatedTime.time()
            updatedTime = str(updatedTime)

            if updatedTime == max_time_str:
                fav_instance = instance_name
                fav_time = updatedTime
            

    if fav_instance == "":
        return "No instance"
    else:
        return fav_instance
def getFavInstIcon():
    with open("launcherProfiles.json") as f:
        data = json.load(f)
    all_insts = data['all-instances']
    if all_insts == [{}]:
        return "release"
    all_time = "00:00:00"
    fav_instance = ""
    fav_time = "00:00:00"
    playTimes = []
    for inst_dict in all_insts:
        for instance_name, instance_data_list in inst_dict.items():
            instance_data = instance_data_list[0]
            time_amt = instance_data["timePlayed"]
            timePlayed = all_time
            hd,md,sd=str(time_amt).split(':')

            newhrs = int(hd)
            newmins = int(md)
            newsecs = int(sd)

            addedTime=datetime.timedelta(hours=newhrs, minutes=newmins, seconds=newsecs)


            playTimes.append(str(addedTime))


    time_objects = [datetime.datetime.strptime(t, '%H:%M:%S') for t in playTimes]
    max_time = max(time_objects)
    max_time_str = max_time.strftime('%H:%M:%S')

    for inst_dict in all_insts:
        for instance_name, instance_data_list in inst_dict.items():
            instance_data = instance_data_list[0]
            time_amt = instance_data["timePlayed"]
            timePlayed = all_time

            hrs,mins,secs=timePlayed.split(':')
            oghrs = int(hrs)
            ogmins = int(mins)
            ogsecs = int(secs)

            originalTime=datetime.datetime.combine(datetime.date.today(), datetime.time(hour=oghrs,minute=ogmins,second=ogsecs))


            hd,md,sd=str(time_amt).split(':')

            newhrs = int(hd)
            newmins = int(md)
            newsecs = int(sd)

            addedTime=datetime.timedelta(hours=newhrs, minutes=newmins, seconds=newsecs)

            updatedTime = originalTime + addedTime
            updatedTime = updatedTime.time()
            updatedTime = str(updatedTime)

            if updatedTime == max_time_str:
                fav_instance = instance_name
                fav_time = updatedTime
            
    with open("launcherProfiles.json") as f:
        data = json.load(f)

    all_insts = data['all-instances']
    for inst_dict in all_insts:
        for instance_name, instance_data_list in inst_dict.items():
            if instance_name == fav_instance:
                return instance_data_list[0]["icon"]
            
    return "release"
getFavInstIcon()