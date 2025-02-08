import http
import requests
import argparse
import re

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--host', type=str)
    parser.add_argument('-C', '--count', type=int, default=1)
    parser.add_argument('-F', '--file', type=str)
    parser.add_argument('-O', '--output', type=str, default='console')

    args = parser.parse_args()

    return args
    
        
def getting_response(host, number_of_calls, args):
    success_count = 0
    failed_count = 0
    errors_count = 0
    times = []
    for i in range(number_of_calls):
        try:
            response = requests.get(host)
        except requests.exceptions.RequestException as e:
            print(f"Error occurred while making request to {host}: {e}")
            continue
        status = response.status_code
        if status == 200:
            success_count += 1
        elif status == 400 or status == 500:
            failed_count += 1
        elif status == 503:
            errors_count += 1
        time = response.elapsed.total_seconds()
        times.append(time)

    if times:
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
    else:
        min_time = max_time = avg_time = 0
    output(host, success_count, failed_count,
           errors_count, min_time, max_time, avg_time, args)

def output(host_name, success_count, failed_count,
           errors_count, min_time, max_time, avg_time, args):
    if args.output == 'console':
        print(f'''\nHost_name: {host_name}\nNumber of successed request: {success_count}\nNumber of failed request: {failed_count}\nNumber of errors: {errors_count}\nMinimum/Maximum elapsed time: {min_time}/{max_time}\nAverage elapsed time: {avg_time}.\n''')
    else:
        with open(args.output, 'w') as file:
            file.write(f'''\nHost_name: {host_name}\nNumber of successed request: {success_count}\nNumber of failed request: {failed_count}\nNumber of errors: {errors_count}\nMinimum/Maximum elapsed time: {min_time}/{max_time}\nAverage elapsed time: {avg_time}.\n''')

def try_match_host(list_of_requests):
    pattern = r'^(https?://)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(/.*)?$'
    for host in list_of_requests:
        if not re.match(pattern, host):
            print(f'{host} is not valid name of host')
            exit(1)
            
def gettimg_hosts_from_file(path):
    try:
        with open(path, 'r') as file:
            s = [line.strip('\n') for line in file.readlines()]
    except FileNotFoundError as e:
        print('Error: source file not found')
    return s
          

if __name__ == '__main__':
    args = get_arguments()
    if args.host and args.file:
        print("It can be only one argument - -H or -F")
        exit(1)
        
    if args.file:
        list_of_requests = gettimg_hosts_from_file(args.file)
    else:
        try:
            list_of_requests = args.host.split(',')
        except AttributeError as e:
            print('After key -H must be at least one adress')
            exit(1)
    number_of_calls = args.count
    try_match_host(list_of_requests)

    for host in list_of_requests:
        getting_response(host, number_of_calls, args)
    