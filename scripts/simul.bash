#!/bin/bash
for i in {1..10}
do
   sshpass -p 'alguma senha errada' ssh -o StrictHostKeyChecking=no user@localhost
done
