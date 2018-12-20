
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

/* au chargement de la page on cache le formulaire de creation de Compte et ses alertes */
$( document ).ready(function(){
  $("#div_creation_compte").hide();
  $("#creation_compte_alerte").hide();
  $("#magasin_row").hide();

});


/* ce code est exécuté à chaque fois qu'on saisie une lettre dan sle champs d 'email du formulaire de connexion affichier afficher par défaut au chargement de la page */
  $("#input_email_connexion").keyup(function(){
  /* je récupère l"email saisie dans une variable */
    var email = $("#input_email_connexion");
    var email_value = new String(email.val());

/*    console.log( email_value.length > 0 && email_value.search("@")==-1
    && (tableau_erreur_affiché.le_mail_de_connexion_de_compte_ne_contient_pas_arobase===false));
*/

/* s'il ne contient pas "@" et qu'on a pas encore afficher l'erreur alors on l 'affiche */
  if( email_value.length > 0 && email_value.search("@")==-1
    && (tableau_erreur_affiché.le_mail_de_connexion_de_compte_ne_contient_pas_arobase===false)){
    alerte_erreur("le_mail_de_connexion_de_compte_ne_contient_pas_arobase","Merci d'entrer une adresse mail correcte");
    tableau_erreur_affiché.le_mail_de_connexion_de_compte_ne_contient_pas_arobase=true;
    console.log("pas de @")
  }
/* si le mail contient "@", on supprime l'erreur */
  else if ( email_value.search("@") > 0)
    {
      /*console.log("efface moi ca");*/
      $("#le_mail_de_connexion_de_compte_ne_contient_pas_arobase").remove();
      tableau_erreur_affiché.le_mail_de_connexion_de_compte_ne_contient_pas_arobase=false;
    }
  });



/* code exécuter à chaque fois qu'on clique sur le boutton "se connecter" de la bar de navigation */
$("#seconnecter").click(function(){
  /* on cahce le formulaire de creation de compte au profis du formulaire de connexion */
  $("#div_creation_compte").hide();
  $("#creation_compte_alerte").hide();
  $("#div_connexion").show(1000);

  /* j'efface le message d'alerte concernant le formulaire de creation de compte */
  $("#le_mail_de_creation_de_compte_ne_contient_pas_arobase").remove();
  tableau_erreur_affiché.le_mail_de_creation_de_compte_ne_contient_pas_arobase=false;

/* je desactive le boutton "creation de compte" de la barre de navigation au profis de celui de "connexion"*/
  var active=$(this).parent().hasClass("active");
  if ( active = "false"){
    $(this).parent().addClass("active");
    $("#creeruncompte").parent().removeClass("active");
  }

/* je récupère l"email saisie dans une variable */
      var email = $("#input_email_connexion");
      email.focus();
      var email_value = new String(email.val());

/* s'il ne contient pas "@" et qu'on a pas encore afficher l'erreur alors on l 'affiche */
      if(  (email_value.length > 0) && email_value.search("@")==-1
         && tableau_erreur_affiché.le_mail_de_connexion_de_compte_ne_contient_pas_arobase==false){

      alerte_erreur("le_mail_de_connexion_de_compte_ne_contient_pas_arobase","Merci d'entrer une adresse mail correcte");
      tableau_erreur_affiché.le_mail_de_connexion_de_compte_ne_contient_pas_arobase=true;
      console.log("affichie apres click ssur se connecter")
    }
    console.log(email_value);
});




/* code exécuter à chaque fois qu'on clique sur le boutton "creer un compte" de la bar de navigation */
$("#creeruncompte").click(function(){
  $("#div_connexion").hide();
  $("#div_creation_compte").show(1000);
  $("#creation_compte_alerte").show();

//suppression du messsage d'erreur
  $("#le_mail_de_connexion_de_compte_ne_contient_pas_arobase").remove();
  tableau_erreur_affiché.le_mail_de_connexion_de_compte_ne_contient_pas_arobase=false;


  /* je desactive le boutton "connexion" de la barre de navigation au profis de celui de "creation de compte*/
var active=$(this).parent().hasClass("active");
  if ( active = "false"){
    $(this).parent().addClass("active");
    $("#seconnecter").parent().removeClass("active");
  }


/* quand on clic sur directeur de magasin, on affiche le champs "Magasin" */
  $("#directeur_label").click(function(){
        $("#magasin_row").show(500);
  });

/* quand clic sur "commercial" on cache le champs "Magasin"*/
  $("#commercial_label").click(function(){
        $("#magasin_row").hide(500);
  });


  $("#nom").focus();
  var email = $("#input_email_creation_de_compte");
  var email_value = new String(email.val());


  /* s'il ne contient pas "@" et qu'on a pas encore afficher l'erreur alors on l 'affiche */
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


/* quand on envoie le formualire de connexion */
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


/* quand on envoie le formaulaire de creation de compte*/
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
