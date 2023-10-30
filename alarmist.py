
class Alarmist:
    
    def send_alarms(alarms) -> None:
        r = requests.post('https://httpbin.org/post', data = alarms)
        # TODO: check response status code
        # TODO: handle exceptions

    def authorize() -> None:
        pass
