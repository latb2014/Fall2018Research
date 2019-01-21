console.log("Hello");

function populateSVG(patternNumber, sentenceID) {
  d3.select('#mainSVG').remove();
  var svg = document.createElement("svg");
  $(svg).attr("id", "mainSVG");
  $(svg).attr("viewBox", "0 0 100 100");
  $(svg).attr("preserveAspectRatio", "xMinYMax meet");
  
  $("#svgContainer").append(svg);
  
  var xValue = 20;
  $.getJSON("/barrett/credibility_pattern_dictionaries.json", function(dataReal)
{
    var sentenceList = dataReal[patternNumber]['pattern_annotated_sents'][sentenceID];
    var i;
    for(i = 0; i < sentenceList.length; i++){
        var svgText = document.createElement("text");
      $(svgText).attr("y", 100);
      //$(svgText).attr("x", xValue);
      $(svgText).attr("id", "textElem");
      //$(svgText).text(sentenceList[i]['the_string']);
      $(svg).append(svgText);
      
      var svgTspan = document.createElement("tspan");
      $(svgTspan).attr("x", xValue);
      $(svgTspan).attr("id", "tspanElem");
      $(svgTspan).text(sentenceList[i]['the_string']);
      $(svgText).append(svgTspan);
      
      xValue = xValue + 100;
    }
});
  
  
}

function populatePatterns(){
  var listHolder = document.getElementById("holdingTank");
  while (listHolder.firstChild) {
    listHolder.removeChild(listHolder.firstChild);
  }
  $.getJSON("/barrett/credibility_pattern_dictionaries.json", function(credDictionary)
  {
    $.getJSON("/scripts/credibility_unannotated_documents.json", function(unanDocs)
    {
      
      var i = 0;
      $.each( credDictionary, function( key, value ){
        var listGroup = document.createElement("div");
        listGroup.classList.add('list-group');
        $(listHolder).append(listGroup);
        var j;
        for(j = 0; j < value['pattern_n_sents']; j++){
          var sentenceIndex = value['pattern_sent_ids'][j];
          var listItem = document.createElement("a");
          listItem.classList.add('list-group-item');
          listItem.classList.add('list-group-item-action');
          $(listItem).attr('data-toggle', 'list');
          $(listItem).text(unanDocs[sentenceIndex]);
          $(listItem).attr('onclick', 'populateSVG('+ key + ', ' + sentenceIndex +')');
          $(listGroup).append(listItem);
        }
      });
    });
  });
}