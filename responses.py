import requests
import json
import wmi

def get_response(message: str) -> str:

    p_message = message.lower()
    global response_w
    global response_json

    if p_message == "ping":
        return "pong"
    
    if p_message == "bot_version":
        return 
    
    if p_message == "cls":
        return 
    
    if p_message == "help":
        return '''
                    Moguce opcije su:
                    bot_version - za prikazivanje informacija o botu
                    help - pomocni meni
                    vreme posao - prikazivanje vremena za posao
                    vreme 3h - prikazivanje prognoze za naredna 3h
                    vreme osvezi - pribavljanje novih podataka za prognozu
                    rad main / rad alt - edom 
                    temps - prikazivanje hardware monitora
                '''
    
    if p_message == 'vreme osvezi':
        response_w = requests.get(url="http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/301537?apikey=CA9NQQq3k812FGW4wXWlCvA4pOD2onbY&details=true&metric=true")
        response_json = json.loads(response_w.content)
        return(response_w.status_code)

    if p_message.startswith('vreme'):
        
        if p_message == 'vreme posao':
            temp07 = ''
            temp15 = ''
            rainprob = ''
            for sets in response_json:
                if sets['DateTime'].split('T')[1].split(':')[0] == '07':
                    temp07 = str(sets['Temperature']['Value']) + sets['Temperature']['Unit']
                elif sets['DateTime'].split('T')[1].split(':')[0] == '15':
                    temp15 = str(sets['Temperature']['Value']) + sets['Temperature']['Unit']
                    rainprob += str(sets['RainProbability']) + '%'       
            return(f'''Vremenska prognoza Uzice:\n
                    Temperatura u 0700: {temp07}
                    Temperatura u 1500: {temp15}
                    Mogucnost padanja kise: {rainprob} % ''')

        if p_message == 'vreme 3h':
            with open('vreme.txt', 'w', encoding='utf-8') as f:
                f.write('Vremenska prognoza Uzice, za naredna 3 sata: \n\n')
            izlaz = ''
            brojac = 0
            sat = ''
            temp = ''
            vv = ''
            rainprob = ''
            ro = ''
            iconp = ''
            for sets in response_json:
                if brojac == 3:
                    break
                sat = sets['DateTime'].split('T')[1].split(':')[0]
                temp = str(sets['Temperature']['Value']) + sets['Temperature']['Unit']
                ro = str(sets['RealFeelTemperature']['Value']) + sets['RealFeelTemperature']['Unit']
                iconp = sets['IconPhrase']
                vv = str(sets['RelativeHumidity']) + '%'
                rainprob = str(sets['RainProbability']) + '%'
                with open('vreme.txt','a', encoding='utf-8') as f:
                    f.write(f'''Vremenska prognoza Uzice za {sat}h:
                                Temperatura : {temp}
                                Realan osecaj : {ro}
                                Oblacnost: {iconp}
                                Vlaznost vazduha: {vv}
                                Mogucnost padanja kise: {rainprob}

                                ''')
                brojac += 1
            with open('vreme.txt','r', encoding='utf-8') as f:
                izlaz = f.read()
            return izlaz
    
    if p_message == 'temps':
        w = wmi.WMI(namespace="root\OpenHardwareMonitor")
        temperature_infos = w.Sensor()
        interest = ['GPU Core','GPU Fan','CPU Package', 'CPU Total']
        w1 = w2 = ''
        with open('temps.txt', 'w', encoding='utf-8') as f:
                f.write('Hardware Monitor: \n\n')
        for sensor in temperature_infos:
            if sensor.name in interest:
                f = open('temps.txt', 'a', encoding='utf-8')
                if sensor.SensorType=='Temperature':
                    f.write(str(sensor.Name + ' {}C'.format("%.1f"%sensor.Value)+'\n'))
                elif sensor.SensorType=='Fan':
                    f.write(str(sensor.Name + ' {}%'.format(sensor.Value)+'\n'))
                else:
                    f.close()
                
        with open('temps.txt','r', encoding='utf-8') as f:
                izlaz = f.read()
                return izlaz
              
            
                 
    return "`Wrong command!`"