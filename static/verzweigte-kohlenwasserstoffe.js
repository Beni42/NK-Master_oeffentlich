$(document).ready(function (){

    let question_at = -1,
    correct_answers = 0,
    question = ["Wie lautet dieses Molekül nach IUPAC? Schreibe den Namen des Moleküls in das Eingabe-Feld"],
    solution = ["3,4-Dimethylheptan", "5-Ethyl-3,7,8-trimethylundecan", "4-Ethyl-2-methylheptan", "2-Methylpent-2-en", "5-Methyl-4-propylhept-2-en", "2,2,3,6-Tetramethyloct-4-en", "3-Ethyl-2,7-dimethyldec-5-in"],
    Image = ["../static/uebungen/verzweigte_kohlenwasserstoffe/Aufgabe1.png",
    "../static/uebungen/verzweigte_kohlenwasserstoffe/Aufgabe2.png",
    "../static/uebungen/verzweigte_kohlenwasserstoffe/Aufgabe3.png",
    "../static/uebungen/verzweigte_kohlenwasserstoffe/Aufgabe4.png",
    "../static/uebungen/verzweigte_kohlenwasserstoffe/Aufgabe5.png",
    "../static/uebungen/verzweigte_kohlenwasserstoffe/Aufgabe6.png",
    "../static/uebungen/verzweigte_kohlenwasserstoffe/Aufgabe7.png"],
    number_of_questions = solution.length;

    function load_question(){
        question_at++;
        console.log("Fragerunde "+question_at,"Anzahl_Aufgaben "+number_of_questions);
        $('#check_answer, #input').prop('disabled', false);
        $('#next').prop('disabled', true);
        $('#response').text('');
        $("#question").text(question[0]);
        progress = question_at / number_of_questions * 100;
        $('#counter').css('width', ''+progress+'%');
        console.log(progress);
        $('#input').prop('value', '');
        if (typeof Image[question_at] == "string"){
            $('#image').prop("src", Image[question_at]);
        }
        if (question_at>=number_of_questions-1){
            $('#switch_buttons').hide();
            $('#finish').show();
            $('#finish').prop('disabled', true);
        }
    }

    function check_answer(){
        if(!$('#input').val()) {
            $('#response').text('Du musst zuerst eine Antwort eintippen').css('color', 'red');
        } else {
            if ($('#input').val() == solution[question_at]){
                $('#response').text('Richtig. Die Lösung lautet '+solution[question_at]).css('color', 'green');
                correct_answers++
            } else {
                $('#response').text('Falsch. Die Lösung lautet '+solution[question_at]).css('color', 'red');
            }
            $('#check_answer, #input').prop('disabled', true);
            $('#next').prop('disabled', false);
            if (question_at>=number_of_questions-1){
                $('#finish').prop('disabled', false)
            }
        }
    }

     function finish(){
        $('#solve').hide();
        $('#end').show();
        $('#final_result').text("Du hast " +correct_answers+ " von " +number_of_questions+ " Aufgaben richtig gelöst.");
        $.ajax({
            url: '',
            method: 'post',
            contentType: 'application/json',
            data: JSON.stringify({
                answers_right: correct_answers,
                answers_total: number_of_questions,
            }),
        })
    }

    $('#end, #finish').hide();

    load_question();

    $('#next').on('click', load_question);

    $('#check_answer').on('click', check_answer);

    $('#finish').on('click',finish);

    $(document).on("keypress", function(event){
        if (event.which === 13 && $('#check_answer').prop('disabled') === false){
            check_answer();
            console.log('it worked')
        } else if (event.which === 13 && $('#next').prop('disabled') === false && !(question_at>=number_of_questions-1)) {
            load_question();
            console.log('it worked too')
        } else if (event.which === 13 && $('#finish').prop('disabled') === false && question_at>=number_of_questions-1){
            finish();
        }
     })
})