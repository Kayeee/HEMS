function check_field_value(){
  if($(this).val() == 'Custom_Command_Input'){
    $('#custom').show();
  }
  else{
    $('#custom').hide();
  }
}

$(document).ready(function(){
  $('div select').first().change(function(){
    check_field_value.call($('div select').first());
  });
});
