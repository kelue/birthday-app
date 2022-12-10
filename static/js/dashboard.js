document.getElementById('copy-text').addEventListener('click', function(e){ 
    
  });

function copyText(){
    let myUrl = document.getElementById("user-link").innerHTML;
    myUrl = myUrl.split('<')
    myUrl = myUrl[0].trim()
    copytoclipboard(myUrl)
    alert(myUrl + ' copied to clipboard!')
}

function copytoclipboard(str){
    const el = document.createElement('textarea');
    el.value = str;
    document.body.appendChild(el);
    el.select();
    document.execCommand('copy');
    document.body.removeChild(el);
}
