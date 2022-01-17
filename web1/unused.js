/* These are some preliminary functions
written during development of main.js
Put here for (unlikely) further use
*/

function show_json(x) {
 console.log('show_json:',x);
 console.log('name=',x['prop']['name']);
}
function show_json1(x) {
 console.log('show_json1');
 let elt=document.getElementById('verse');
 let name = x['prop']['name'];
 let html = '<p>The name is ' + name + '</p>';
 elt.innerHTML = html;
}
function show_json2(x) {
 console.log('show_json2');
 let verse = "58"
 let elt=document.getElementById('verse');
 let html = null;
 for (let i=0;i<x.length;i++) {
  let y = x[i];
  let L = y['L'];
  if (verse == L) {
   html = y['html'];
   break;
  }
 }
 if (html == null) {
  html = '<p>Could not find verse ' + verse + '</p>';
 }
 elt.innerHTML = html;
}
function load_json(file,callback) {
 // Ref: https://thecodingtrain.com/Courses/data-and-apis/1.1-fetch.html
 fetch(file)
  .then(x => {
   console.log('response');
   return x.json();
  })
  .then(x => {
   callback(x);
  })
}
//load_json('json/section00.json',show_json3)
/*
let x = document.getElementsByTagName("BODY")[0];
x.onload = display_verse_url;
console.log('added load listener',x);
*/
function load_json_verse_notasync(verse,file,callback) {
 // not needed
 fetch(file)
  .then(x => {
   console.log('response');
   return x.json();
  })
  .then(x => {
   callback(x,verse);
  })
  .catch(error => {
   verse_error(verse);
  })
}
function show_json3(x) {
 console.log('show_json3');
 let verse = "69"
 let elt=document.getElementById('verse');
 let html = null;
 if (verse in x) {
  html = x[verse]
 }
 if (html == null) {
  html = '<p>Could not find verse ' + verse + '</p>';
 }
 elt.innerHTML = html;
}
