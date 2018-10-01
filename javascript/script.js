let token = localStorage.getItem("token")

function getUrlVars() {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
    vars[key] = value;
    });
    return vars;
}
var id = getUrlVars()["id"];


function add_question(e){
    e.preventDefault()
    let title = document.getElementById("title").value
    let description = document.getElementById("description").value
    if(token ==null){
        window.location="index.html"
    }
    else{
        fetch("https://stack-challenge3.herokuapp.com/stack_overflow/api/v1/questions", {
        method:'POST',
        mode:'cors',
        headers:{
            'Accept':'application/json,text/plain,*/*',
            'Content-type':'application/json',
            'Authorization':'Bearer ' + token
        },
        body:JSON.stringify({question:title, description:description})
        })
        .then((response)=>response.json())
        .then((data) => {
            if(data['message'] == "Question successfully Added"){
                results = `<div id="success"><strong>Success! </strong> ${data['message']} </div>`
                document.getElementById('info-box').innerHTML = results

                window.setTimeout(function(){
                    window.location="post-question.html"
                },2000);
            }
        })
    }
}  



function signup(e){
    e.preventDefault()
    let fullname = document.getElementById("fullname").value
    let username = document.getElementById("username").value
    let email = document.getElementById("email").value
    let password = document.getElementById("password").value
    let confirm_password = document.getElementById("confirm_password").value

    if (password != confirm_password){
        document.getElementById('info-box').innerHTML = `<div id="warning">Passwords dont match</div>`
    }
    else{
        fetch("https://stack-challenge3.herokuapp.com/stack_overflow/api/v1/auth/signup", {
        method:'POST',
        mode:'cors',
        headers:{
            'Accept':'application/json,text/plain,*/*',
            'Content-type':'application/json'
        },
        body:JSON.stringify({fullname:fullname,username:username,email:email,password})
        })
        .then((response)=>response.json())
        .then((data) => {
            if(data['message'] == "User Successfully Added"){
                results = `<div id="success"><strong>Success! </strong> ${data['message']} </div>`
                document.getElementById('info-box').innerHTML = results

                window.setTimeout(function(){
                    window.location="sign-up.html"
                },2000);
            }
        })
    }
} 

function deleteQuestion(id){
    let questionId = id;
    if(confirm("Delete a question!")){
      return fetch("https://stack-challenge3.herokuapp.com/stack_overflow/api/v1/questions/"+id,{
          method:'DELETE',
          mode: 'cors',
          headers:{
              'Accept':'application/json,text/plain,*/*',
              'Content-type':'application/json',
              'Authorization':'Bearer ' + token
          }
      })
      .then((response) => response.json())
      .then((data) => {
          if(data['message'] == "Question was succesfully deleted"){
              results = `<div id="success"><strong>Success! </strong> ${data['message']} </div>`
              document.getElementById('info-box').innerHTML = results
  
              window.setTimeout(function(){
                  window.location="recently-asked-questions.html"
              },2000);
          }
          else{
              results = `<div id="warning"><strong>Warning! </strong> ${data['message']} </div>`
              document.getElementById('info-box').innerHTML = results
          }
      })
    }
  }

function saveAnswer(e){
    e.preventDefault()
    let answer = document.getElementById("answer").value
    fetch("https://stack-challenge3.herokuapp.com/stack_overflow/api/v1/questions/"+id+"/answers", { 
        method:'POST',
        mode:'cors',
        headers:{
            'Accept':'application/json,text/plain,*/*',
            'Content-type':'application/json',
            'Authorization':'Bearer ' + token              
        },
        body:JSON.stringify({answer:answer})
    })    
    .then((response) => response.json())
    .then((data) => console.log(data))

}