
/* alerte_erreur(message)
cette fonction ajoute un alerte dans la div dont l'identifiant est "div_erreur"
id est la valeur de l'identifiant du div ajouté*/
function alerte_erreur(id,message){
  $("#div_erreur").append("<div id=\""+ id + "\" class=\"col-11 col-xl-6  col-lg-6 col-md-8 col-sm-10  \" ><div style=\"text-align:center;\" class=\"alert alert-danger\" role=\"alert\"> "
  + message + "</div></div>");
}

// cette vaariable permet de savoir si on a déaffiché le message d'erreur,pour éviter de l'afficher plusieurs fois
var tableau_erreur_affiché= {"le_mail_de_creation_de_compte_ne_contient_pas_arobase":false ,//le mail du formaulaire de creation de compte
                             "le_mail_de_connexion_de_compte_ne_contient_pas_arobase":false} ;
var premiere_fois=true;
$( document ).ready(function(){
  $("#div_creation_compte").hide();
  $("#div_connexion").hide();
  $("#creation_compte_alerte").hide();
  $("#magasin_row").hide();

});

$("#seconnecter").click(function(){
  $("#div_creation_compte").hide();
  $("#creation_compte_alerte").hide();
  $("#div_connexion").show(1000);

  $("#le_mail_de_creation_de_compte_ne_contient_pas_arobase").remove();
  tableau_erreur_affiché.le_mail_de_creation_de_compte_ne_contient_pas_arobase=false;


  var active=$(this).parent().hasClass("active");
  if ( active = "false"){
    $(this).parent().addClass("active");
    $("#creeruncompte").parent().removeClass("active");
  }


      var email = $("#input_email_connexion");
      email.focus();
      var email_value = new String(email.val());


      if(  (email_value.length > 0) && email_value.search("@")==-1
         && tableau_erreur_affiché.le_mail_de_connexion_de_compte_ne_contient_pas_arobase==false){

      alerte_erreur("le_mail_de_connexion_de_compte_ne_contient_pas_arobase","Merci d'entrer une adresse mail correcte");
      tableau_erreur_affiché.le_mail_de_connexion_de_compte_ne_contient_pas_arobase=true;
      console.log("affichie apres click ssur se connecter")
    }
    console.log(email_value);
});




  $("#input_email_connexion").keyup(function(){
    var email = $("#input_email_connexion");
    var email_value = new String(email.val());

    console.log( email_value.length > 0 && email_value.search("@")==-1
    && (tableau_erreur_affiché.le_mail_de_connexion_de_compte_ne_contient_pas_arobase===false));

  if( email_value.length > 0 && email_value.search("@")==-1
    && (tableau_erreur_affiché.le_mail_de_connexion_de_compte_ne_contient_pas_arobase===false)){
    alerte_erreur("le_mail_de_connexion_de_compte_ne_contient_pas_arobase","Merci d'entrer une adresse mail correcte");
    tableau_erreur_affiché.le_mail_de_connexion_de_compte_ne_contient_pas_arobase=true;
    console.log("pas de @")
  }

  else if ( email_value.search("@") > 0)
    {
      console.log("efface moi ca");
      $("#le_mail_de_connexion_de_compte_ne_contient_pas_arobase").remove();
      tableau_erreur_affiché.le_mail_de_connexion_de_compte_ne_contient_pas_arobase=false;
    }
  });




$("#creeruncompte").click(function(){
  $("#div_connexion").hide();
  $("#div_creation_compte").show(1000);
  $("#creation_compte_alerte").show();

//suppression du messsage d'erreur
  $("#le_mail_de_connexion_de_compte_ne_contient_pas_arobase").remove();
  tableau_erreur_affiché.le_mail_de_connexion_de_compte_ne_contient_pas_arobase=false;

var active=$(this).parent().hasClass("active");
  if ( active = "false"){
    $(this).parent().addClass("active");
    $("#seconnecter").parent().removeClass("active");
  }

  $("#directeur_label").click(function(){
        $("#magasin_row").show(500);
  });

  $("#commercial_label").click(function(){
        $("#magasin_row").hide(500);
  });


  $("#nom").focus();
  var email = $("#input_email_creation_de_compte");
  var email_value = new String(email.val());

  console.log(email_value)
  if( email_value.length > 0 && email_value.search("@")==-1
     && tableau_erreur_affiché.le_mail_de_creation_de_compte_ne_contient_pas_arobase==false ){
  alerte_erreur("le_mail_de_creation_de_compte_ne_contient_pas_arobase","Merci d'entrer ne addresse mail correcte. Exemple: toto@gmail.com");
  tableau_erreur_affiché.le_mail_de_creation_de_compte_ne_contient_pas_arobase=true;
}
});

$("#input_email_creation_de_compte").keyup(function(){
  var email = $("#input_email_creation_de_compte");
  var email_value = new String(email.val());

  if( email_value.length > 0 && email_value.search("@")==-1
  && tableau_erreur_affiché.le_mail_de_creation_de_compte_ne_contient_pas_arobase==false){
  alerte_erreur("le_mail_de_creation_de_compte_ne_contient_pas_arobase","Merci d'entrer une adresse mail correcte");
  tableau_erreur_affiché.le_mail_de_creation_de_compte_ne_contient_pas_arobase=true;
}
else if ( email_value.search("@") > 0)
  {
    $("#le_mail_de_creation_de_compte_ne_contient_pas_arobase").remove();
    tableau_erreur_affiché.le_mail_de_creation_de_compte_ne_contient_pas_arobase=false;
  }
});

$("#connexion_formulaire").submit(function(){
  // si le mail n est pas valide
  if ( tableau_erreur_affiché.le_mail_de_connexion_de_compte_ne_contient_pas_arobase==true){
    location.reload();
  }
  else {//si le mail est valide

    // on envoie les données par la methode post au scripte qui vérifie leur existantce dans la BD
    // si le retour est positif on le connecte au site
    document.location.href="http://www.google.com/";

    //si non on recharge la page on affichant le message d'erreur: identifiant ou mot de passe incorrecte
  }
})

$("#creation_de_compte_formulaire").submit(function(){
  // si le mail n est pas valide
   if ( tableau_erreur_affiché.le_mail_de_creation_de_compte_ne_contient_pas_arobase==true){
    location.reload();
  }
  else {//si le mail est valide

    // on envoie les donnée par la methode post au script qui envoie le mail
    // si le retour est positif on affiche le message : mail envoyé

    //si non on affiche un message d'erreur
  }
})
