import subprocess #import required library
data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('gbk').split('\n') #store profiles data in "data" variable
profiles = [i.split(":")[1][1:-1] for i in data if"所有用户配置文件"in i] #store the profile by converting them to list
for i in profiles:
    # running the command to check passwords
    results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('gbk').split('\n')
    # storing passwords after converting them to list
    results = [b.split(":")[1][1:-1] for b in results if"关键内容"in b]
    if results:
        print ("{:<30}|  {:<}".format(i, results[0]))
        
    # try:
        
    # except IndexError:
    #     print ("{:<30}|  {:<}".format(i, ""))