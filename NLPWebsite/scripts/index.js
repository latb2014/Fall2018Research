/**
 * index.js
 * - All our useful JS goes here, awesome!
 */

console.log("JavaScript is amazing! default555");

$('#Credibility').click(function() {
 $('#expandList').empty();
 $("<li class=\"list-group-item\">Cred</li>").appendTo('#expandList');
});

$('#Politeness').click(function() {
 $('#expandList').empty();
 $("<li class=\"list-group-item\">Pol</li>").appendTo('#expandList');
});

$('#Sentiment').click(function() {
 $('#expandList').empty();
 $("<li class=\"list-group-item\">Sent</li>").appendTo('#expandList');
});

$('#Custom').click(function() {
 $('#expandList').empty();
 $("<li class=\"list-group-item\">Custo</li>").appendTo('#expandList');
});