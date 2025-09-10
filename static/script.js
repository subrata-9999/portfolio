let preLoader = document.getElementById("pre-loader");

function loading_function() {
  preLoader.style.display = "none";
}

let up_nav = document.querySelector(".navbar-toggler");

let nav = document.querySelector("nav");
window.addEventListener("scroll", function () {
  if (window.pageYOffset > 100) {
    nav.classList.remove("bg-transparent");
    nav.classList.add("shadow");
    document.querySelector(".navbar").style.paddingTop = "1%";
    document.querySelector(".navbar").style.paddingBottom = "1%";
  } else {
    nav.classList.add("bg-transparent");
    nav.classList.remove("bg-dark", "shadow");
    document.querySelector(".navbar").style.paddingTop = "2%";
    document.querySelector(".navbar").style.paddingBottom = "2%";
  }
});

let shutter_down = document.querySelector(".shutter_down");
shutter_down.addEventListener("click", function () {
  nav.classList.remove("bg-transparent");
});


emailjs.init("FHjQCdg0p2Dce04aZ");

    
      document.querySelector(".btn_c").addEventListener("click", function (e) {
        e.preventDefault(); // Prevent form submission
    
        const name = document.getElementById("user_name").value;
        const mail_id = document.getElementById("mail_id").value;
        const message = document.getElementById("message_body").value;
    
        if (name && mail_id && message) {
          // Send confirmation email to user
          emailjs.send("service_xyxk5uy", "template_16recw9", {
            to_name: name,
            from_name: "Subrata Pramanik",
            reply_to: mail_id,
            message: `Thanks ${name} for connecting me <3 \nI have received your email. We will get back shortly :) \nHave a nice day ☀️`,
          }).then(
            function(response) {
              alert("Message Sent Successfully\nCheck your Mail (spam also)");
            },
            function(error) {
              console.error("Failed to send confirmation email:", error);
              alert("Failed to send the confirmation email. Please try again.");
            }
          );
    
          // Send notification email to you
          emailjs.send("service_xyxk5uy", "template_16recw9", {
            to_name: "Subrat Pramanik",
            from_name: "Your Portfolio",
            message: message+ "\nThis is generated from your portfolio",
            reply_to: "myprotfolio357@gmail.com",
          }).then(
            function(response) {
              // alert("Message Sent Successfully\nCheck your Mail (spam also)");
              // Clear form fields
              console.log("Message Sent Successfully\nCheck your Mail (spam also), for owner");
          
            },
            function(error) {
              // console.error("Failed to send message:", error);
              // alert("Failed to send the message. Please try again.");
            }
          );

          document.getElementById("user_name").value = "";
          document.getElementById("mail_id").value = "";
          document.getElementById("message_body").value = "";
    
          
        } else {
          if (!message) {
            alert("Please fill the message section");
          } else if (!mail_id) {
            alert("Please enter your email ID");
          } else if (!name) {
            alert("Please enter your name");
          } else {
            alert("Please fill all the sections");
          }
        }
      });