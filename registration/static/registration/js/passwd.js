         function myFunction()
{
    $('#signup').bootstrapValidator({
        icon: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },

        fields: {
            password1: {
                validators: {
                    notEmpty: {
                        message: 'The password is required and can\'t be empty'
                    },
                    identical: {
                        field: 'password2',
                        message: 'The password and its confirm are not the same'
                    }
                }
            },
            password2: {
                validators: {
                    identical: {
                        field: 'password1',
                        message: 'The password and its confirm are not the same'
                    }
                }
            }
        }
    });

    }
    $(document).ready(myFunction());
