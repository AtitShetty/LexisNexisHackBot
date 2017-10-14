var builder = require('botbuilder');
var restify = require('restify');
var cognitiveservices = require('botbuilder-cognitiveservices');
var google = require('google');

google.resultsPerPage = 3;


// Setup Restify Server
var server = restify.createServer();
server.listen(process.env.port || process.env.PORT || 3978, function() {
    console.log('%s listening to %s', server.name, server.url);
});

// Create chat connector for communicating with the Bot Framework Service
var connector = new builder.ChatConnector({
    appId: process.env.MICROSOFT_APP_ID,
    appPassword: process.env.MICROSOFT_APP_PASSWORD
});

// Listen for messages from users
server.post('/api/messages', connector.listen());



// Receive messages from the user and respond by echoing each message back (prefixed with 'You said:')
var bot = new builder.UniversalBot(connector);



var luisAppUrl = process.env.LUIS_APP_URL;
var luisRecognizer = new builder.LuisRecognizer(luisAppUrl);

var qnarecognizer = new cognitiveservices.QnAMakerRecognizer({
    knowledgeBaseId: process.env.QNA_KB_ID,
    subscriptionKey: process.env.QNA_SUB_KEY,
    top: 3,
    qnaThreshold: 0.85
});

var intents = new builder.IntentDialog({
    recognizers: [qnarecognizer, luisRecognizer],
    recognizeOrder: builder.RecognizeOrder.series
});

bot.on('conversationUpdate', function(message) {
    if (message.membersAdded) {
        message.membersAdded.forEach(function(identity) {
            if (identity.id == message.address.bot.id) {
                var reply = new builder.Message()
                    .address(message.address)
                    .text("Welcome to Lexis Advance.<br>How can I help you?<br>You can ask questions like \"How do I filter results after search?\" or \"How to create a new folder?\"");
                bot.send(reply);
            }
        });
    }
});

bot.dialog('/', intents);


intents.matches('qna', [
    function(session, args) {
        var answerEntity = JSON.parse(builder.EntityRecognizer.findEntity(args.entities, 'answer').entity);

        session.dialogData.answerEntity = answerEntity;

        session.send(answerEntity.summary);

        if (answerEntity.additionalLinks && answerEntity.additionalLinks != "None") {
            builder.Prompts.confirm(session, "We found some additional links topics. Do you want to view them?");
        } else {
            session.endConversation();
        }
    },
    function(session, results) {
        if (results.response) {
            session.send(session.dialogData.answerEntity.additionalLinks);
        } else {
            session.send("That's alright, you can continue exploring more topics.");
        }
    }
]);

// intents.matches('Help', [
//     function(session) {
//         session.send("How can I help you?<br>You can ask questions like \"How do I filter results after search?\" or \"How to create a new folder?\"");
//     }
// ]);

intents.onDefault([
    function(session) {
        session.dialogData.searchMsg = session.message.text;
        builder.Prompts.confirm(session, "No results found.<br>Do you wish to perform a google search?");
    },
    function(session, results) {
        if (results.response) {
            console.log("Atit" + session.dialogData.searchMsg);
            google(session.dialogData.searchMsg, function(err, res) {
                if (err) {
                    console.error(err);
                } else {
                    console.log(JSON.stringify(res))
                    var searches = "";
                    for (var i in res.links) {
                        console.log(res.links[i])
                        if (res.links[i] && res.links[i].title && res.links[i].href) {
                            var link = res.links[i];
                            searches += link.title + ' - ' + link.href + "<br><br>";
                        }
                    }

                    session.send(searches);

                }

            });
        } else {
            session.send("That's alright, you can refine your search.");
        }
    }
]);
