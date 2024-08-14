from django.shortcuts import render, redirect
from .models import *
import requests
import math


def index(request):
    url = 'https://ergast.com/api/f1/current/results.json?limit=1000'
    response = requests.get(url)
    data = response.json()['MRData']['RaceTable']['Races']

    round = CurrentSeason.objects.get(constructorId = 'rb')
    if len(data) != round.roundNumber:
        loadCurrentData()
        
    if request.method == "POST":
        if 'driver' in request.POST:
            driverId = request.POST['driver']
            trackId = request.POST['track']
            return redirect('driver', driverId=driverId, trackId=trackId)
        elif 'track' in request.POST:
            trackId = request.POST['track']
            return redirect('race', trackId=trackId)
        
    return render(request, "predictor/index.html")

def driver(request, driverId, trackId):
    if request.method == "POST":
        driverId = request.POST['driver']
        trackId = request.POST['track']
        return redirect('driver', driverId=driverId, trackId=trackId)
    
    quali, result = prediction(trackId, driverId)
    driver = Driver.objects.get(driverId = driverId)
    track = Track.objects.get(trackId = trackId)
    constructor = Constructor.objects.get(constructorId = driver.constructorId)
    suffix1, suffix2 = suffix(quali, result)
    driverProfile = DriverProfile.objects.get(driverId = driverId)
    trackProfile = TrackProfile.objects.get(trackId = trackId)

    return render(request, "predictor/driver.html", {
        'driver': driver,
        'track': track,
        'constructor': constructor,
        'quali': quali,
        'result': result,
        'suffix1': suffix1,
        'suffix2': suffix2,
        'driverProfile': driverProfile,
        'trackProfile': trackProfile
    })

def race(request, trackId):
    track = Track.objects.get(trackId = trackId)
    quali, result = prediction(trackId)
    driverStanding, constructorStanding = standings(result)
    trackProfile = TrackProfile.objects.get(trackId = trackId)

    if request.method == "POST":
        trackId = request.POST['track']
        return redirect('race', trackId=trackId)


    return render(request, "predictor/race.html", {
        'track': track,
        'quali': quali,
        'result': result,
        'driverStanding': driverStanding,
        'constructorStanding': constructorStanding,
        'trackProfile': trackProfile
    })


def prediction(trackId, driverId=None):
    prediction = {}
    drivers = Driver.objects.all()
    for i in drivers:
        qualiDiff, resultDiff = racePercentageDiffs(i.driverId, trackId)
        qualiPrediction, resultPrediction = racePrediction(i.driverId, qualiDiff, resultDiff)
        prediction[i.driverName] = [qualiPrediction, resultPrediction]

    qualiPrediction = sorted(prediction.items(), key=lambda x: x[1][0])
    resultPrediction = sorted(prediction.items(), key=lambda x: x[1][1])

    if driverId == None:
        return qualiPrediction, resultPrediction
    else:
        driverName = Driver.objects.get(driverId = driverId).driverName
        qualiIndex = 1
        for key, value in qualiPrediction:
            if key == driverName:
                quali = qualiIndex
                break
            qualiIndex += 1

        resultIndex = 1
        for key, value in resultPrediction:
            if key == driverName:
                result = resultIndex
                break
            resultIndex += 1

        return quali, result

def suffix(quali, result):
    suffix = {1 : 'st', 2 : 'nd', 3 : 'rd'}
    suffixes = []
    
    if quali in suffix:
        suffixes.append(suffix[quali])
    else:
        suffixes.append('th')

    if result in suffix:
        suffixes.append(suffix[result])
    else:
        suffixes.append('th')

    return suffixes[0], suffixes[1]

def racePercentageDiffs(driverId, trackId):
    constructorId = Driver.objects.get(driverId = driverId).constructorId

    trackD = TrackResult.objects.get(driverId = driverId, trackId = trackId)
    seasonD = SeasonResult.objects.get(driverId = driverId) 
    trackC = TrackResult.objects.get(constructorId = constructorId, trackId = trackId)
    seasonC = SeasonResult.objects.get(constructorId = constructorId)

    tqD, sqD = avgList(trackD.avgQuali, seasonD.avgQuali)
    trD, srD = avgList(trackD.avgResult, seasonD.avgResult)

    tqC, sqC = avgList(trackC.avgQuali, seasonC.avgQuali)
    trC, srC = avgList(trackC.avgResult, seasonC.avgResult)

    qualiDiffD = resultDiffD = qualiDiffC = resultDiffC = 0

    if tqD != 0:
        qualiDiffD = round((((tqD - sqD) / sqD) * 100) * 0.3, 2)
    if trD != 0:
        resultDiffD = round((((trD - srD) / srD) * 100) * 0.3, 2)
    if tqC != 0:
        qualiDiffC = round((((tqC - sqC) / sqC) * 100) * 0.15, 2)
    if trC != 0:
        resultDiffC = round((((trC - srC) / srC) * 100) * 0.15, 2)

    qualiDiff = qualiDiffD + qualiDiffC
    resultDiff = resultDiffD + resultDiffC

    return qualiDiff, resultDiff

def avgList(list1, list2):
    count = 0
    total_1 = total_2 = 0
    index = 0

    if list1 != []:
        for avg in list1:
            if avg != -1 and list2[index] != -1:
                total_1 += float(avg)
                total_2 += float(list2[index])
                count += 1
            index += 1
        
    if count != 0:
        return round((total_1 / count), 2), round((total_2 / count), 2)
    else:
        return 0, 0

def racePrediction(driverId, qualiDiff, resultDiff):
    constructorId = Driver.objects.get(driverId = driverId).constructorId

    currentDriver = CurrentSeason.objects.get(driverId = driverId)
    currentConstructor = CurrentSeason.objects.get(constructorId = constructorId)

    prediction = ((currentDriver.avgQuali * 3) + currentConstructor.avgQuali) / 4
    qualiPrediction = prediction * ((100 + qualiDiff) / 100)

    prediction = ((currentDriver.avgResult * 3) + currentConstructor.avgResult) / 4
    resultPrediction = prediction * ((100 + resultDiff) / 100)

    return qualiPrediction, resultPrediction

def standings(prediction):
    currentStandings = CurrentStanding.objects.all()
    constructorDict = {}
    driverDict = {}
    pointList = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]

    for i in currentStandings:
        if i.driverId:
            points = i.points
            index = 0
            for key, value in prediction:
                try:
                    driver = Driver.objects.get(driverName = key)
                    if i.driverId == driver.driverId:
                        points += pointList[index]
                        index += 1
                except:
                    pass
                index += 1
            try:
                driverN = Driver.objects.get(driverId = i.driverId)
                driverDict[driverN.driverName] = int(math.floor(points))
            except:
                pass
        else:
            points = i.points
            index = 0
            for key, value in prediction:
                try:
                    constructor = Driver.objects.get(driverName = key)
                    if i.constructorId == constructor.constructorId:
                        points += pointList[index]
                except:
                    pass
                index += 1
            try:
                constructorN = Constructor.objects.get(constructorId = i.constructorId)
                constructorDict[constructorN.constructorName] = int(math.floor(points))
            except:
                pass

    driver = sorted(driverDict.items(), key=lambda x: x[1], reverse=True)
    constructor = sorted(constructorDict.items(), key=lambda x: x[1], reverse=True)

    return driver, constructor

def loadDatabase(request):
    url = 'https://ergast.com/api/f1/current/results.json?limit=1000'
    response = requests.get(url)
    data = response.json()['MRData']['RaceTable']['Races']

    round = CurrentSeason.objects.get(constructorId = 'rb')
    if len(data) != round.roundNumber:
        loadCurrentData()

    dnf = ['R', 'D', 'E', 'W', 'F', 'N']

    for i in range(5):
        driverDict = {
            "max_verstappen": {"result": 0, "quali": 0, "rc": 0, "qc": 0},
            "alonso": {"result": 0, "quali": 0, "rc": 0, "qc": 0},
            "gasly": {"result": 0, "quali": 0, "rc": 0, "qc": 0},
            "perez": {"result": 0, "quali": 0, "rc": 0, "qc": 0},
            "sainz": {"result": 0, "quali": 0, "rc": 0, "qc": 0},
            "hamilton": {"result": 0, "quali": 0, "rc": 0, "qc": 0},
            "norris": {"result": 0, "quali": 0, "rc": 0, "qc": 0},
            "albon": {"result": 0, "quali": 0, "rc": 0, "qc": 0},
            "piastri": {"result": 0, "quali": 0, "rc": 0, "qc": 0},
            "ocon": {"result": 0, "quali": 0, "rc": 0, "qc": 0},
            "stroll": {"result": 0, "quali": 0, "rc": 0, "qc": 0},
            "hulkenberg": {"result": 0, "quali": 0, "rc": 0, "qc": 0},
            "ricciardo": {"result": 0, "quali": 0, "rc": 0, "qc": 0},
            "bottas": {"result": 0, "quali": 0, "rc": 0, "qc": 0},
            "tsunoda": {"result": 0, "quali": 0, "rc": 0, "qc": 0},
            "kevin_magnussen": {"result": 0, "quali": 0, "rc": 0, "qc": 0},
            "russell": {"result": 0, "quali": 0, "rc": 0, "qc": 0},
            "zhou": {"result": 0, "quali": 0, "rc": 0, "qc": 0},
            "leclerc": {"result": 0, "quali": 0, "rc": 0, "qc": 0},
            "sargeant": {"result": 0, "quali": 0, "rc": 0, "qc": 0}
        }

        constructorDict = {
            "williams": {"result": 0, "quali": 0, "rc": 0, "qc": 0},
            "red_bull": {"result": 0, "quali": 0, "rc": 0, "qc": 0},
            "sauber": {"result": 0, "quali": 0, "rc": 0, "qc": 0},
            "mercedes": {"result": 0, "quali": 0, "rc": 0, "qc": 0},
            "mclaren": {"result": 0, "quali": 0, "rc": 0, "qc": 0},
            "haas": {"result": 0, "quali": 0, "rc": 0, "qc": 0},
            "ferrari": {"result": 0, "quali": 0, "rc": 0, "qc": 0},
            "aston_martin": {"result": 0, "quali": 0, "rc": 0, "qc": 0},
            "alpine": {"result": 0, "quali": 0, "rc": 0, "qc": 0},
            "rb": {"result": 0, "quali": 0, "rc": 0, "qc": 0}
        }
        
        for key, value in driverDict.items():
            newDriver = SeasonResult(driverId = key)
            newDriver.save()

        for key, value in constructorDict.items():
            newCon = SeasonResult(constructorId = key)
            newCon.save()
    
        url = f'https://ergast.com/api/f1/{2023 - i}/results.json?limit=1000'
        response = requests.get(url)
        data = response.json()['MRData']['RaceTable']['Races']

        for j in range(len(data)):
            for k in range(len(data[j]['Results'])):
                if data[j]['Results'][k]['Driver']['driverId'] in driverDict:
                    if data[j]['Results'][k]['positionText'] not in dnf:
                        driverDict[data[j]['Results'][k]['Driver']['driverId']]['result'] += int(data[j]['Results'][k]['position'])
                        driverDict[data[j]['Results'][k]['Driver']['driverId']]['rc'] += 1
                    if data[j]['Results'][k]['grid'] != 0:
                        driverDict[data[j]['Results'][k]['Driver']['driverId']]['quali'] += int(data[j]['Results'][k]['grid'])
                        driverDict[data[j]['Results'][k]['Driver']['driverId']]['qc'] += 1
                    
                if data[j]['Results'][k]['Constructor']['constructorId'] in constructorDict:
                    if data[j]['Results'][k]['positionText'] not in dnf:
                        constructorDict[data[j]['Results'][k]['Constructor']['constructorId']]['result'] += int(data[j]['Results'][k]['position'])
                        constructorDict[data[j]['Results'][k]['Constructor']['constructorId']]['rc'] += 1
                    if data[j]['Results'][k]['grid'] != 0:
                        constructorDict[data[j]['Results'][k]['Constructor']['constructorId']]['quali'] += int(data[j]['Results'][k]['grid'])
                        constructorDict[data[j]['Results'][k]['Constructor']['constructorId']]['qc'] += 1
                else:
                    if data[j]['Results'][k]['Constructor']['constructorId'] == 'alfa':
                        if data[j]['Results'][k]['positionText'] not in dnf:
                            constructorDict['sauber']['result'] += int(data[j]['Results'][k]['position'])
                            constructorDict['sauber']['rc'] += 1
                        if data[j]['Results'][k]['grid'] != 0:
                            constructorDict['sauber']['quali'] += int(data[j]['Results'][k]['grid'])
                            constructorDict['sauber']['qc'] += 1
                    elif data[j]['Results'][k]['Constructor']['constructorId'] == 'alphatauri' or data[j]['Results'][k]['Constructor']['constructorId'] == 'toro_rosso':
                        if data[j]['Results'][k]['positionText'] not in dnf:
                            constructorDict['rb']['result'] += int(data[j]['Results'][k]['position'])
                            constructorDict['rb']['rc'] += 1
                        if data[j]['Results'][k]['grid'] != 0:
                            constructorDict['rb']['quali'] += int(data[j]['Results'][k]['grid'])
                            constructorDict['rb']['qc'] += 1
                    elif data[j]['Results'][k]['Constructor']['constructorId'] == 'racing_point':
                        if data[j]['Results'][k]['positionText'] not in dnf:
                            constructorDict['aston_martin']['result'] += int(data[j]['Results'][k]['position'])
                            constructorDict['aston_martin']['rc'] += 1
                        if data[j]['Results'][k]['grid'] != 0:
                            constructorDict['aston_martin']['quali'] += int(data[j]['Results'][k]['grid'])
                            constructorDict['aston_martin']['qc'] += 1
                    elif data[j]['Results'][k]['Constructor']['constructorId'] == 'renault':
                        if data[j]['Results'][k]['positionText'] not in dnf:
                            constructorDict['alpine']['result'] += int(data[j]['Results'][k]['position'])
                            constructorDict['alpine']['rc'] += 1
                        if data[j]['Results'][k]['grid'] != 0:
                            constructorDict['alpine']['quali'] += int(data[j]['Results'][k]['grid'])
                            constructorDict['alpine']['qc'] += 1


        for key, value in driverDict.items():
            driver = SeasonResult.objects.get(driverId = key)
            if value["rc"] != 0:
                driver.avgResult.append(round((value["result"] / value["rc"]), 1))
                driver.avgQuali.append(round((value["quali"] / value["qc"]), 1))
                driver.save()

        for key, value in constructorDict.items():
            constructor = SeasonResult.objects.get(constructorId = key)
            constructor.avgResult.append(round((value["result"] / value["rc"]), 1))
            constructor.avgQuali.append(round((value["quali"] / value["qc"]), 1))
            constructor.save()



    data = TrackResult.objects.filter()

    for obj in data:
        count = 0
        for num in obj.avgQuali:
            if type(num) == str:
                obj.avgQuali.pop(count)
                obj.avgQuali.insert(count, float(num))
            count += 1
        count = 0
        for num in obj.avgResult:
            if type(num) == str:
                obj.avgResult.pop(count)
                obj.avgResult.insert(count, float(num))
            count += 1
        obj.save()


    # gets the average result at each track for the last 5 seasons
    dnf = ['R', 'D', 'E', 'W', 'F', 'N']

    trackId = Track.objects.filter()

    for t in range(len(trackId)):
        driverDict = {
            "max_verstappen": {"result": [], "quali": [], "rc": 0, "qc": 0},
            "alonso": {"result": [], "quali": [], "rc": 0, "qc": 0},
            "gasly": {"result": [], "quali": [], "rc": 0, "qc": 0},
            "perez": {"result": [], "quali": [], "rc": 0, "qc": 0},
            "sainz": {"result": [], "quali": [], "rc": 0, "qc": 0},
            "hamilton": {"result": [], "quali": [], "rc": 0, "qc": 0},
            "norris": {"result": [], "quali": [], "rc": 0, "qc": 0},
            "albon": {"result": [], "quali": [], "rc": 0, "qc": 0},
            "piastri": {"result": [], "quali": [], "rc": 0, "qc": 0},
            "ocon": {"result": [], "quali": [], "rc": 0, "qc": 0},
            "stroll": {"result": [], "quali": [], "rc": 0, "qc": 0},
            "hulkenberg": {"result": [], "quali": [], "rc": 0, "qc": 0},
            "ricciardo": {"result": [], "quali": [], "rc": 0, "qc": 0},
            "bottas": {"result": [], "quali": [], "rc": 0, "qc": 0},
            "tsunoda": {"result": [], "quali": [], "rc": 0, "qc": 0},
            "kevin_magnussen": {"result": [], "quali": [], "rc": 0, "qc": 0},
            "russell": {"result": [], "quali": [], "rc": 0, "qc": 0},
            "zhou": {"result": [], "quali": [], "rc": 0, "qc": 0},
            "leclerc": {"result": [], "quali": [], "rc": 0, "qc": 0},
            "sargeant": {"result": [], "quali": [], "rc": 0, "qc": 0}
        }

        constructorDict = {
            "williams": {"result": [], "quali": []},
            "red_bull": {"result": [], "quali": []},
            "sauber": {"result": [], "quali": []},
            "mercedes": {"result": [], "quali": []},
            "mclaren": {"result": [], "quali": []},
            "haas": {"result": [], "quali": []},
            "ferrari": {"result": [], "quali": []},
            "aston_martin": {"result": [], "quali": []},
            "alpine": {"result": [], "quali": []},
            "rb": {"result": [], "quali": []}
        }
        count = 0
        for i in range(5):
            url = f'https://ergast.com/api/f1/{2023 - i}/circuits/{trackId[t].trackId}/results.json'
            response = requests.get(url)
            data = response.json()['MRData']['RaceTable']['Races']

            if data:
                for j in range(len(data[0]['Results'])):
                    if data[0]['Results'][j]['Driver']['driverId'] in driverDict:
                        if data[0]['Results'][j]['positionText'] not in dnf:
                            driverDict[data[0]['Results'][j]['Driver']['driverId']]['result'].append(data[0]['Results'][j]['position'])
                            driverDict[data[0]['Results'][j]['Driver']['driverId']]['rc'] += 1
                        else:
                            driverDict[data[0]['Results'][j]['Driver']['driverId']]['result'].append(-1)
                            driverDict[data[0]['Results'][j]['Driver']['driverId']]['rc'] += 1
                        
                        if data[0]['Results'][j]['grid'] != '0':
                            driverDict[data[0]['Results'][j]['Driver']['driverId']]['quali'].append(data[0]['Results'][j]['grid'])
                            driverDict[data[0]['Results'][j]['Driver']['driverId']]['qc'] += 1
                        else:
                            driverDict[data[0]['Results'][j]['Driver']['driverId']]['quali'].append(-1)
                            driverDict[data[0]['Results'][j]['Driver']['driverId']]['qc'] += 1

                    if data[0]['Results'][j]['Constructor']['constructorId'] in constructorDict:
                        if data[0]['Results'][j]['positionText'] not in dnf:
                            constructorDict[data[0]['Results'][j]['Constructor']['constructorId']]['result'].append(data[0]['Results'][j]['position'])
                        else:
                            constructorDict[data[0]['Results'][j]['Constructor']['constructorId']]['result'].append(-1)

                        if data[0]['Results'][j]['grid'] != '0':
                            constructorDict[data[0]['Results'][j]['Constructor']['constructorId']]['quali'].append(data[0]['Results'][j]['grid'])
                        else:
                            constructorDict[data[0]['Results'][j]['Constructor']['constructorId']]['quali'].append(-1)
                    else:
                        if data[0]['Results'][j]['Constructor']['constructorId'] == 'alphatauri' or data[0]['Results'][j]['Constructor']['constructorId'] == 'toro_rosso':
                            if data[0]['Results'][j]['positionText'] not in dnf:
                                constructorDict['rb']['result'].append(data[0]['Results'][j]['position'])
                            else:
                                constructorDict['rb']['result'].append(-1)

                            if data[0]['Results'][j]['grid'] != '0':
                                constructorDict['rb']['quali'].append(data[0]['Results'][j]['grid'])
                            else:
                                constructorDict['rb']['quali'].append(-1)
                        elif data[0]['Results'][j]['Constructor']['constructorId'] == 'alfa':
                            if data[0]['Results'][j]['positionText'] not in dnf:
                                constructorDict['sauber']['result'].append(data[0]['Results'][j]['position'])
                            else:
                                constructorDict['sauber']['result'].append(-1)

                            if data[0]['Results'][j]['grid'] != '0':
                                constructorDict['sauber']['quali'].append(data[0]['Results'][j]['grid'])
                            else:
                                constructorDict['sauber']['quali'].append(-1)
                        elif data[0]['Results'][j]['Constructor']['constructorId'] == 'racing_point':
                            if data[0]['Results'][j]['positionText'] not in dnf:
                                constructorDict['aston_martin']['result'].append(data[0]['Results'][j]['position'])
                            else:
                                constructorDict['aston_martin']['result'].append(-1)

                            if data[0]['Results'][j]['grid'] != '0':
                                constructorDict['aston_martin']['quali'].append(data[0]['Results'][j]['grid'])
                            else:
                                constructorDict['aston_martin']['quali'].append(-1)
                        elif data[0]['Results'][j]['Constructor']['constructorId'] == 'renault':
                            if data[0]['Results'][j]['positionText'] not in dnf:
                                constructorDict['alpine']['result'].append(data[0]['Results'][j]['position'])
                            else:
                                constructorDict['alpine']['result'].append(-1)

                            if data[0]['Results'][j]['grid'] != '0':
                                constructorDict['alpine']['quali'].append(data[0]['Results'][j]['grid'])
                            else:
                                constructorDict['alpine']['quali'].append(-1)

            count += 1 
            for key, value in driverDict.items():
                if value["rc"] != count:
                    value["result"].append(-1)
                    value["rc"] += 1
                if value["qc"] != count:
                    value["quali"].append(-1)
                    value["qc"] += 1

            for key, value in constructorDict.items():
                if len(value["result"]) == ((count * 2) - 2):
                    value["result"].append(-1)
                    value["result"].append(-1)
                elif len(value["result"]) == ((count * 2) -1 ):
                    value["result"].append(-1)
                if len(value["quali"]) == ((count * 2) - 2):
                    value["quali"].append(-1)
                    value["quali"].append(-1)
                elif len(value["quali"]) == ((count * 2) -1 ):
                    value["quali"].append(-1)

        for key, value in driverDict.items():
            newDriver = TrackResult(trackId = trackId[t].trackId, driverId = key)
            for x in range(5):
                newDriver.avgResult.append(value["result"][x])
                newDriver.avgQuali.append(value["quali"][x])
        
        for key, value in constructorDict.items():
            newConstructor = TrackResult(trackId = trackId[t].trackId, constructorId = key)
            for y in range(0, 10, 2):
                if value["result"][y] != -1:
                    if value["result"][y + 1] != -1:
                        newConstructor.avgResult.append(((int(value["result"][y]) + int(value["result"][y + 1])) / 2))
                    else:
                        newConstructor.avgResult.append(value["result"][y])
                elif value["result"][y + 1] != -1:
                    newConstructor.avgResult.append(value["result"][y + 1])
                else:
                    newConstructor.avgResult.append(-1)

                if value["quali"][y] != -1:
                    if value["quali"][y + 1] != -1:
                        newConstructor.avgQuali.append(((int(value["quali"][y]) + int(value["quali"][y + 1])) / 2))
                    else:
                        newConstructor.avgQuali.append(value["quali"][y])
                elif value["quali"][y + 1] != -1:
                    newConstructor.avgQuali.append(value["quali"][y + 1])
                else:
                    newConstructor.avgQuali.append(-1)
            newConstructor.save()


    # gets the
    dnf = ['R', 'D', 'E', 'W', 'F', 'N']

    trackId = Track.objects.filter()
    driverId = Driver.objects.filter()
    constructorId = Constructor.objects.filter()

    for t in range(len(trackId)):
        for d in range(len(driverId)):
            resultListDriver = []
            qualiListDriver = []
            for i in range(5):
                url = f'https://ergast.com/api/f1/{2023 - i}/circuits/{trackId[t].trackId}/drivers/{driverId[d].driverId}/results.json'
                response = requests.get(url)
                data = response.json()['MRData']['RaceTable']['Races']

                if data:
                    data = data[0]['Results'][0]
                    if data ['positionText'] not in dnf:
                        resultListDriver.append(int(data['position']))
                    else:
                        resultListDriver.append(-1)

                    if data['grid'] != 0:
                        qualiListDriver.append(int(data['grid']))
                    else:
                        qualiListDriver.append(-1)

            trackDriver = TrackResult(trackId = trackId[t].trackId, driverId = driverId[d].driverId)
            for i in resultListDriver:
                trackDriver.avgResult.append(i)
            for i in qualiListDriver:
                trackDriver.avgQuali.append(i)
            trackDriver.save()

        for c in range(len(constructorId)):
            constructor = constructorId[c].constructorId
            resultListConstructor = []
            qualiListConstructor = []
            for i in range(5):
                if constructorId[c].constructorId2 is not None:
                    if (i >= 0 and i <= 3) and constructorId[c].constructorId2.startswith('a'):
                        constructor = constructorId[c].constructorId2
                    elif i >= 3 and constructorId[c].constructorId2.startswith('r'):
                        constructor = constructorId[c].constructorId2
                elif i >= 4 and constructorId[c].constructorId3 is not None:
                    constructor = constructorId[c].constructorId3

                url = f'https://ergast.com/api/f1/{2023 - i}/circuits/{trackId[t].trackId}/constructors/{constructor}/results.json'
                response = requests.get(url)
                data = response.json()['MRData']['RaceTable']['Races']        

                if data:
                    if data[0]['Results'][0]['positionText'] not in dnf:
                        if data[0]['Results'][1]['positionText'] not in dnf:
                            avg_result = (int(data[0]['Results'][0]['position']) + int(data[0]['Results'][1]['position'])) / 2
                            resultListConstructor.append(avg_result)
                        else:
                            resultListConstructor.append(int(data[0]['Results'][0]['position'])) 
                    elif data[0]['Results'][1]['positionText'] not in dnf:
                        resultListConstructor.append(int(data[0]['Results'][1]['position']))
                    else:
                        resultListConstructor.append(-1)

                    if data[0]['Results'][0]['grid'] != 0:
                        if data[0]['Results'][1]['grid'] != 0:
                            avg_quali = (int(data[0]['Results'][0]['grid']) + int(data[0]['Results'][1]['grid'])) / 2
                            qualiListConstructor.append(avg_quali)
                        else:
                            qualiListConstructor.append(int(data[0]['Results'][0]['grid']))
                    elif data[0]['Results'][1]['grid'] != 0:
                        qualiListConstructor.append(int(data[0]['Results'][1]['grid']))
                    else:
                        qualiListConstructor.append(-1)
                else:
                    resultListConstructor.append(-1)
                    qualiListConstructor.append(-1)

            trackConstructor = TrackResult(trackId = trackId[t].trackId, constructorId = constructorId[c].constructorId)
            for i in resultListConstructor:
                trackConstructor.avgResult.append(i)
            for i in qualiListConstructor:
                trackConstructor.avgQuali.append(i)
            trackConstructor.save()

        


    url = 'https://ergast.com/api/f1/2024/circuits.json'
    response = requests.get(url)
    data = response.json()

    data = data['MRData']['CircuitTable']['Circuits']

    for i in range(len(data)):
        trackId = data[i]['circuitId']
        trackName = data[i]['circuitName']
        trackCity = data[i]['Location']['locality']
        trackCountry = data[i]['Location']['country']

        newTrack = Track(trackId = trackId, trackName = trackName, trackCity = trackCity, trackCountry = trackCountry)
        newTrack.save()



    url = 'https://ergast.com/api/f1/2024/constructors.json'
    response = requests.get(url)
    data = response.json()

    data = data['MRData']['ConstructorTable']['Constructors']
    
    for i in range(len(data)):
        constructorId = data[i]['constructorId']
        constructorName = data[i]['name']
        newConstructor = Constructor(constructorId = constructorId, constructorName = constructorName)
        newConstructor.save()

    return render(request, "predictor/index.html")



    url = 'https://ergast.com/api/f1/current/driverStandings.json'
    response = requests.get(url)
    data = response.json()
    data = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']

    for i in range(len(data)):
        driverId = data[i]['Driver']['driverId']
        driverName = f"{data[i]['Driver']['givenName']} {data[i]['Driver']['familyName']}"
        driverCode = data[i]['Driver']['code']
        driverNumber = data[i]['Driver']['permanentNumber']
        driverDOB = data[i]['Driver']['dateOfBirth']
        driverNationality = data[i]['Driver']['nationality']
        constructorId = data[i]['Constructors'][0]['constructorId']
        newDriver = Driver(driverId = driverId, driverName = driverName, driverCode = driverCode, driverNumber = driverNumber, driverDOB = driverDOB, driverNationality = driverNationality, constructorId = constructorId)
        newDriver.save()

    return render(request, "predictor/index.html")

def loadCurrentData():
    CurrentSeason.objects.all().delete()
    CurrentStanding.objects.all().delete()


    url = 'https://ergast.com/api/f1/current/results.json?limit=1000'
    response = requests.get(url)
    data = response.json()['MRData']['RaceTable']['Races']

    dnf = ['R', 'D', 'E', 'W', 'F', 'N']

    driverDict = {
        "max_verstappen": {"result": 0, "quali": 0, "rc": 0, "qc": 0},
        "alonso": {"result": 0, "quali": 0, "rc": 0, "qc": 0},
        "gasly": {"result": 0, "quali": 0, "rc": 0, "qc": 0},
        "perez": {"result": 0, "quali": 0, "rc": 0, "qc": 0},
        "sainz": {"result": 0, "quali": 0, "rc": 0, "qc": 0},
        "hamilton": {"result": 0, "quali": 0, "rc": 0, "qc": 0},
        "norris": {"result": 0, "quali": 0, "rc": 0, "qc": 0},
        "albon": {"result": 0, "quali": 0, "rc": 0, "qc": 0},
        "piastri": {"result": 0, "quali": 0, "rc": 0, "qc": 0},
        "ocon": {"result": 0, "quali": 0, "rc": 0, "qc": 0},
        "stroll": {"result": 0, "quali": 0, "rc": 0, "qc": 0},
        "hulkenberg": {"result": 0, "quali": 0, "rc": 0, "qc": 0},
        "ricciardo": {"result": 0, "quali": 0, "rc": 0, "qc": 0},
        "bottas": {"result": 0, "quali": 0, "rc": 0, "qc": 0},
        "tsunoda": {"result": 0, "quali": 0, "rc": 0, "qc": 0},
        "kevin_magnussen": {"result": 0, "quali": 0, "rc": 0, "qc": 0},
        "russell": {"result": 0, "quali": 0, "rc": 0, "qc": 0},
        "zhou": {"result": 0, "quali": 0, "rc": 0, "qc": 0},
        "leclerc": {"result": 0, "quali": 0, "rc": 0, "qc": 0},
        "sargeant": {"result": 0, "quali": 0, "rc": 0, "qc": 0}
    }

    constructorDict = {
        "williams": {"result": 0, "quali": 0, "rc": 0, "qc": 0},
        "red_bull": {"result": 0, "quali": 0, "rc": 0, "qc": 0},
        "sauber": {"result": 0, "quali": 0, "rc": 0, "qc": 0},
        "mercedes": {"result": 0, "quali": 0, "rc": 0, "qc": 0},
        "mclaren": {"result": 0, "quali": 0, "rc": 0, "qc": 0},
        "haas": {"result": 0, "quali": 0, "rc": 0, "qc": 0},
        "ferrari": {"result": 0, "quali": 0, "rc": 0, "qc": 0},
        "aston_martin": {"result": 0, "quali": 0, "rc": 0, "qc": 0},
        "alpine": {"result": 0, "quali": 0, "rc": 0, "qc": 0},
        "rb": {"result": 0, "quali": 0, "rc": 0, "qc": 0}
    }

    for key, value in driverDict.items():
        newDriver = CurrentSeason(driverId = key, roundNumber = 8, avgResult = 0, avgQuali = 0)
        newDriver.save()

    for key, value in constructorDict.items():
        newCon = CurrentSeason(constructorId = key, roundNumber = 8, avgResult = 0, avgQuali = 0)
        newCon.save()

    for i in range(len(data)):
        for j in range(len(data[i]['Results'])):
            if data[i]['Results'][j]['Driver']['driverId'] in driverDict:
                if data[i]['Results'][j]['positionText'] not in dnf:
                    driverDict[data[i]['Results'][j]['Driver']['driverId']]['result'] += int(data[i]['Results'][j]['position'])
                    driverDict[data[i]['Results'][j]['Driver']['driverId']]['rc'] += 1
                if data[i]['Results'][j]['grid'] != 0:
                    driverDict[data[i]['Results'][j]['Driver']['driverId']]['quali'] += int(data[i]['Results'][j]['grid'])
                    driverDict[data[i]['Results'][j]['Driver']['driverId']]['qc'] += 1

            if data[i]['Results'][j]['Constructor']['constructorId'] in constructorDict:
                if data[i]['Results'][j]['positionText'] not in dnf:
                    constructorDict[data[i]['Results'][j]['Constructor']['constructorId']]['result'] += int(data[i]['Results'][j]['position'])
                    constructorDict[data[i]['Results'][j]['Constructor']['constructorId']]['rc'] += 1
                if data[i]['Results'][j]['grid'] != 0:
                    constructorDict[data[i]['Results'][j]['Constructor']['constructorId']]['quali'] += int(data[i]['Results'][j]['grid'])
                    constructorDict[data[i]['Results'][j]['Constructor']['constructorId']]['qc'] += 1
            else:
                if data[i]['Results'][j]['Constructor']['constructorId'] == 'alfa':
                    if data[i]['Results'][j]['positionText'] not in dnf:
                        constructorDict['sauber']['result'] += int(data[i]['Results'][j]['position'])
                        constructorDict['sauber']['rc'] += 1
                    if data[i]['Results'][j]['grid'] != 0:
                        constructorDict['sauber']['quali'] += int(data[i]['Results'][j]['grid'])
                        constructorDict['sauber']['qc'] += 1
                elif data[i]['Results'][j]['Constructor']['constructorId'] == 'alphatauri' or data[i]['Results'][j]['Constructor']['constructorId'] == 'toro_rosso':
                    if data[i]['Results'][j]['positionText'] not in dnf:
                        constructorDict['rb']['result'] += int(data[i]['Results'][j]['position'])
                        constructorDict['rb']['rc'] += 1
                    if data[i]['Results'][j]['grid'] != 0:
                        constructorDict['rb']['quali'] += int(data[i]['Results'][j]['grid'])
                        constructorDict['rb']['qc'] += 1
                elif data[i]['Results'][j]['Constructor']['constructorId'] == 'racing_point':
                    if data[i]['Results'][j]['positionText'] not in dnf:
                        constructorDict['aston_martin']['result'] += int(data[i]['Results'][j]['position'])
                        constructorDict['aston_martin']['rc'] += 1
                    if data[i]['Results'][j]['grid'] != 0:
                        constructorDict['aston_martin']['quali'] += int(data[i]['Results'][j]['grid'])
                        constructorDict['aston_martin']['qc'] += 1
                elif data[i]['Results'][j]['Constructor']['constructorId'] == 'renault':
                    if data[i]['Results'][j]['positionText'] not in dnf:
                        constructorDict['alpine']['result'] += int(data[i]['Results'][j]['position'])
                        constructorDict['alpine']['rc'] += 1
                    if data[i]['Results'][j]['grid'] != 0:
                        constructorDict['alpine']['quali'] += int(data[i]['Results'][j]['grid'])
                        constructorDict['alpine']['qc'] += 1

    
    for key, value in driverDict.items():
        driver = CurrentSeason.objects.get(driverId = key)
        driver.avgResult += round((value['result'] / value['rc']), 1)
        driver.avgQuali += round((value['quali'] / value['qc']), 1)
        driver.save()

    for key, value in constructorDict.items():
        con = CurrentSeason.objects.get(constructorId = key)
        con.avgResult += round((value['result'] / value['rc']), 1)
        con.avgQuali += round((value['quali'] / value['qc']), 1)
        con.save()

    url = 'https://ergast.com/api/f1/current/driverStandings.json'
    response = requests.get(url)
    data = response.json()['MRData']['StandingsTable']['StandingsLists']

    for i in range(len(data[0]['DriverStandings'])):
        driver = CurrentStanding(driverId = data[0]['DriverStandings'][i]['Driver']['driverId'], position = int(data[0]['DriverStandings'][i]['position']), points = float(data[0]['DriverStandings'][i]['points']))
        driver.save()

    url = 'https://ergast.com/api/f1/current/constructorStandings.json'
    response = requests.get(url)
    data = response.json()['MRData']['StandingsTable']['StandingsLists']

    for i in range(len(data[0]['ConstructorStandings'])):
        con = CurrentStanding(constructorId = data[0]['ConstructorStandings'][i]['Constructor']['constructorId'], position = int(data[0]['ConstructorStandings'][i]['position']), points = float(data[0]['ConstructorStandings'][i]['points']))
        con.save()