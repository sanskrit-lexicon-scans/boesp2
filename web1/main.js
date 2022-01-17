// (setq js-indent-level 1)  # for Emacs

async function load_json_verse(verse,file,callback) {
 const response = await fetch(file);
 const json = await response.json();
 callback(json,verse);
}

function verse_error(verse) {
 let elt=document.getElementById('verse');
 let html = '<p>Could not find verse ' + verse + '</p>';
 elt.innerHTML = html;
}
function show_json4(x,verse) {
 //console.log('show_json4');
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
function get_verse_from_url() {
 /* two methods to get verse (X)
 ?verse=X
 ?X
*/
 let href = window.location.href;
 let url = new URL(href);
 let verse = url.searchParams.get('verse'); // Could be null
 if (verse == null) {
  let search = url.search  // ?X
  verse = search.substr(1)  // drop initial ?
 }
 //console.log('get_verse_from_url: ',verse);
 return verse;
}
function get_section_from_verse(verse) {
 let ans = null; // returned on error
 let i = parseInt(verse); // removes decimal part.
 if (isNaN(i)) {
  return ans;
 }
 if (i < 1) {
  return ans;
 }
 let s = i.toString();
 if (s.length > 4){
  return ans;
 }
 let s1 = s.padStart(4,'0');  // '12' -> '0012'
 let s2 = s1.substr(0,2); // '0123' -> '01'
 return s2;
}
function get_file_from_verse(verse) {
 //console.log('verse=',verse);
 let section = get_section_from_verse(verse);
 let file = null;
 if (section != null) {
  file = `json/section${section}.json`;
 }
 //console.log(`get_file_from_verse ${verse} ->${file}`);
 return file;
}

function display_verse_url() {
 let verse = get_verse_from_url();
 let file = get_file_from_verse(verse);
 load_json_verse(verse,file,show_json4)
  .catch(error => {
   verse_error(verse);
   });
}  

document.getElementsByTagName("BODY")[0].onload = display_verse_url;
