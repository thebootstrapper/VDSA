


/* estCorrect(id,etat)
cette fonction modifie le style des éléments de la liste décrivant le mot de mot_de_passe_ouble
*/
function estCorrect(id,etat){
  if (etat == false)// si la condition n est pas remplie on colore le message en rouge
    $("#"+id+"").css("color","red");
  else
    $("#"+id+"").css("color","#856404");
};



$(document).ready(function(){
  $("#inputPassword_1").focus();
});


$("#inputPassword_1").keyup(function(){

  var mot_de_passe_value = new String ($(this).val());

/*  je vérifie si le mot de passe contient plus de 8 caractères */
  var longueur = mot_de_passe_value.length;
  if (longueur<8)
    estCorrect("longueur",false);
  else {
      estCorrect("longueur",true);
  }
/*  je vérifie si le mot de passe contient un caractère numérique */
  var contient_num= new RegExp('\\d');
  if (contient_num.test(mot_de_passe_value)==false)
    estCorrect("caractere_num",false);
  else {
      estCorrect("caractere_num",true);
  }

/*  je vérifie si le mot de passe contient un caractère alpha-numérique */
  var contient_un_non_alpha_num= new RegExp('\\W');
  if (contient_un_non_alpha_num.test(mot_de_passe_value)==false)
    estCorrect("caractere_non_alpha_num",false);
  else {
      estCorrect("caractere_non_alpha_num",true);
  }

});



/* quand on envoie le formulairre */
$("#div_mot_de_passe").submit(function(){
/* je suppose que le mot de passe est valide, puis je fais vérifications */
  var mot_de_passe_est_correcte=true;
  var mot_de_passe_value = new String ($(this).val());


  var longueur = mot_de_passe_value.length;
  if (longueur<8){
      mot_de_passe_est_correcte=false;
      estCorrect("longueur",false);
  }
  else {
      estCorrect("longueur",true);
  }


  var contient_num= new RegExp('\\d');
  if (contient_num.test(mot_de_passe_value)==false){
      mot_de_passe_est_correcte=false;
      estCorrect("caractere_num",false);
  }
  else {mot_de_passe_correct
      estCorrect("caractere_num",true);
  }


  var contient_un_non_alpha_num= new RegExp('\\W');
  if (contient_un_non_alpha_num.test(mot_de_passe_value)==false){
      mot_de_passe_est_correcte=false;
      estCorrect("caractere_non_alpha_num",false);
  }
  else {
      estCorrect("caractere_non_alpha_num",true);
  }


  //si le mot de passe n'est pas correcte correcte on recharhge la page
  if ( mot_de_passe_est_correcte==false){
      location.reload();
    }
/*  else{

    // s il est correcte on envoie le formulaire par la methode POST au script qui l'insert dans la BD

      // si le retour est positif on affiche le message : "mot de passe enregistrer" avec un lien pour se connecter
      if (){

          }
      else {//si l'enregistrement ne s'est pas bien passé

        //si non on affiche un message d'erreur
      }
    }
*/
})
