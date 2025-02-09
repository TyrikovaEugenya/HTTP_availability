# Test assignment for an intern in the direction of "Automated Testing (Python)"
A console program for testing server availability via the HTTP protocol.
The program measures the request execution time and outputs statistics on the server's response speed.

# Use of program

1. The `-H/--hosts` key with the value of the host(s) to which the requests will be sent. Multiple addresses can be specified, separated by commas without spaces.  
2. The optional `-C/--count` key with the value of the number of requests to be sent to each host to calculate the average response time (default is 1).  
3. The optional `-F/--file` key allows reading hostnames from a separate file (cannot be used simultaneously with `-H`).  
4. The optional `-O/--output` key allows specifying a file for outputting statistics (by default, the output is displayed in the console).

Example: python main.py –H https://ya.ru,https://google.com -C 5.

# Statistic output
The program outputs statistics on the server's response:
1. Host – the name of the tested host;
2. Success – the number of successful requests;
3. Failed – the number of requests that resulted in server errors (400 or 500);
4. Errors – the number of requests during which the server was unavailable;
5. Min – the minimum request execution time;
6. Max – the maximum request execution time;
7. Avg – the average request execution time;
