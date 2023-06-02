# myllm
CLI to text-generation-webui API

As it says--command line interface to whatever you have running locally in your text-generation-webui at port 5000.

> ./myllm.sh "What is the distance from the earth to the sun?"

The structure of the request assumes that you are using an OpenAssistant model.  If you are using a different model, change the assistant, prompter, and endofturn token files.

Inspired by Simon Williston's llm.sh

Includes api-example code from oobabooga
