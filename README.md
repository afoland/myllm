# oracle.sh
CLI to text-generation-webui API

As it says--command line interface to whatever you have running locally in your text-generation-webui at port 5000.  (t-g-w must be started with the api flag)

Your prompt request should be in quotes:

> ./oracle.sh "What is the distance from the earth to the sun?"

The structure of the request assumes that you are using an OpenAssistant model.  If you are using a different model, change the assistant, prompter, and endofturn token files accordingly.

Inspired by Simon Williston's llm.sh, this queries instead locally.

Includes code taken from api-example of oobabooga
