# LexisNexisHackBot

## Sentiments

Creating an intelligent bot that will simplify getting relevant information and solving problems.

## Contributors

[Abhinav Medhekar](amedhek@ncsu.edu), [Atit Shetty](atit.shetty@gmail.com), [Harshal Gurjar](hkgurjar@ncsu.edu)

## Microsoft Bot Framework

[Microsoft Resource for Node](https://docs.microsoft.com/en-us/bot-framework/nodejs/bot-builder-nodejs-quickstart)

[Link to bot emulator](https://github.com/Microsoft/BotFramework-Emulator/releases/tag/v3.5.31)

## How to run the application

If .env file present run (sample .env file has been provided)

```node -r dotenv/config app.js```

If .env file not present, set the environment variables present in the file and then run

```node app.js```

## Configurations

LUIS_config.xml is the configuration to set up intents and utterances in Microsoft LUIS website.

output.tsv has been created by parsing Lexis Advance xml. This will be used for NLP processing by Microsoft QNA cognitive service.



