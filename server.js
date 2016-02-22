var stackexchange = require('stackexchange');

var options = { version: 2.2 };
var context = new stackexchange(options);

var filter = {
  key: 'NGR16KWDHIjGDT4E0ZBt4w((',
  pagesize: 50,
  tagged: 'node.js',
  sort: 'activity',
  order: 'asc'
};

// Get all the questions (http://api.stackexchange.com/docs/questions)
context.questions.questions(filter, function(err, results){
  if (err) throw err;

  //console.log(results.items);
  //console.log(results.has_more);
});

var answerFilter = {
  key: 'NGR16KWDHIjGDT4E0ZBt4w((',
  ids: ['35566051']
};
context.questions.answers(answerFilter, function(error, results) {
    console.log('error = ' + error);
    console.log('results = ' + JSON.stringify(results));
});