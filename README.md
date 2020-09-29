# Python HN newsletter

Rewrite of the [previous version](https://github.com/dan-l/hn-newsletter) to use Python3 and AWS stack.

To deploy as lambda function, run `./deploy.sh`.

To update the dependencies for lambda function, run `pip3 install -t ../package/python -r requirements.txt` in hn-newsletter directory.

To lint, run `./pylint hn-newsletter`.  
