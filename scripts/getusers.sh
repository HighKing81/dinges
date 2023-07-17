#!/bin/bash
# Pre-migratie knutselwerkje van Michel
#
# Dit script output alle users met encoded passwords als knip/plak useradd commando.
# Hiermee kun je snel een lijst maken met alle users en deze als script uitvoeren
# op een andere machine om daar alle accounts snel aan te maken.
#
# LET OP! Dit script output ALLE accounts.
# Voer de ouput van dit script dus niet blind aan een andere machine zonder eerst even
# door de lijst te bladeren en systeemaccounts e.d. uit te filteren.
#
                                                                                                                                                                     
popusersgid=$(grep popusers /etc/group | cut -d':' -f3);
awk -F: '{ print $1" "$3" "$4" "$6" "$7 }' /etc/passwd | while read user uid gid homedir shell; do
        password=$(grep "^$user:" /etc/shadow | cut -d':' -f2);
        if [ "$gid" == "$popusersgid" ]; then
                echo "useradd -d $homedir -s /bin/false -p '$password' -g popusers $user"
        elif [ "$uid" -gt 499 ]; then
                echo "useradd -d $homedir -s $shell -p '$password' $user"
        fi
done
