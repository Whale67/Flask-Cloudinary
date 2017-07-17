
var user_image = $('#user_upload').attr('public_id')

var generateSignature = function(callback, params_to_sign){
    $.ajax({
      url     : "/signature",
      type    : "POST",
      dataType: "text",
      data    : { data: params_to_sign},
      complete: function() {console.log("complete")},
      success : function(signature, textStatus, xhr) { callback(signature); },
      error   : function(xhr, status, error) { console.log(xhr, status, error); }
    });
  }

  
  $('#upload_widget_opener').cloudinary_upload_widget(
    { cloud_name: '<cloud_name>', 
      upload_preset: '<preset>', 
      api_key: '<api_key>',
      upload_signature: generateSignature,
      cropping: 'server', 
      cropping_aspect_ratio: 1,
      cropping_default_selection_ratio: 1.0,
      theme: 'purple', 
      sources: ['local', 'camera'], 
      resource_type: 'image', 
      client_allowed_formats: ["png","jpg", "jpeg"],
      form: '#upload_form',
      field_name: 'image',
      max_files: 1,
      thumbnails: false,
      multiple: false,
      public_id: user_image,
      button_caption: 'Upload',
      button_class: 'sr-button' 
  }, 
    function(error, result) { 
            $.each(result, function(index, object) {
                $('#user_upload').attr('src', 'https://res.cloudinary.com/ds8bt3a3o/image/upload/v' + object.version +'/' + object.public_id);

                $.ajax({
                    data : {
                      public_id: object.public_id,
                      version: object.version
                    },
                    type : 'POST',
                    url : '/image_id'
                  })
                            })
                        } 
                      );