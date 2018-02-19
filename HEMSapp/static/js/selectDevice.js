function check_field_value(){
  if($(this).val() == 'Custom_Command_Input'){
    $('#custom').show();
  }
  else{
    $('#custom').hide();
  }
}

$(document).ready(function(){
  $('#hems_input').change(function(){
    check_field_value.call($('#hems_input'));
  });
});
